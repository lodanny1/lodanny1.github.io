document.getElementById('gradesForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const hwAvg = parseInt(document.getElementById('hwAvg').value);
    const midExam = parseInt(document.getElementById('midExam').value);
    const finalExam = parseInt(document.getElementById('finalExam').value);
    const participation = parseInt(document.getElementById('participation').value);
    
    const inputs = [hwAvg, midExam, finalExam, participation];
    
    if (inputs.every(num => num >= 0 && num <= 100)) {
        const finalAverage = Math.round((0.5 * hwAvg) + (0.2 * midExam) + (0.2 * finalExam) + (0.1 * participation));
        let letterGrade = '';
        
        if (finalAverage >= 90) {
            letterGrade = 'A';
        } else if (finalAverage >= 80) {
            letterGrade = 'B';
        } else if (finalAverage >= 70) {
            letterGrade = 'C';
        } else if (finalAverage >= 60) {
            letterGrade = 'D';
        } else {
            letterGrade = 'F';
        }

        let resultMessage = `Final Average: ${finalAverage}, Letter Grade: ${letterGrade}`;
        if (letterGrade === 'D' || letterGrade === 'F') {
            resultMessage += " - Student must retake the course.";
        }
        document.getElementById('result').innerText = resultMessage;
    } else {
        document.getElementById('result').innerText = "Error: Please enter valid grades (0-100).";
    }
});

document.getElementById('clearBtn').addEventListener('click', function() {
    document.getElementById('gradesForm').reset();
    document.getElementById('result').innerText = '';
});
