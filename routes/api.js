const express = require('express');
const router = express.Router();

const { calculateFare } = require('../utils/osrm');
const { splitBudget } = require('../utils/budget');
const { generateOTP, verifyOTP } = require('../utils/otp');

// Fare calculation route
router.post('/fare', async (req, res) => {
    try {
        const { source_lat, source_lng, destination_lat, destination_lng } = req.body;
        
        if (!source_lat || !source_lng || !destination_lat || !destination_lng) {
            return res.status(400).json({ error: 'Missing coordinates' });
        }
        
        const fareData = await calculateFare(source_lat, source_lng, destination_lat, destination_lng);
        res.json(fareData);
    } catch (error) {
        res.status(500).json({ error: 'Failed to calculate fare' });
    }
});

// Budget split route
router.post('/budget', (req, res) => {
    try {
        const { budget } = req.body;
        
        if (typeof budget !== 'number' || budget < 0) {
            return res.status(400).json({ error: 'Invalid budget provided' });
        }
        
        const split = splitBudget(budget);
        res.json(split);
    } catch (error) {
        res.status(500).json({ error: 'Failed to split budget' });
    }
});

// Generate OTP route
router.post('/auth/generate-otp', async (req, res) => {
    try {
        const { phone } = req.body;
        
        if (!phone) {
            return res.status(400).json({ error: 'Phone number is required' });
        }
        
        const result = await generateOTP(phone);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: 'Failed to generate OTP' });
    }
});

// Verify OTP route
router.post('/auth/verify-otp', async (req, res) => {
    try {
        const { phone, otp } = req.body;
        
        if (!phone || !otp) {
            return res.status(400).json({ error: 'Phone and OTP are required' });
        }
        
        const isValid = await verifyOTP(phone, otp);
        if (isValid) {
            res.json({ success: true, message: 'OTP verified successfully' });
        } else {
            res.status(400).json({ success: false, error: 'Invalid or expired OTP' });
        }
    } catch (error) {
        res.status(500).json({ error: 'Failed to verify OTP' });
    }
});

module.exports = router;

