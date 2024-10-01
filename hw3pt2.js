document.getElementById('calculate').addEventListener('click', function() {
    const prices = [20.99, 12.75, 9.95, 35.89];
    let totalSales = 0;
    let hasError = false;
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.innerText = ''; // Clear previous error messages

    const quantities = [
        document.getElementById('item1Qty').value,
        document.getElementById('item2Qty').value,
        document.getElementById('item3Qty').value,
        document.getElementById('item4Qty').value
    ];

    // Loop through quantities and validate input
    for (let i = 0; i < quantities.length; i++) {
        const qty = quantities[i];

        // Check if input is a valid number
        if (isNaN(qty) || qty.trim() === '') {
            errorMessage.innerText = 'Please enter valid numbers for all quantities.';
            hasError = true;
            break;
        }

        // Check if number is negative
        if (qty < 0) {
            errorMessage.innerText = 'Quantities cannot be negative. Please enter non-negative numbers.';
            hasError = true;
            break;
        }

        const qtySold = parseInt(qty);
        const totalItemSales = qtySold * prices[i];

        document.getElementById(`item${i + 1}Sold`).value = qtySold;
        document.getElementById(`item${i + 1}Total`).value = totalItemSales.toFixed(2);
        totalSales += totalItemSales;
    }

    if (!hasError) {
        // Calculate total earnings if no error found
        const baseSalary = 250;
        const commissionRate = 0.09;
        const weeklyEarnings = baseSalary + (totalSales * commissionRate);

        document.getElementById('totalSold').innerText = `$${totalSales.toFixed(2)}`;
        document.getElementById('weeklyEarnings').innerText = `$${weeklyEarnings.toFixed(2)}`;
    } else {
        // Clear total fields if there are input errors
        for (let i = 1; i <= 4; i++) {
            document.getElementById(`item${i}Sold`).value = '';
            document.getElementById(`item${i}Total`).value = '';
        }
        document.getElementById('totalSold').innerText = '';
        document.getElementById('weeklyEarnings').innerText = '';
    }
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
    document.getElementById('errorMessage').innerText = ''; // Clear error messages
});
