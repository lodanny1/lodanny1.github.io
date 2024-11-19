function searchCharacter() {
    const text = document.getElementById("textInput").value.toLowerCase();
    const char = document.getElementById("charInput").value.toLowerCase();
    const output = document.getElementById("output");

    if (char.length === 0) return;

    const count = (text.split(char).length - 1);

    if (count > 0) {
        output.innerHTML = `
            <p><strong>The character "${char}" shows up:</strong> ${count} times.</p>
        `;
    } else {
        const newWindow = window.open("", "", "width=300,height=100");
        newWindow.document.write(`
            <p style="font-family: Arial, sans-serif; text-align: center; margin: 10px 0;">
                Search character "${char}" not found in the content you typed.
            </p>
            <div style="text-align: center;">
                <button onclick="window.close()" style="padding: 5px 10px; font-size: 14px; margin-top: -5px;">
                    Close
                </button>
            </div>
        `);
        output.innerHTML = "";
    }
}

document.getElementById("clearButton").addEventListener("click", () => {
    document.getElementById("output").innerHTML = "";
});

