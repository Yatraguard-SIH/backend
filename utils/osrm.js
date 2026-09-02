const axios = require('axios');

const TARIFF_PER_KM = process.env.TARIFF_PER_KM || 15;
const BASE_FARE = process.env.BASE_FARE || 50;
const SURCHARGE_MULTIPLIER = 1.33;

const calculateFare = async (source_lat, source_lng, destination_lat, destination_lng) => {
    try {
        const url = `http://router.project-osrm.org/route/v1/driving/${source_lng},${source_lat};${destination_lng},${destination_lat}?overview=full`;
        const response = await axios.get(url);

        if (!response.data || response.data.code !== 'Ok') {
            throw new Error('OSRM API Error');
        }

        const route = response.data.routes[0];
        const distanceKm = route.distance / 1000;
        const durationMin = route.duration / 60;
        const polyline = route.geometry;

        const baseFare = BASE_FARE + (distanceKm * TARIFF_PER_KM);
        const min_fare = Math.round(baseFare);
        const max_fare = Math.round(baseFare * SURCHARGE_MULTIPLIER);

        return { min_fare, max_fare, distance: distanceKm, duration: durationMin, polyline };
    } catch (error) {
        console.error('Error in calculateFare:', error.message);
        throw error;
    }
};

module.exports = { calculateFare };

// Example: calculateFare(28.6139, 77.2090, 28.5355, 77.3910).then(console.log);

