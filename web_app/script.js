document.getElementById('calculateButton').addEventListener('click', function() {
    const expression = document.getElementById('expression').value;

    fetch('http://localhost:8000/calculate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ expression: expression })
    })
    .then(response => response.json())
    .then(data => {
        if (data.result !== undefined) {
            document.getElementById('result').innerText = `Result: ${data.result}`;
            fetchExpressions();
        } else {
            document.getElementById('result').innerText = `Error: ${data.detail}`;
        }
    })
    .catch(error => {
        document.getElementById('result').innerText = `Error: ${error.message}`;
    });
});

document.getElementById('downloadCsvButton').addEventListener('click', function() {
    window.location.href = 'http://localhost:8000/export_csv/';
});

function appendToExpression(value) {
    const expressionInput = document.getElementById('expression');
    expressionInput.value += value;
}

function clearExpression() {
    document.getElementById('expression').value = '';
}

function backspace() {
    const expressionInput = document.getElementById('expression');
    expressionInput.value = expressionInput.value.slice(0, -1);
}

function fetchExpressions() {
    fetch('http://localhost:8000/expressions/')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('expressionsTable').querySelector('tbody');
            tbody.innerHTML = '';
            data.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.id}</td>
                    <td>${item.expression}</td>
                    <td>${item.result}</td>
                `;
                tbody.appendChild(row);
            });
        });
}

fetchExpressions();
