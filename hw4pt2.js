function calculateCompoundInterest(principal, rate, years) {
    let result = [];
    for (let year = 1; year <= years; year++) {
        let amount = principal * Math.pow(1 + rate, year);
        result.push({ year, amount: amount.toFixed(2), rate: (rate * 100).toFixed(2) });
    }
    return result;
}

function generateTable(rate) {
    let rows = calculateCompoundInterest(1000, rate, 5);
    let table = `<table>
        <thead>
            <tr><th>Year</th><th>Amount on Deposit</th><th>Interest Rate</th></tr>
        </thead>
        <tbody>`;
    
    rows.forEach((row, index) => {
        table += `<tr${index % 2 === 0 ? ' class="even-row"' : ''}>
            <td>${row.year}</td>
            <td>${row.amount}</td>
            <td>${row.rate}%</td>
        </tr>`;
    });
    
    table += `</tbody></table>`;
    return table;
}

let tablesDiv = document.getElementById("tables");
let interestRates = [0.05, 0.06, 0.07]; 

interestRates.forEach(rate => {
    tablesDiv.innerHTML += `<h2>Interest Rate: ${(rate * 100).toFixed(2)}%</h2>`;
    tablesDiv.innerHTML += generateTable(rate);
});
