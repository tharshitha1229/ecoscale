const crypto = require('crypto');
if (!globalThis.crypto) {
    globalThis.crypto = crypto;
}
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const History = require('./models/History');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Database Connection
mongoose.connect(process.env.MONGO_URI)
    .then(() => console.log('✅ Connected to MongoDB Atlas successfully!'))
    .catch((err) => console.error('❌ MongoDB connection error:', err));

// --- API ROUTES ---

// 1. Route to save a new carbon calculation
app.post('/api/history', async (req, res) => {
    try {
        const newRecord = new History(req.body);
        const savedRecord = await newRecord.save();
        res.status(201).json({ message: 'Record saved successfully', data: savedRecord });
    } catch (error) {
        console.error('❌ MONGO DB SAVE ERROR:', error.message); // <-- THIS WILL EXPOSE THE BUG
        res.status(500).json({ error: 'Failed to save record' });
    }
});

// 2. Route to get all past calculations
app.get('/api/history/:username', async (req, res) => {
    try {
        const userHistory = await History.find({ username: req.params.username }).sort({ timestamp: -1 });
        res.status(200).json(userHistory);
    } catch (error) {
        res.status(500).json({ error: 'Failed to retrieve history' });
    }
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`🚀 EcoScale Backend API running on http://localhost:${PORT}`);
});