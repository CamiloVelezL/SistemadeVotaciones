// URLs de la API
const API_BASE = '/api';

// Elementos del DOM
const candidateForm = document.getElementById('candidateForm');
const voterForm = document.getElementById('voterForm');
const messageDiv = document.getElementById('message');

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', function() {
    loadCandidates();
    loadVoters();
    loadStats();
    
    // Event listeners para formularios
    candidateForm.addEventListener('submit', handleCandidateSubmit);
    voterForm.addEventListener('submit', handleVoterSubmit);
});

// Manejar envío de formulario de candidato
async function handleCandidateSubmit(e) {
    e.preventDefault();
    
    const name = document.getElementById('candidateName').value;
    const party = document.getElementById('candidateParty').value;
    
    try {
        const response = await fetch(`${API_BASE}/candidates`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, party })
        });
        
        if (response.ok) {
            showMessage('Candidato agregado exitosamente', 'success');
            candidateForm.reset();
            loadCandidates();
            loadStats();
        } else {
            const error = await response.json();
            showMessage(`Error: ${error.error}`, 'error');
        }
    } catch (error) {
        showMessage('Error de conexión', 'error');
    }
}

// Manejar envío de formulario de votante
async function handleVoterSubmit(e) {
    e.preventDefault();
    
    const name = document.getElementById('voterName').value;
    const email = document.getElementById('voterEmail').value;
    
    try {
        const response = await fetch(`${API_BASE}/voters`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email })
        });
        
        if (response.ok) {
            showMessage('Votante registrado exitosamente', 'success');
            voterForm.reset();
            loadVoters();
            loadStats();
        } else {
            const error = await response.json();
            showMessage(`Error: ${error.error}`, 'error');
        }
    } catch (error) {
        showMessage('Error de conexión', 'error');
    }
}

// Cargar lista de candidatos - VERSIÓN ACTUALIZADA CON BOTÓN ELIMINAR
async function loadCandidates() {
    const container = document.getElementById('candidatesList');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Cargando candidatos...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/candidates`);
        const candidates = await response.json();
        
        if (candidates.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-users"></i>
                    <p>No hay candidatos registrados</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = candidates.map(candidate => `
            <div class="list-item">
                <div class="list-item-info">
                    <h4>${candidate.name}</h4>
                    <p>${candidate.party || 'Sin partido'}</p>
                </div>
                <div class="list-item-actions">
                    <button class="btn btn-danger" onclick="deleteCandidate(${candidate.id})">
                        <i class="fas fa-trash"></i> Eliminar
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = '<div class="error">Error al cargar candidatos</div>';
    }
}

// Eliminar candidato
async function deleteCandidate(candidateId) {
    if (!confirm('¿Está seguro de que desea eliminar este candidato?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/candidates/${candidateId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showMessage('Candidato eliminado exitosamente', 'success');
            loadCandidates();
            loadStats();
        } else {
            const error = await response.json();
            showMessage(`Error: ${error.error}`, 'error');
        }
    } catch (error) {
        showMessage('Error de conexión', 'error');
    }
}

// Cargar lista de votantes
async function loadVoters() {
    const container = document.getElementById('votersList');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Cargando votantes...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/voters`);
        const voters = await response.json();
        
        if (voters.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-user-friends"></i>
                    <p>No hay votantes registrados</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = voters.map(voter => `
            <div class="list-item">
                <div class="list-item-info">
                    <h4>${voter.name}</h4>
                    <p>${voter.email} - ${voter.has_voted ? 'Ya votó' : 'No ha votado'}</p>
                </div>
                <div class="list-item-actions">
                    ${!voter.has_voted ? 
                        `<button class="btn btn-danger" onclick="deleteVoter(${voter.id})">
                            <i class="fas fa-trash"></i> Eliminar
                        </button>` : 
                        '<small>No se puede eliminar</small>'
                    }
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = '<div class="error">Error al cargar votantes</div>';
    }
}

// Eliminar votante
async function deleteVoter(voterId) {
    if (!confirm('¿Está seguro de que desea eliminar este votante?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/voters/${voterId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showMessage('Votante eliminado exitosamente', 'success');
            loadVoters();
            loadStats();
        } else {
            const error = await response.json();
            showMessage(`Error: ${error.error}`, 'error');
        }
    } catch (error) {
        showMessage('Error de conexión', 'error');
    }
}

// Cargar estadísticas
async function loadStats() {
    try {
        const [candidatesResponse, votersResponse] = await Promise.all([
            fetch(`${API_BASE}/candidates`),
            fetch(`${API_BASE}/voters`)
        ]);
        
        const candidates = await candidatesResponse.json();
        const voters = await votersResponse.json();
        
        const votedCount = voters.filter(voter => voter.has_voted).length;
        
        document.getElementById('totalCandidates').textContent = candidates.length;
        document.getElementById('totalVoters').textContent = voters.length;
        document.getElementById('votedCount').textContent = votedCount;
    } catch (error) {
        console.error('Error cargando estadísticas:', error);
    }
}

// Mostrar mensajes al usuario
function showMessage(text, type) {
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.classList.remove('hidden');
    
    setTimeout(() => {
        messageDiv.classList.add('hidden');
    }, 5000);
}