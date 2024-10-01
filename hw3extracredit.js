let num1, num2;

function generateQuestion() {
    num1 = Math.floor(Math.random() * 10);
    num2 = Math.floor(Math.random() * 10);
    document.getElementById('question').innerText = `How much is ${num1} times ${num2}?`;
    document.getElementById('resultMessage').innerText = ''; 
}

function checkAnswer() {
    const userAnswer = parseInt(document.getElementById('answer').value);
    const correctAnswer = num1 * num2;

    if (userAnswer === correctAnswer) {
        document.getElementById('resultMessage').innerText = "Very good!";
        document.getElementById('answer').value = '';

        const continuePlaying = confirm("Do you want to keep playing?");
        if (continuePlaying) {
            generateQuestion();
        } else {
            document.getElementById('resultMessage').innerText = "Thanks for playing, see you next time!";
            document.getElementById('answer').style.display = 'none'; 
            document.getElementById('submitAnswer').style.display = 'none'; 
        }
    } else {
        document.getElementById('resultMessage').innerText = "No. Please try again.";
    }
}

document.getElementById('submitAnswer').addEventListener('click', checkAnswer);
generateQuestion();
