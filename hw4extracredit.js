function generateSquare() {
    let num = parseInt(document.getElementById("numberInput").value);
    let resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "";

    if (isNaN(num) || num < 2 || num > 10) {
        resultDiv.innerHTML = "<p>Please enter a valid number between 2 and 10.</p>";
        return;
    }

    let square = "";
    for (let i = 0; i < num; i++) {
        if (i === 0 || i === num - 1) {
            square += "* ".repeat(num) + "<br>";
        } else {
            square += "* " + "&nbsp;".repeat((num - 2) * 2) + "*<br>";
        }
    }

    resultDiv.innerHTML = `<pre>${square}</pre>`;
}
