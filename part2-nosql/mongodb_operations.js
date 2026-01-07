
use("fleximart_nosql");

db.products.drop();

const productsData = JSON.parse(cat("part2-nosql/products_catalog.json"));
db.products.insertMany(productsData);

print("\n✅ Operation 1: Data loaded into 'products' collection");
print("Total documents in products:", db.products.countDocuments());

db.products.createIndex({ product_id: 1 }, { unique: true });


print("\n✅ Operation 2: Electronics products with price < 50000 (name, price, stock)");

db.products.find(
  { category: "Electronics", price: { $lt: 50000 } },
  { _id: 0, name: 1, price: 1, stock: 1 }
).sort({ price: 1 });


print("\n✅ Operation 3: Products with average rating >= 4.0");

db.products.aggregate([
  {
    $addFields: {
      avgRating: { $avg: "$reviews.rating" }
    }
  },
  {
    $match: {
      avgRating: { $gte: 4.0 }
    }
  },
  {
    $project: {
      _id: 0,
      product_id: 1,
      name: 1,
      category: 1,
      avgRating: { $round: ["$avgRating", 2] }
    }
  },
  // Highest rated first
  { $sort: { avgRating: -1 } }
]);


print("\n✅ Operation 4: Add review to ELEC001");

db.products.updateOne(
  { product_id: "ELEC001" },
  {
    $push: {
      reviews: {
        user_id: "U999",
        username: "U999",
        rating: 4,
        comment: "Good value",
        date: new Date() // ISODate() in mongosh
      }
    },
    $set: { updated_at: new Date().toISOString() }
  }
);

print("Updated ELEC001 (show last review only):");
db.products.find(
  { product_id: "ELEC001" },
  { _id: 0, product_id: 1, name: 1, last_review: { $slice: ["$reviews", -1] } }
);


print("\n✅ Operation 5: Average price by category (sorted desc)");

db.products.aggregate([
  {
    $group: {
      _id: "$category",
      avg_price: { $avg: "$price" },
      product_count: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      category: "$_id",
      avg_price: { $round: ["$avg_price", 2] },
      product_count: 1
    }
  },
  { $sort: { avg_price: -1 } }
]);

print("\n✅ All operations completed.");
