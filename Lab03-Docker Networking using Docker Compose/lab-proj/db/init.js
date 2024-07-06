// MongoDB Initialization Script

// Sample data
var sampleData = [
  { "brand": "Apple", "model": "MacBook Pro", "price": 2000 },
  { "brand": "Dell", "model": "XPS 15", "price": 1800 },
  { "brand": "Lenovo", "model": "ThinkPad X1 Carbon", "price": 2200 },
  { "brand": "HP", "model": "Spectre x360", "price": 1600 },
  { "brand": "Microsoft", "model": "Surface Laptop 4", "price": 1500 },
  { "brand": "Asus", "model": "ZenBook 14", "price": 1300 },
  { "brand": "Acer", "model": "Swift 5", "price": 1100 },
  { "brand": "Samsung", "model": "Galaxy Book Pro", "price": 1900 },
  { "brand": "Google", "model": "Pixelbook Go", "price": 1400 },
  { "brand": "Razer", "model": "Blade 15", "price": 2500 }
];

// Connect to the database
var conn = new Mongo();
var db = conn.getDB('mydatabase');

// Insert sample data into a collection
db.laptops.insertMany(sampleData);

