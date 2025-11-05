// Utilitários JavaScript gerais

// Função para formatar datas
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

// Função para mostrar mensagens de sucesso/erro
function showMessage(message, type = 'success') {
    const messageEl = document.createElement('div');
    messageEl.className = `message message-${type}`;
    messageEl.textContent = message;
    messageEl.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 2rem;
        background: ${type === 'success' ? '#10b981' : '#ef4444'};
        color: white;
        border-radius: 0.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideIn 0.3s;
    `;
    
    document.body.appendChild(messageEl);
    
    setTimeout(() => {
        messageEl.style.animation = 'slideOut 0.3s';
        setTimeout(() => messageEl.remove(), 300);
    }, 3000);
}

// Atualização automática de estatísticas (opcional)
if (window.location.pathname === '/') {
    setInterval(() => {
        fetch('/api/stats')
            .then(r => r.json())
            .then(stats => {
                // Atualizar estatísticas no dashboard se necessário
                console.log('Stats updated:', stats);
            });
    }, 30000); // A cada 30 segundos
}
