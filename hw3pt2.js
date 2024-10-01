document.getElementById('calculate').addEventListener('click', function() {
    const prices = [20.99, 12.75, 9.95, 35.89];
    let totalSales = 0;

    const quantities = [
        parseInt(document.getElementById('item1Qty').value) || 0,
        parseInt(document.getElementById('item2Qty').value) || 0,
        parseInt(document.getElementById('item3Qty').value) || 0,
        parseInt(document.getElementById('item4Qty').value) || 0
    ];

    for (let i = 0; i < prices.length; i++) {
        const qtySold = quantities[i];
        const totalItemSales = qtySold * prices[i];

        document.getElementById(`item${i + 1}Sold`).value = qtySold;
        document.getElementById(`item${i + 1}Total`).value = totalItemSales.toFixed(2); 
        totalSales += totalItemSales;
    }

    const baseSalary = 250;
    const commissionRate = 0.09;
    const weeklyEarnings = baseSalary + (totalSales * commissionRate);

    document.getElementById('totalSold').innerText = `$${totalSales.toFixed(2)}`; 
    document.getElementById('weeklyEarnings').innerText = `$${weeklyEarnings.toFixed(2)}`; 
});


document.getElementById('clearForm').addEventListener('click', function() {
    document.getElementById('sellerName').value = '';
    document.getElementById('item1Qty').value = '';
    document.getElementById('item2Qty').value = '';
    document.getElementById('item3Qty').value = '';
    document.getElementById('item4Qty').value = '';
    
    for (let i = 1; i <= 4; i++) {
        document.getElementById(`item${i}Sold`).value = '';
        document.getElementById(`item${i}Total`).value = '';
    }

    document.getElementById('totalSold').innerText = '';
    document.getElementById('weeklyEarnings').innerText = '';
});
