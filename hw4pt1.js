let sum1 = 0;
let product1 = 1;

for (let i = 5; i <= 25; i += 4) {
    sum1 += i;
    product1 *= i;
}

document.getElementById("result1").innerHTML = `
    <p>The result of 5 * 9 * 13 * 17 * 21 * 25 is ${product1.toLocaleString()}.</p>
    <p>The result of 5 + 9 + 13 + 17 + 21 + 25 is ${sum1.toLocaleString()}.</p>
`;

let sum2 = 0;
let product2 = 1;
let j = 3;

while (j <= 18) {
    sum2 += j;
    product2 *= j;
    j += 3;
}

document.getElementById("result2").innerHTML = `
    <p>The result of 3 * 6 * 9 * 12 * 15 * 18 is ${product2.toLocaleString()}.</p>
    <p>The result of 3 + 6 + 9 + 12 + 15 + 18 is ${sum2.toLocaleString()}.</p>
`;
