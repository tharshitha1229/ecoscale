const mongoose = require('mongoose');

const historySchema = new mongoose.Schema({
    username: { type: String, required: true }, // To identify which classmate did the test
    device: { type: String, required: true },
    mobile: { type: String, required: true },
    coding_hours: { type: Number, required: true },
    streaming_hours: { type: Number, required: true },
    heavy_hours: { type: Number, required: true },
    total_emission: { type: Number, required: true },
    operational_emission: { type: Number },
    embodied_emission: { type: Number },
    pue: { type: Number },
    energy_kwh: { type: Number },
    timestamp: { type: Date, default: Date.now }
});

module.exports = mongoose.model('History', historySchema);