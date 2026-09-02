const twilio = require('twilio');

const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;
const twilioPhone = process.env.TWILIO_PHONE_NUMBER;
const client = accountSid && authToken ? twilio(accountSid, authToken) : null;

const otpStore = new Map();

const generateOTP = async (phone) => {
    try {
        const otp = Math.floor(100000 + Math.random() * 900000).toString();
        const expiresAt = Date.now() + 10 * 60 * 1000; // 10 minutes
        
        otpStore.set(phone, { otp, expiresAt });
        
        if (client) {
            await client.messages.create({
                body: `Your OTP is ${otp}. Valid for 10 minutes.`,
                from: twilioPhone,
                to: phone
            });
        }
        
        return { success: true, message: 'OTP sent' };
    } catch (error) {
        console.error('Error generating OTP:', error.message);
        throw error;
    }
};

const verifyOTP = async (phone, otp) => {
    try {
        const stored = otpStore.get(phone);
        
        if (!stored) return false;
        if (Date.now() > stored.expiresAt) {
            otpStore.delete(phone);
            return false;
        }
        
        if (stored.otp === otp) {
            otpStore.delete(phone);
            return true;
        }
        
        return false;
    } catch (error) {
        console.error('Error verifying OTP:', error.message);
        throw error;
    }
};

module.exports = { generateOTP, verifyOTP };

// Example: generateOTP('+1234567890').then(() => verifyOTP('+1234567890', '123456').then(console.log));

