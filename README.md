# Trip Planner Backend

Hey team! I have set up the backend for our SIH trip planner app. It is built with Node.js and Express. Here is a simple breakdown of what is done and how to use it.

## What's included?

I created 3 main features:
1. **Fare Calculation**: Calculates the distance, time, and estimated trip fare using the OSRM routing API.
2. **Budget Splitter**: Automatically splits a user's total trip budget using the standard 50/30/20 rule (50% Needs, 30% Wants, 20% Savings).
3. **OTP Authentication**: Generates and verifies 6-digit OTPs via SMS using Twilio.

## How to run the project

1. Clone or pull this code.
2. Run `npm install` to download the packages.
3. Create a `.env` file in the main folder (you can copy `.env.example`) and add our Twilio keys and Fare config.
4. Run `node index.js` to start the server. It will run on port 3000 by default.

## API Endpoints Available

All endpoints start with `http://localhost:3000/api`.

### 1. Calculate Fare
- **URL**: `POST /fare`
- **What it does**: Takes the starting and ending locations and returns the route distance, time, and estimated fare (min & max).
- **Send this JSON**:
  ```json
  {
    "source_lat": 28.6139,
    "source_lng": 77.2090,
    "destination_lat": 28.5355,
    "destination_lng": 77.3910
  }
  ```

### 2. Split Budget
- **URL**: `POST /budget`
- **What it does**: Takes a total budget amount and splits it.
- **Send this JSON**:
  ```json
  {
    "budget": 10000
  }
  ```

### 3. Generate OTP
- **URL**: `POST /auth/generate-otp`
- **What it does**: Sends a 6-digit OTP to the user's phone number.
- **Send this JSON**:
  ```json
  {
    "phone": "+919876543210"
  }
  ```

### 4. Verify OTP
- **URL**: `POST /auth/verify-otp`
- **What it does**: Checks if the OTP entered by the user is correct and valid (expires in 10 mins).
- **Send this JSON**:
  ```json
  {
    "phone": "+919876543210",
    "otp": "123456"
  }
  ```

Let me know if you guys need any changes or new endpoints added!

