const express = require('express');
const { MongoClient } = require('mongodb');

const app = express();
const PORT = process.env.PORT || 3000;
const MONGODB_URI = 'mongodb://mongodb:27017/mydatabase'; // MongoDB URI

app.use(express.json()); // Parse JSON bodies
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded bodies

// Connect to MongoDB
MongoClient.connect(MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(client => {
    console.log('Connected to MongoDB');
    const db = client.db();

// Define routes
app.get('/', (req, res) => {
  console.log('Received request for /');
  res.send('Hello, Dockerized Node.js App!');
});

// Get data from MongoDB
app.get('/data', async (req, res) => {
  try {
    console.log('Received request for /data');
    
    // Ensure that the MongoDB connection is established
    if (!db) {
      console.error('MongoDB connection is not established');
      return res.status(500).send('Internal Server Error');
    }
    
    // Fetch data from MongoDB
    const data = await db.collection('laptops').find().toArray();
    
    console.log('Data fetched successfully:', data);
    
    // Send the fetched data as a JSON response
    res.json(data);
  } catch (error) {
    console.error('Error fetching data:', error);
    res.status(500).send('Internal Server Error');
  }
});

    // Add new data to MongoDB
    app.post('/data', async (req, res) => {
      try {
        // Assuming req.body contains the new data object
        const newData = req.body;
        const result = await db.collection('laptops').insertOne(newData);
        res.status(201).json(result.ops);
      } catch (error) {
        console.error('Error adding data:', error);
        res.status(500).send('Internal Server Error');
      }
    });

    // Update data in MongoDB
    app.put('/data/:id', async (req, res) => {
      try {
        const id = req.params.id;
        const newData = req.body;
        const result = await db.collection('laptops').updateOne({ _id: id }, { $set: newData });
        res.json(result);
      } catch (error) {
        console.error('Error updating data:', error);
        res.status(500).send('Internal Server Error');
      }
    });

    // Delete data from MongoDB
    app.delete('/data/:id', async (req, res) => {
      try {
        const id = req.params.id;
        const result = await db.collection('laptops').deleteOne({ _id: id });
        res.json(result);
      } catch (error) {
        console.error('Error deleting data:', error);
        res.status(500).send('Internal Server Error');
      }
    });

    // Start the server
    app.listen(PORT, () => {
      console.log(`Server is running on port ${PORT}`);
    });
  })
  .catch(error => {
    console.error('Error connecting to MongoDB:', error);
    process.exit(1); // Exit the process if unable to connect to MongoDB
  });

