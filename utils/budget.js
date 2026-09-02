const splitBudget = (total_budget) => {
    if (typeof total_budget !== 'number' || total_budget < 0) {
        throw new Error('Invalid budget amount');
    }
    
    return {
        needs: total_budget * 0.50,
        wants: total_budget * 0.30,
        savings: total_budget * 0.20
    };
};

module.exports = { splitBudget };

// Example: console.log(splitBudget(10000));

