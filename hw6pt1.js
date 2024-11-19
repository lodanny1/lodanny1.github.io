function processNumber() {
    const input = document.getElementById("numberInput").value.trim();
    const output = document.getElementById("output");

    if (isNaN(input) || !input.includes(".") || input.split(".")[1].length < 4) {
        output.innerHTML = "<p><strong>Error:</strong> You need to type a number with at least 4 decimals. Please try again.</p>";
        return;
    }

    const number = parseFloat(input);
    output.innerHTML = `
        <p><strong>You typed number:</strong> ${number}</p>
        <p><strong>Rounded to the nearest integer:</strong> ${Math.round(number)}</p>
        <p><strong>Square root rounded to integer:</strong> ${Math.round(Math.sqrt(number))}</p>
        <p><strong>Rounded to the nearest 10th position:</strong> ${number.toFixed(1)}</p>
        <p><strong>Rounded to the nearest 100th position:</strong> ${number.toFixed(2)}</p>
        <p><strong>Rounded to the nearest 1000th position:</strong> ${number.toFixed(3)}</p>
    `;
}

document.getElementById("clearButton").addEventListener("click", () => {
    document.getElementById("output").innerHTML = "";
});
