function validatePhone() {
    const phone = document.getElementById("phoneInput").value.trim();
    const output = document.getElementById("output");
    const regex = /^\(\d{3}\) \d{3}-\d{4}$/;

    if (regex.test(phone)) {
        output.innerHTML = `
            <p><strong>Thank you for providing your phone number:</strong> ${phone}</p>
            <p><strong>An agent will contact you soon.</strong></p>
        `;
    } else {
        output.innerHTML = `
            <p><strong>Error:</strong> Please enter your phone number in the format (999) 999-9999.</p>
        `;
    }
}

document.getElementById("clearButton").addEventListener("click", () => {
    document.getElementById("output").innerHTML = "";
});
