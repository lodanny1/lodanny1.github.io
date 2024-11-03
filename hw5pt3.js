const statesData = [
    ["AL", "Alabama", "Montgomery", 4903185],
    ["AK", "Alaska", "Juneau", 731545],
    ["AZ", "Arizona", "Phoenix", 7278717],
    ["AR", "Arkansas", "Little Rock", 3017825],
    ["CA", "California", "Sacramento", 39512223],
    ["CO", "Colorado", "Denver", 5758736]
];

function lookupState() {
    const input = document.getElementById("stateInput").value.trim().toLowerCase();
    const output = document.getElementById("output");

    output.innerHTML = "";

    if (!input) {
        output.innerHTML = "Please enter a state name or abbreviation.";
        return;
    }

    const state = statesData.find(([abbr, name]) =>
        abbr.toLowerCase() === input || name.toLowerCase() === input
    );

    if (state) {
        const [abbr, name, capital, population] = state;
        output.innerHTML = `
            <p>Thank you for your inquiry. Here is the information you requested:</p>
            <p><strong>State Abbr:</strong> ${abbr}<br>
               <strong>State Name:</strong> ${name}<br>
               <strong>Capital:</strong> ${capital}<br>
               <strong>Population:</strong> ${population.toLocaleString()}</p>
        `;
    } else {
        output.innerHTML = `
            <p>Sorry, we do not have information about this state. We only have information about ${statesData.map(([abbr]) => abbr).join(", ")}.</p>
        `;
    }
}

document.getElementById("clearButton").addEventListener("click", () => {
    document.getElementById("output").innerHTML = "";
});
