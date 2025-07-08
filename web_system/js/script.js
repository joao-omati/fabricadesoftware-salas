// Sistema de Reserva de Salas - JavaScript

// Dados simulados para demonstração
const mockData = {
    salas: [
        { bloco: 'A', sala: '101', turma: 'SB276', turno: 'manha', dia: 'segunda' },
        { bloco: 'B', sala: '203', turma: 'ADM2PM', turno: 'tarde', dia: 'terca' },
        { bloco: 'C', sala: '304', turma: 'SB306', turno: 'manha', dia: 'quarta' },
        { bloco: 'A', sala: '307', turma: 'ADM2PM', turno: 'tarde', dia: 'terca' },
        { bloco: 'D', sala: '205', turma: 'ADM2PM', turno: 'manha', dia: 'quinta' },
        { bloco: 'E', sala: '209', turma: 'DIR2PM', turno: 'noite', dia: 'sexta' }
    ],
    usuario: {
        nome: 'Administrador',
        email: 'admin@unieuro.edu.br'
    }
};

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Função principal de inicialização
function initializeApp() {
    const currentPage = getCurrentPage();
    
    switch(currentPage) {
        case 'login':
            initializeLogin();
            break;
        case 'dashboard':
            initializeDashboard();
            break;
        case 'cadastrar':
            initializeCadastrar();
            break;
        case 'reservar':
            initializeReservar();
            break;
        case 'perfil':
            initializePerfil();
            break;
    }
    
    // Inicializar funcionalidades comuns
    initializeCommonFeatures();
}

// Detectar página atual
function getCurrentPage() {
    const path = window.location.pathname;
    const filename = path.split('/').pop().split('.')[0];
    
    if (filename === '' || filename === 'index') {
        return 'login';
    }
    
    return filename;
}

// ===== FUNCIONALIDADES DA PÁGINA DE LOGIN =====
function initializeLogin() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
}

function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Validação simples
    if (!email || !password) {
        showAlert('Por favor, preencha todos os campos.', 'error');
        return;
    }
    
    if (!isValidEmail(email)) {
        showAlert('Por favor, insira um e-mail válido.', 'error');
        return;
    }
    
    // Simulação de login
    showAlert('Login realizado com sucesso!', 'success');
    
    // Redirecionar para dashboard após 1 segundo
    setTimeout(() => {
        window.location.href = 'dashboard.html';
    }, 1000);
}

// ===== FUNCIONALIDADES DO DASHBOARD =====
function initializeDashboard() {
    loadDashboardData();
    initializeFilters();
}

function loadDashboardData() {
    const tableBody = document.querySelector('.data-table tbody');
    if (!tableBody) return;
    
    // Limpar tabela
    tableBody.innerHTML = '';
    
    // Carregar dados das salas
    mockData.salas.forEach(sala => {
        const row = createTableRow(sala);
        tableBody.appendChild(row);
    });
    
    // Atualizar contador
    updateStatsCounter();
}

function createTableRow(sala) {
    const row = document.createElement('tr');
    
    const badgeClass = `badge badge-${sala.turno}`;
    const turnoText = sala.turno.charAt(0).toUpperCase() + sala.turno.slice(1);
    const diaText = sala.dia.charAt(0).toUpperCase() + sala.dia.slice(1);
    
    row.innerHTML = `
        <td>${sala.bloco}</td>
        <td>${sala.sala}</td>
        <td>${sala.turma}</td>
        <td><span class="${badgeClass}">${turnoText}</span></td>
        <td>${diaText}</td>
        <td><button class="btn-select" onclick="selectSala('${sala.bloco}', '${sala.sala}')">Selecionar</button></td>
    `;
    
    return row;
}

function updateStatsCounter() {
    const statsNumber = document.querySelector('.stats-number');
    if (statsNumber) {
        statsNumber.textContent = mockData.salas.length;
    }
}

// ===== FUNCIONALIDADES DE FILTROS =====
function initializeFilters() {
    const filterSelects = document.querySelectorAll('.filters-grid select');
    
    filterSelects.forEach(select => {
        select.addEventListener('change', applyFilters);
    });
}

function applyFilters() {
    const filters = getActiveFilters();
    const filteredData = filterSalas(mockData.salas, filters);
    
    // Atualizar tabela com dados filtrados
    updateTable(filteredData);
}

function getActiveFilters() {
    const filters = {};
    
    const blocoFilter = document.querySelector('[id*="filter-bloco"]');
    const cursoFilter = document.querySelector('[id*="filter-curso"]');
    const turmaFilter = document.querySelector('[id*="filter-turma"]');
    const diaFilter = document.querySelector('[id*="filter-dia"]');
    const turnoFilter = document.querySelector('[id*="filter-turno"]');
    
    if (blocoFilter && blocoFilter.value) filters.bloco = blocoFilter.value;
    if (cursoFilter && cursoFilter.value) filters.curso = cursoFilter.value;
    if (turmaFilter && turmaFilter.value) filters.turma = turmaFilter.value;
    if (diaFilter && diaFilter.value) filters.dia = diaFilter.value;
    if (turnoFilter && turnoFilter.value) filters.turno = turnoFilter.value;
    
    return filters;
}

function filterSalas(salas, filters) {
    return salas.filter(sala => {
        for (let key in filters) {
            if (sala[key] !== filters[key]) {
                return false;
            }
        }
        return true;
    });
}

function updateTable(data) {
    const tableBody = document.querySelector('.data-table tbody');
    if (!tableBody) return;
    
    tableBody.innerHTML = '';
    
    data.forEach(sala => {
        const row = createTableRow(sala);
        tableBody.appendChild(row);
    });
    
    // Atualizar contador
    const statsNumber = document.querySelector('.stats-number');
    if (statsNumber) {
        statsNumber.textContent = data.length;
    }
}

function clearFilters() {
    const filterSelects = document.querySelectorAll('.filters-grid select');
    
    filterSelects.forEach(select => {
        select.value = '';
    });
    
    // Recarregar dados originais
    loadDashboardData();
}

// ===== FUNCIONALIDADES DE CADASTRAR =====
function initializeCadastrar() {
    initializeFilters();
    showCadastroMessage();
}

function showCadastroMessage() {
    const formContainer = document.querySelector('.form-container');
    if (formContainer) {
        formContainer.innerHTML = `
            <h3>Área de Cadastro</h3>
            <p>Selecione os filtros acima para começar a cadastrar novos itens no sistema.</p>
            <div style="margin-top: 20px;">
                <button class="btn-primary" onclick="showCadastroForm()">Novo Cadastro</button>
            </div>
        `;
    }
}

function showCadastroForm() {
    const formContainer = document.querySelector('.form-container');
    if (formContainer) {
        formContainer.innerHTML = `
            <h3>Cadastrar Nova Sala</h3>
            <form id="cadastroForm" style="margin-top: 20px;">
                <div class="form-group">
                    <label for="novo-bloco">Bloco</label>
                    <select id="novo-bloco" name="bloco" required>
                        <option value="">Selecione</option>
                        <option value="A">A</option>
                        <option value="B">B</option>
                        <option value="C">C</option>
                        <option value="D">D</option>
                        <option value="E">E</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="nova-sala">Número da Sala</label>
                    <input type="text" id="nova-sala" name="sala" placeholder="Ex: 101" required>
                </div>
                <div class="form-group">
                    <label for="nova-turma">Turma</label>
                    <input type="text" id="nova-turma" name="turma" placeholder="Ex: SB276" required>
                </div>
                <button type="submit" class="btn-primary">Cadastrar Sala</button>
                <button type="button" class="btn-secondary" onclick="showCadastroMessage()" style="margin-left: 10px;">Cancelar</button>
            </form>
        `;
        
        document.getElementById('cadastroForm').addEventListener('submit', handleCadastro);
    }
}

function handleCadastro(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const novaSala = {
        bloco: formData.get('bloco'),
        sala: formData.get('sala'),
        turma: formData.get('turma'),
        turno: 'manha', // Valor padrão
        dia: 'segunda' // Valor padrão
    };
    
    // Adicionar à lista de salas
    mockData.salas.push(novaSala);
    
    showAlert('Sala cadastrada com sucesso!', 'success');
    showCadastroMessage();
}

// ===== FUNCIONALIDADES DE RESERVAR =====
function initializeReservar() {
    initializeFilters();
    showReservaMessage();
}

function showReservaMessage() {
    const formContainer = document.querySelector('.form-container');
    if (formContainer) {
        formContainer.innerHTML = `
            <h3>Área de Reserva</h3>
            <p>Selecione os filtros acima para visualizar as salas disponíveis e fazer sua reserva.</p>
            <div style="margin-top: 20px;">
                <button class="btn-primary" onclick="showReservaForm()">Nova Reserva</button>
            </div>
        `;
    }
}

function showReservaForm() {
    const formContainer = document.querySelector('.form-container');
    if (formContainer) {
        formContainer.innerHTML = `
            <h3>Fazer Reserva</h3>
            <form id="reservaForm" style="margin-top: 20px;">
                <div class="form-group">
                    <label for="reserva-bloco">Bloco</label>
                    <select id="reserva-bloco" name="bloco" required>
                        <option value="">Selecione</option>
                        <option value="A">A</option>
                        <option value="B">B</option>
                        <option value="C">C</option>
                        <option value="D">D</option>
                        <option value="E">E</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="reserva-sala">Sala</label>
                    <input type="text" id="reserva-sala" name="sala" placeholder="Ex: 101" required>
                </div>
                <div class="form-group">
                    <label for="reserva-data">Data</label>
                    <input type="date" id="reserva-data" name="data" required>
                </div>
                <div class="form-group">
                    <label for="reserva-horario">Horário</label>
                    <select id="reserva-horario" name="horario" required>
                        <option value="">Selecione</option>
                        <option value="08:00-10:00">08:00 - 10:00</option>
                        <option value="10:00-12:00">10:00 - 12:00</option>
                        <option value="14:00-16:00">14:00 - 16:00</option>
                        <option value="16:00-18:00">16:00 - 18:00</option>
                        <option value="19:00-21:00">19:00 - 21:00</option>
                    </select>
                </div>
                <button type="submit" class="btn-primary">Confirmar Reserva</button>
                <button type="button" class="btn-secondary" onclick="showReservaMessage()" style="margin-left: 10px;">Cancelar</button>
            </form>
        `;
        
        document.getElementById('reservaForm').addEventListener('submit', handleReserva);
    }
}

function handleReserva(event) {
    event.preventDefault();
    
    showAlert('Reserva realizada com sucesso!', 'success');
    showReservaMessage();
}

// ===== FUNCIONALIDADES DO PERFIL =====
function initializePerfil() {
    loadUserProfile();
    
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', handleProfileUpdate);
    }
}

function loadUserProfile() {
    const nomeInput = document.getElementById('nome');
    const emailInput = document.getElementById('email-perfil');
    
    if (nomeInput) nomeInput.value = mockData.usuario.nome;
    if (emailInput) emailInput.value = mockData.usuario.email;
}

function handleProfileUpdate(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const senhaAtual = formData.get('senha-atual');
    const novaSenha = formData.get('nova-senha');
    const confirmarSenha = formData.get('confirmar-senha');
    
    // Validações
    if (novaSenha && novaSenha !== confirmarSenha) {
        showAlert('As senhas não coincidem.', 'error');
        return;
    }
    
    if (novaSenha && novaSenha.length < 6) {
        showAlert('A senha deve ter pelo menos 6 caracteres.', 'error');
        return;
    }
    
    // Atualizar dados do usuário
    mockData.usuario.nome = formData.get('nome');
    mockData.usuario.email = formData.get('email');
    
    showAlert('Perfil atualizado com sucesso!', 'success');
}

// ===== FUNCIONALIDADES COMUNS =====
function initializeCommonFeatures() {
    // Adicionar eventos de navegação
    addNavigationEvents();
    
    // Adicionar eventos de logout
    addLogoutEvents();
}

function addNavigationEvents() {
    const navLinks = document.querySelectorAll('.nav-item a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Remover classe active de todos os itens
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            
            // Adicionar classe active ao item clicado
            this.parentElement.classList.add('active');
        });
    });
}

function addLogoutEvents() {
    const logoutButtons = document.querySelectorAll('.btn-logout');
    
    logoutButtons.forEach(button => {
        button.addEventListener('click', logout);
    });
}

function logout() {
    if (confirm('Tem certeza que deseja sair?')) {
        showAlert('Logout realizado com sucesso!', 'success');
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1000);
    }
}

function selectSala(bloco, sala) {
    showAlert(`Sala ${bloco}${sala} selecionada!`, 'info');
}

// ===== FUNÇÕES UTILITÁRIAS =====
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showAlert(message, type = 'info') {
    // Remover alertas existentes
    const existingAlert = document.querySelector('.alert');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    // Criar novo alerta
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        max-width: 300px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        animation: slideIn 0.3s ease-out;
    `;
    
    // Definir cor baseada no tipo
    switch(type) {
        case 'success':
            alert.style.backgroundColor = '#10b981';
            break;
        case 'error':
            alert.style.backgroundColor = '#ef4444';
            break;
        case 'info':
            alert.style.backgroundColor = '#3b82f6';
            break;
        default:
            alert.style.backgroundColor = '#6b7280';
    }
    
    alert.textContent = message;
    document.body.appendChild(alert);
    
    // Remover após 3 segundos
    setTimeout(() => {
        if (alert.parentNode) {
            alert.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }
    }, 3000);
}

// Adicionar animações CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);


// ===== FUNCIONALIDADES DE EXIBIR SALAS =====
function initializeExibir() {
    initializeBlockFilters();
    loadRoomsData();
}

function initializeBlockFilters() {
    const blockButtons = document.querySelectorAll('.btn-block');
    
    blockButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            blockButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Filter rooms based on selected block
            filterRoomsByBlock(this.textContent);
        });
    });
}

function filterRoomsByBlock(blockText) {
    const roomCards = document.querySelectorAll('.room-card');
    
    roomCards.forEach(card => {
        if (blockText === 'Todos os Blocos') {
            card.style.display = 'block';
        } else {
            const roomTitle = card.querySelector('h4').textContent;
            const roomBlock = roomTitle.split('-')[0].replace('Sala ', '');
            
            if (blockText.includes(roomBlock)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        }
    });
}

function loadRoomsData() {
    // Dados das salas já estão no HTML, mas podemos adicionar mais funcionalidades aqui
    const editButtons = document.querySelectorAll('.btn-edit');
    
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const roomCard = this.closest('.room-card');
            const roomTitle = roomCard.querySelector('h4').textContent;
            showAlert(`Editando ${roomTitle}`, 'info');
        });
    });
}

// ===== FUNCIONALIDADES DE RELATÓRIOS =====
function initializeRelatorios() {
    const reportForm = document.querySelector('.report-filters');
    if (reportForm) {
        const generateButton = reportForm.querySelector('.btn-primary');
        if (generateButton) {
            generateButton.addEventListener('click', generateReport);
        }
    }
}

function generateReport() {
    const reportType = document.getElementById('report-type').value;
    const filterBloco = document.getElementById('filter-bloco-rel').value;
    const filterTurmaCurso = document.getElementById('filter-turma-curso-rel').value;
    
    if (!reportType) {
        showAlert('Por favor, selecione um tipo de relatório.', 'error');
        return;
    }
    
    // Simular geração de relatório
    const reportDisplay = document.querySelector('.report-display');
    
    reportDisplay.innerHTML = `
        <div class="report-content">
            <h3>Relatório: ${getReportTypeName(reportType)}</h3>
            <div class="report-filters-applied">
                <p><strong>Filtros aplicados:</strong></p>
                <ul>
                    ${filterBloco ? `<li>Bloco: ${filterBloco}</li>` : ''}
                    ${filterTurmaCurso ? `<li>Turma/Curso: ${filterTurmaCurso}</li>` : ''}
                    <li>Data de geração: ${new Date().toLocaleDateString('pt-BR')}</li>
                </ul>
            </div>
            <div class="report-data">
                <h4>Dados do Relatório</h4>
                <table class="report-table">
                    <thead>
                        <tr>
                            <th>Sala</th>
                            <th>Bloco</th>
                            <th>Status</th>
                            <th>Ocupação</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>A-101</td>
                            <td>A</td>
                            <td>Ocupada</td>
                            <td>85%</td>
                        </tr>
                        <tr>
                            <td>A-102</td>
                            <td>A</td>
                            <td>Livre</td>
                            <td>0%</td>
                        </tr>
                        <tr>
                            <td>A-103</td>
                            <td>A</td>
                            <td>Livre</td>
                            <td>0%</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="report-actions">
                <button class="btn-primary" onclick="exportReport()">Exportar PDF</button>
                <button class="btn-secondary" onclick="printReport()">Imprimir</button>
            </div>
        </div>
    `;
    
    showAlert('Relatório gerado com sucesso!', 'success');
}

function getReportTypeName(type) {
    const types = {
        'uso-salas': 'Uso de Salas',
        'reservas-futuras': 'Reservas Futuras',
        'historico-reservas': 'Histórico de Reservas'
    };
    return types[type] || 'Relatório Personalizado';
}

function exportReport() {
    showAlert('Funcionalidade de exportação em desenvolvimento.', 'info');
}

function printReport() {
    window.print();
}

// Atualizar a função de inicialização principal
function initializeApp() {
    const currentPage = getCurrentPage();
    
    switch(currentPage) {
        case 'login':
            initializeLogin();
            break;
        case 'dashboard':
            initializeDashboard();
            break;
        case 'cadastrar':
            initializeCadastrar();
            break;
        case 'reservar':
            initializeReservar();
            break;
        case 'perfil':
            initializePerfil();
            break;
        case 'exibir':
            initializeExibir();
            break;
        case 'relatorios':
            initializeRelatorios();
            break;
    }
    
    // Inicializar funcionalidades comuns
    initializeCommonFeatures();
}

// Adicionar estilos CSS para os relatórios via JavaScript
const reportStyles = document.createElement('style');
reportStyles.textContent = `
    .report-content {
        text-align: left;
        width: 100%;
    }
    
    .report-content h3 {
        color: #1f2937;
        margin-bottom: 20px;
        font-size: 20px;
    }
    
    .report-filters-applied {
        background: #f9fafb;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    .report-filters-applied ul {
        margin: 8px 0 0 20px;
        color: #6b7280;
    }
    
    .report-data h4 {
        color: #374151;
        margin-bottom: 16px;
    }
    
    .report-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }
    
    .report-table th,
    .report-table td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .report-table th {
        background: #f9fafb;
        font-weight: 600;
        color: #374151;
    }
    
    .report-actions {
        display: flex;
        gap: 12px;
        margin-top: 20px;
    }
    
    .report-actions button {
        padding: 10px 20px;
    }
`;
document.head.appendChild(reportStyles);

