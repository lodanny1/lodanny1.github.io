function validateForm() {
    const fullName = document.getElementById("fullName").value.trim();
    const ageGroup = document.querySelector('input[name="ageGroup"]:checked');
    const browsers = document.querySelectorAll('input[name="browser"]:checked');
    const movieGenre = document.getElementById("movieGenre").value;
    const output = document.getElementById("output");

    output.innerHTML = "";

    let errors = [];

    if (!fullName) {
        errors.push("Please enter your full name.");
    }
    if (!ageGroup) {
        errors.push("Please select your age group.");
    }
    if (browsers.length === 0) {
        errors.push("Please select at least one browser you have used.");
    }
    if (!movieGenre) {
        errors.push("Please select your favorite movie genre.");
    }

    if (errors.length > 0) {
        output.innerHTML = errors.join("<br>");
    } else {
        const ageGroupText = ageGroup.nextElementSibling.innerText;
        const browserText = Array.from(browsers).map(browser => browser.nextElementSibling.innerText).join(", ");

        output.innerHTML = `
            <p>Thank you for your submission!</p>
            <p><strong>Full Name:</strong> ${fullName}</p>
            <p><strong>Age Group:</strong> ${ageGroupText}</p>
            <p><strong>Browsers Used:</strong> ${browserText}</p>
            <p><strong>Favorite Movie Genre:</strong> ${movieGenre}</p>
        `;
    }
}

document.getElementById("clearButton").addEventListener("click", () => {
    document.getElementById("output").innerHTML = "";
});
