const output = document.getElementById('output');
const statusLabel = document.getElementById('status');
const reloadButton = document.getElementById('reload');

function render(message, isError = false) {
    output.textContent = message;
    statusLabel.textContent = isError ? 'Falha ao consumir a API' : 'API respondendo normalmente';
    statusLabel.style.color = isError ? '#b91c1c' : '#166534';
}

async function loadHealth() {
    render('Carregando...');

    try {
        const response = await fetch('/api/health', {
            headers: {
                Accept: 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        render(JSON.stringify({ endpoint: '/api/health', ...data }, null, 2));
    } catch (error) {
        render(`Erro ao consumir a API: ${error.message}`, true);
    }
}

reloadButton.addEventListener('click', loadHealth);
window.addEventListener('DOMContentLoaded', loadHealth);

