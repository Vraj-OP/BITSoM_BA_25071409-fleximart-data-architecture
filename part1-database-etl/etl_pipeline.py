"""
FlexiMart ETL Pipeline (Part 1)

Deliverables:
- etl_pipeline.py: ETL script with comments + error handling + logging
- data_quality_report.txt: Generated report showing:
  - number of records processed per file
  - number of duplicates removed
  - number of missing values handled
  - number of records loaded successfully

Reads raw CSVs from: ../data/
Loads into provided DB schema:
- customers
- products
- orders
- order_items

How to run (Windows PowerShell):
1) pip install -r part1-database-etl/requirements.txt
2) setx DB_URL "mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/fleximart"
   (Restart terminal)
3) python part1-database-etl/etl_pipeline.py
"""

import os
import re
import logging
from collections import defaultdict

import numpy as np
import pandas as pd
from dateutil import parser
from sqlalchemy import create_engine, text


# ----------------------------
# Paths (as per repo structure)
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))           # .../part1-database-etl
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data")) # .../data

CUSTOMERS_CSV = os.path.join(DATA_DIR, "customers_raw.csv")
PRODUCTS_CSV  = os.path.join(DATA_DIR, "products_raw.csv")
SALES_CSV     = os.path.join(DATA_DIR, "sales_raw.csv")

REPORT_PATH   = os.path.join(BASE_DIR, "data_quality_report.txt")


# ----------------------------
# Logging (required for code quality marks)
# ----------------------------
logging.basicConfig(
    filename=REPORT_PATH,
    level=logging.INFO,
    format="%(message)s"
)

metrics = defaultdict(int)  # for report numbers


# ----------------------------
# Cleaning helper functions
# ----------------------------
def clean_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Trim spaces in all string columns and normalize empty strings to NaN."""
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({"nan": np.nan, "None": np.nan, "": np.nan})
    return df


def standardize_phone(x):
    """Convert phone numbers to +91XXXXXXXXXX (Indian 10-digit format)."""
    if pd.isna(x):
        return None
    s = str(x).strip()
    digits = re.sub(r"\D", "", s)  # keep digits only

    # remove leading 0 (e.g., 0987...)
    if len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]

    # remove leading 91 (e.g., 919876...)
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]

    if len(digits) != 10:
        return None
    return f"+91{digits}"


def standardize_email(x):
    """Lowercase + basic validation. Returns None if invalid."""
    if pd.isna(x):
        return None
    s = str(x).strip().lower()
    return s if ("@" in s and "." in s) else None


def parse_date_to_yyyy_mm_dd(x):
    """Convert mixed date formats to YYYY-MM-DD. Returns None if unparseable."""
    if pd.isna(x):
        return None
    s = str(x).strip()

    # Try robust parsing. Attempt both dayfirst False and True.
    for dayfirst in (False, True):
        try:
            dt = parser.parse(s, dayfirst=dayfirst)
            return dt.strftime("%Y-%m-%d")
        except Exception:
            continue
    return None


def standardize_category(x):
    """Standardize categories: Electronics/Fashion/Groceries"""
    if pd.isna(x):
        return None
    s = str(x).strip().lower()
    mapping = {
        "electronics": "Electronics",
        "fashion": "Fashion",
        "groceries": "Groceries"
    }
    return mapping.get(s, s.title())


def placeholder_email(customer_code: str) -> str:
    """
    customers.email is UNIQUE + NOT NULL in the schema, but raw data has missing emails.
    Create a safe unique placeholder email.
    """
    safe = (customer_code or "unknown").strip().lower()
    return f"missing.{safe}@fleximart.local"


# ----------------------------
# Extract
# ----------------------------
def extract():
    """Read all three CSV files."""
    if not os.path.exists(CUSTOMERS_CSV):
        raise FileNotFoundError(f"Missing file: {CUSTOMERS_CSV}")
    if not os.path.exists(PRODUCTS_CSV):
        raise FileNotFoundError(f"Missing file: {PRODUCTS_CSV}")
    if not os.path.exists(SALES_CSV):
        raise FileNotFoundError(f"Missing file: {SALES_CSV}")

    customers = clean_whitespace(pd.read_csv(CUSTOMERS_CSV))
    products  = clean_whitespace(pd.read_csv(PRODUCTS_CSV))
    sales     = clean_whitespace(pd.read_csv(SALES_CSV))

    metrics["customers_raw"] = len(customers)
    metrics["products_raw"] = len(products)
    metrics["sales_raw"] = len(sales)

    return customers, products, sales


# ----------------------------
# Transform
# ----------------------------
def transform_customers(customers: pd.DataFrame) -> pd.DataFrame:
    """Fix missing emails, standardize phone/date, remove duplicates."""
    customers = customers.copy()

    # Standardization
    customers["email"] = customers["email"].apply(standardize_email)
    customers["phone"] = customers["phone"].apply(standardize_phone)
    customers["registration_date"] = customers["registration_date"].apply(parse_date_to_yyyy_mm_dd)

    # Duplicate removal (C001 duplicated in your data)
    before = len(customers)
    customers = customers.drop_duplicates(subset=["customer_id"], keep="first")
    metrics["customers_duplicates_removed"] = before - len(customers)

    # Missing emails handled (NOT NULL in schema)
    missing_emails = customers["email"].isna().sum()
    metrics["customers_missing_email_handled"] = int(missing_emails)

    customers["email"] = customers.apply(
        lambda r: r["email"] if pd.notna(r["email"]) else placeholder_email(r["customer_id"]),
        axis=1
    )

    # Ensure uniqueness if any collision (rare but safe)
    dup_mask = customers["email"].duplicated(keep=False)
    if dup_mask.any():
        counts = customers.groupby("email").cumcount()
        customers.loc[dup_mask, "email"] = customers.loc[dup_mask, "email"] + "." + counts[dup_mask].astype(str)

    # Fill required names (schema says NOT NULL)
    customers["first_name"] = customers["first_name"].fillna("Unknown")
    customers["last_name"] = customers["last_name"].fillna("Customer")

    return customers


def transform_products(products: pd.DataFrame) -> pd.DataFrame:
    """Standardize category, handle missing price/stock, remove duplicates."""
    products = products.copy()

    products["category"] = products["category"].apply(standardize_category)
    products["product_name"] = products["product_name"].astype(str).str.strip()

    # Price missing -> fill using category median, fallback overall median
    products["price"] = pd.to_numeric(products["price"], errors="coerce")
    missing_price = products["price"].isna().sum()
    metrics["products_missing_price_handled"] = int(missing_price)

    products["price"] = products.groupby("category")["price"].transform(lambda s: s.fillna(s.median()))
    overall_median = products["price"].median()
    if pd.isna(overall_median):
        overall_median = 0.00
    products["price"] = products["price"].fillna(overall_median).round(2)

    # Stock missing -> default 0
    products["stock_quantity"] = pd.to_numeric(products["stock_quantity"], errors="coerce")
    null_stock = products["stock_quantity"].isna().sum()
    metrics["products_null_stock_handled"] = int(null_stock)

    products["stock_quantity"] = products["stock_quantity"].fillna(0).clip(lower=0).astype(int)

    # Remove duplicates by product_id
    before = len(products)
    products = products.drop_duplicates(subset=["product_id"], keep="first")
    metrics["products_duplicates_removed"] = before - len(products)

    return products


def transform_sales(sales: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate transactions, standardize date/status, handle missing IDs."""
    sales = sales.copy()

    # Standardize date
    sales["transaction_date"] = sales["transaction_date"].apply(parse_date_to_yyyy_mm_dd)

    # Status standardization
    sales["status"] = sales["status"].astype(str).str.strip().str.title()
    sales.loc[sales["status"].isin(["Nan", "None"]), "status"] = "Pending"

    # Numeric conversions
    sales["quantity"] = pd.to_numeric(sales["quantity"], errors="coerce").fillna(0).astype(int)
    sales["unit_price"] = pd.to_numeric(sales["unit_price"], errors="coerce").fillna(0.0)

    # Duplicates (T001 duplicated)
    before = len(sales)
    sales = sales.drop_duplicates(subset=["transaction_id"], keep="first")
    metrics["sales_duplicates_removed"] = before - len(sales)

    # Missing IDs count (schema has NOT NULL FKs in orders/order_items)
    metrics["sales_missing_customer_id"] = int(sales["customer_id"].isna().sum())
    metrics["sales_missing_product_id"] = int(sales["product_id"].isna().sum())

    # Subtotal calculation
    sales["subtotal"] = (sales["quantity"] * sales["unit_price"]).round(2)

    return sales


# ----------------------------
# Load
# ----------------------------
def ensure_unknown_records(conn):
    """
    To satisfy NOT NULL + FK constraints in provided schema:
    - Create an Unknown Customer (unique email)
    - Create an Unknown Product (price NOT NULL)
    Returns their DB IDs.
    """
    conn.execute(text("""
        INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
        SELECT 'Unknown', 'Customer', 'unknown.customer@fleximart.local', NULL, NULL, NULL
        WHERE NOT EXISTS (SELECT 1 FROM customers WHERE email='unknown.customer@fleximart.local');
    """))
    unknown_customer_id = conn.execute(
        text("SELECT customer_id FROM customers WHERE email='unknown.customer@fleximart.local' LIMIT 1;")
    ).scalar()

    conn.execute(text("""
        INSERT INTO products (product_name, category, price, stock_quantity)
        SELECT 'Unknown Product', 'Electronics', 0.00, 0
        WHERE NOT EXISTS (
            SELECT 1 FROM products WHERE product_name='Unknown Product' AND category='Electronics'
        );
    """))
    unknown_product_id = conn.execute(
        text("SELECT product_id FROM products WHERE product_name='Unknown Product' AND category='Electronics' LIMIT 1;")
    ).scalar()

    return int(unknown_customer_id), int(unknown_product_id)


def load_to_db(engine, customers_clean, products_clean, sales_clean):
    """
    Load into provided schema tables:
    - customers, products (dimension-like)
    - orders, order_items (facts)
    Each sales transaction is treated as one order with one line item.
    """
    inserted_customers = 0
    inserted_products = 0
    inserted_orders = 0
    inserted_items = 0

    with engine.begin() as conn:
        unknown_customer_id, unknown_product_id = ensure_unknown_records(conn)

        # Map raw IDs -> DB auto-increment IDs
        customer_code_to_dbid = {}
        product_code_to_dbid = {}

        # ---- customers ----
        for _, r in customers_clean.iterrows():
            email = r["email"]

            existing = conn.execute(
                text("SELECT customer_id FROM customers WHERE email=:email LIMIT 1;"),
                {"email": email}
            ).scalar()

            if existing is None:
                conn.execute(text("""
                    INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
                    VALUES (:first_name, :last_name, :email, :phone, :city, :registration_date);
                """), {
                    "first_name": r["first_name"],
                    "last_name": r["last_name"],
                    "email": email,
                    "phone": r.get("phone"),
                    "city": r.get("city"),
                    "registration_date": r.get("registration_date")
                })
                inserted_customers += 1
                existing = conn.execute(
                    text("SELECT customer_id FROM customers WHERE email=:email LIMIT 1;"),
                    {"email": email}
                ).scalar()

            customer_code_to_dbid[r["customer_id"]] = int(existing)

        # ---- products ----
        for _, r in products_clean.iterrows():
            pname = r["product_name"]
            cat = r["category"]

            existing = conn.execute(text("""
                SELECT product_id FROM products
                WHERE product_name=:pname AND category=:cat
                LIMIT 1;
            """), {"pname": pname, "cat": cat}).scalar()

            if existing is None:
                conn.execute(text("""
                    INSERT INTO products (product_name, category, price, stock_quantity)
                    VALUES (:product_name, :category, :price, :stock_quantity);
                """), {
                    "product_name": pname,
                    "category": cat,
                    "price": float(r["price"]),
                    "stock_quantity": int(r["stock_quantity"])
                })
                inserted_products += 1
                existing = conn.execute(text("""
                    SELECT product_id FROM products
                    WHERE product_name=:pname AND category=:cat
                    LIMIT 1;
                """), {"pname": pname, "cat": cat}).scalar()

            product_code_to_dbid[r["product_id"]] = int(existing)

        # ---- orders + order_items ----
        for _, r in sales_clean.iterrows():
            raw_customer_code = r.get("customer_id")
            raw_product_code = r.get("product_id")

            db_customer_id = customer_code_to_dbid.get(raw_customer_code, unknown_customer_id)
            db_product_id = product_code_to_dbid.get(raw_product_code, unknown_product_id)

            order_date = r.get("transaction_date") or "1970-01-01"
            total_amount = float(r.get("subtotal") or 0.0)
            status = r.get("status") or "Pending"

            conn.execute(text("""
                INSERT INTO orders (customer_id, order_date, total_amount, status)
                VALUES (:customer_id, :order_date, :total_amount, :status);
            """), {
                "customer_id": db_customer_id,
                "order_date": order_date,
                "total_amount": total_amount,
                "status": status
            })
            inserted_orders += 1

            # Get order_id (MySQL). Fallback works for others.
            order_id = conn.execute(text("SELECT LAST_INSERT_ID();")).scalar()
            if order_id is None:
                order_id = conn.execute(text("SELECT MAX(order_id) FROM orders;")).scalar()
            order_id = int(order_id)

            qty = int(r.get("quantity") or 0)
            unit_price = float(r.get("unit_price") or 0.0)
            subtotal = float(r.get("subtotal") or (qty * unit_price))

            conn.execute(text("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (:order_id, :product_id, :quantity, :unit_price, :subtotal);
            """), {
                "order_id": order_id,
                "product_id": db_product_id,
                "quantity": qty,
                "unit_price": unit_price,
                "subtotal": subtotal
            })
            inserted_items += 1

    return inserted_customers, inserted_products, inserted_orders, inserted_items


# ----------------------------
# Report writer
# ----------------------------
def write_report():
    """Write required metrics to data_quality_report.txt."""
    logging.info("FLEXIMART DATA QUALITY REPORT")
    logging.info("=" * 40)
    logging.info("")

    logging.info("Customers Dataset")
    logging.info("-" * 20)
    logging.info(f"Raw records processed           : {metrics.get('customers_raw', 0)}")
    logging.info(f"Duplicate records removed       : {metrics.get('customers_duplicates_removed', 0)}")
    logging.info(f"Missing email values handled    : {metrics.get('customers_missing_email_handled', 0)}")
    logging.info(f"Records loaded successfully     : {metrics.get('customers_loaded', 0)}")
    logging.info("")

    logging.info("Products Dataset")
    logging.info("-" * 20)
    logging.info(f"Raw records processed           : {metrics.get('products_raw', 0)}")
    logging.info(f"Duplicate records removed       : {metrics.get('products_duplicates_removed', 0)}")
    logging.info(f"Missing price values handled    : {metrics.get('products_missing_price_handled', 0)}")
    logging.info(f"Null stock values handled       : {metrics.get('products_null_stock_handled', 0)}")
    logging.info(f"Records loaded successfully     : {metrics.get('products_loaded', 0)}")
    logging.info("")

    logging.info("Sales Dataset")
    logging.info("-" * 20)
    logging.info(f"Raw records processed           : {metrics.get('sales_raw', 0)}")
    logging.info(f"Duplicate records removed       : {metrics.get('sales_duplicates_removed', 0)}")
    logging.info(f"Missing customer IDs            : {metrics.get('sales_missing_customer_id', 0)} (mapped to Unknown Customer)")
    logging.info(f"Missing product IDs             : {metrics.get('sales_missing_product_id', 0)} (mapped to Unknown Product)")
    logging.info(f"Records loaded successfully     : {metrics.get('sales_loaded', 0)}")
    logging.info("")

    logging.info("-" * 40)
    logging.info("ETL PROCESS COMPLETED")
    logging.info("-" * 40)


# ----------------------------
# Main
# ----------------------------
def main():
    try:
        db_url = os.getenv("DB_URL")
        if not db_url:
            raise RuntimeError(
                "DB_URL not set.\n"
                "Example (MySQL): setx DB_URL \"mysql+pymysql://root:password@localhost:3306/fleximart\"\n"
                "Restart terminal after setting DB_URL."
            )

        engine = create_engine(db_url)

        # Extract
        customers_raw, products_raw, sales_raw = extract()

        # Transform
        customers_clean = transform_customers(customers_raw)
        products_clean = transform_products(products_raw)
        sales_clean = transform_sales(sales_raw)

        # Track "loaded" counts for report
        metrics["customers_loaded"] = len(customers_clean)
        metrics["products_loaded"] = len(products_clean)
        # sales_loaded means how many transactions will become orders/items
        metrics["sales_loaded"] = len(sales_clean)

        # Load
        ins_c, ins_p, ins_o, ins_oi = load_to_db(engine, customers_clean, products_clean, sales_clean)

        # (optional) track how many were newly inserted vs already existed
        metrics["customers_inserted_new"] = ins_c
        metrics["products_inserted_new"] = ins_p
        metrics["orders_inserted"] = ins_o
        metrics["order_items_inserted"] = ins_oi

        # Write report file
        write_report()

        print("✅ ETL completed successfully.")
        print(f"Customers processed: {metrics['customers_loaded']} | Products processed: {metrics['products_loaded']} | Sales processed: {metrics['sales_loaded']}")
        print(f"Orders inserted: {ins_o} | Order items inserted: {ins_oi}")
        print(f"Report generated at: {REPORT_PATH}")

    except Exception as e:
        # Required error handling
        logging.info("ETL FAILED")
        logging.info(f"Reason: {str(e)}")
        raise


if __name__ == "__main__":
    main()
