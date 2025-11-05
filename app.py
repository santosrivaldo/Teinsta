#!/usr/bin/env python3
"""
Sistema de Gestão ISO 27001
Aplicação para implementação de ISO 27001 em empresas privadas
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory, session
import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
from werkzeug.utils import secure_filename
from functools import wraps

# Tentar carregar variáveis de ambiente do arquivo .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv não está instalado, continuar normalmente

app = Flask(__name__)

# Configurações de segurança - usar variáveis de ambiente em produção
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'iso27001-secret-key-change-in-production')
app.config['PASSWORD'] = os.environ.get('DASHBOARD_PASSWORD', 'admin123')  # Senha padrão: admin123

# Configurações de arquivos
data_dir = Path(os.environ.get('DATA_DIR', '.'))
data_dir.mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = data_dir / 'uploads'
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt', 'png', 'jpg', 'jpeg', 'zip', 'rar'}

DB_PATH = data_dir / 'iso27001.db'

def login_required(f):
    """Decorator para proteger rotas que requerem autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == app.config['PASSWORD']:
            session['logged_in'] = True
            next_page = request.args.get('next', url_for('index'))
            return redirect(next_page)
        else:
            return render_template('login.html', error='Senha incorreta!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout"""
    session.pop('logged_in', None)
    return redirect(url_for('login'))

def parse_modulo_row(row):
    """Parse módulo row que pode ter estrutura antiga (8 campos) ou nova (11 campos)"""
    if len(row) == 8:
        # Estrutura antiga: id, codigo, nome, descricao, concluido, data_conclusao, observacoes, data_criacao
        mod_id, codigo, nome, descricao, concluido, data_conclusao, observacoes, data_criacao = row
        return {
            'id': mod_id,
            'codigo': codigo,
            'nome': nome,
            'descricao': descricao,
            'concluido': concluido,
            'data_planejada_inicio': None,
            'data_planejada_fim': None,
            'data_inicio': None,
            'data_conclusao': data_conclusao,
            'observacoes': observacoes,
            'data_criacao': data_criacao
        }
    else:
        # Estrutura nova: id, codigo, nome, descricao, concluido, data_planejada_inicio, data_planejada_fim, data_inicio, data_conclusao, observacoes, data_criacao
        mod_id, codigo, nome, descricao, concluido, data_planejada_inicio, data_planejada_fim, data_inicio, data_conclusao, observacoes, data_criacao = row
        return {
            'id': mod_id,
            'codigo': codigo,
            'nome': nome,
            'descricao': descricao,
            'concluido': concluido,
            'data_planejada_inicio': data_planejada_inicio,
            'data_planejada_fim': data_planejada_fim,
            'data_inicio': data_inicio,
            'data_conclusao': data_conclusao,
            'observacoes': observacoes,
            'data_criacao': data_criacao
        }

def init_db():
    """Inicializa o banco de dados com as tabelas necessárias"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Verificar se a tabela modulos existe e qual estrutura tem
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='modulos'")
    if c.fetchone():
        # Verificar estrutura da tabela
        c.execute("PRAGMA table_info(modulos)")
        columns = [col[1] for col in c.fetchall()]
        if 'data_planejada_inicio' not in columns:
            # Adicionar novas colunas
            c.execute('ALTER TABLE modulos ADD COLUMN data_planejada_inicio DATE')
            c.execute('ALTER TABLE modulos ADD COLUMN data_planejada_fim DATE')
            c.execute('ALTER TABLE modulos ADD COLUMN data_inicio DATE')
            conn.commit()
    
    # Tabela de Controles
    c.execute('''
        CREATE TABLE IF NOT EXISTS controles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT,
            categoria TEXT,
            status TEXT DEFAULT 'Pendente',
            responsavel TEXT,
            obrigatorio INTEGER DEFAULT 0,
            grupo_implementacao TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Verificar se colunas existem, se não, criar
    c.execute("PRAGMA table_info(controles)")
    columns = [col[1] for col in c.fetchall()]
    if 'obrigatorio' not in columns:
        c.execute('ALTER TABLE controles ADD COLUMN obrigatorio INTEGER DEFAULT 0')
    if 'grupo_implementacao' not in columns:
        c.execute('ALTER TABLE controles ADD COLUMN grupo_implementacao TEXT')
    
    # Tabela de Políticas
    c.execute('''
        CREATE TABLE IF NOT EXISTS politicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT,
            versao TEXT,
            status TEXT DEFAULT 'Rascunho',
            aprovador TEXT,
            data_aprovacao DATE,
            data_revisao DATE,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de Não Conformidades
    c.execute('''
        CREATE TABLE IF NOT EXISTS nao_conformidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT,
            severidade TEXT,
            status TEXT DEFAULT 'Aberto',
            responsavel TEXT,
            acao_corretiva TEXT,
            prazo DATE,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_resolucao DATE
        )
    ''')
    
    # Tabela de Auditorias
    c.execute('''
        CREATE TABLE IF NOT EXISTS auditorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            tipo TEXT,
            escopo TEXT,
            data_auditoria DATE,
            auditor TEXT,
            resultado TEXT,
            observacoes TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de Módulos (para rastreamento de conclusão)
    c.execute('''
        CREATE TABLE IF NOT EXISTS modulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            descricao TEXT,
            concluido INTEGER DEFAULT 0,
            data_planejada_inicio DATE,
            data_planejada_fim DATE,
            data_inicio DATE,
            data_conclusao DATE,
            observacoes TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de Passos de Ação (guia passo a passo por módulo)
    c.execute('''
        CREATE TABLE IF NOT EXISTS passos_acao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modulo_codigo TEXT NOT NULL,
            ordem INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT,
            concluido INTEGER DEFAULT 0,
            data_conclusao DATE,
            responsavel TEXT,
            FOREIGN KEY (modulo_codigo) REFERENCES modulos(codigo)
        )
    ''')
    
    # Tabela de Anexos dos Controles
    c.execute('''
        CREATE TABLE IF NOT EXISTS anexos_controles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            controle_id INTEGER NOT NULL,
            nome_arquivo TEXT NOT NULL,
            nome_original TEXT NOT NULL,
            tamanho INTEGER,
            tipo TEXT,
            descricao TEXT,
            data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (controle_id) REFERENCES controles(id)
        )
    ''')
    
    # Tabela de Normas
    c.execute('''
        CREATE TABLE IF NOT EXISTS normas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            descricao TEXT,
            tipo TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de Relacionamento Controle-Norma
    c.execute('''
        CREATE TABLE IF NOT EXISTS controle_normas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            controle_id INTEGER NOT NULL,
            norma_id INTEGER NOT NULL,
            FOREIGN KEY (controle_id) REFERENCES controles(id),
            FOREIGN KEY (norma_id) REFERENCES normas(id),
            UNIQUE(controle_id, norma_id)
        )
    ''')
    
    # Tabela de Tasks de Controle
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks_controle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            controle_id INTEGER NOT NULL,
            ordem INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT,
            concluido INTEGER DEFAULT 0,
            responsavel TEXT,
            data_conclusao DATE,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (controle_id) REFERENCES controles(id)
        )
    ''')
    
    # Tabela de Relacionamento Task-Norma
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks_normas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            norma_id INTEGER NOT NULL,
            FOREIGN KEY (task_id) REFERENCES tasks_controle(id),
            FOREIGN KEY (norma_id) REFERENCES normas(id),
            UNIQUE(task_id, norma_id)
        )
    ''')
    
    # Tabela de Documentos Necessários por Controle
    c.execute('''
        CREATE TABLE IF NOT EXISTS documentos_controle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            controle_id INTEGER NOT NULL,
            nome_documento TEXT NOT NULL,
            tipo_documento TEXT,
            descricao TEXT,
            obrigatorio INTEGER DEFAULT 0,
            template TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (controle_id) REFERENCES controles(id)
        )
    ''')
    
    # Inserir todos os módulos da ISO 27001
    modulos_padrao = [
        ('A.5', 'Política de Segurança', 'Políticas de segurança da informação', None, None, None, None),
        ('A.6', 'Organização da Segurança da Informação', 'Estrutura organizacional para segurança', None, None, None, None),
        ('A.7', 'Segurança em Recursos Humanos', 'Segurança antes, durante e após o emprego', None, None, None, None),
        ('A.8', 'Gestão de Ativos', 'Responsabilidade por ativos e classificação da informação', None, None, None, None),
        ('A.9', 'Controle de Acesso', 'Requisitos de negócio de controle de acesso', None, None, None, None),
        ('A.10', 'Criptografia', 'Controles criptográficos', None, None, None, None),
        ('A.11', 'Segurança Física e do Ambiente', 'Áreas seguras e equipamentos', None, None, None, None),
        ('A.12', 'Segurança nas Operações', 'Operações responsáveis e proteção contra malware', None, None, None, None),
        ('A.13', 'Segurança nas Comunicações', 'Gestão de segurança de rede', None, None, None, None),
        ('A.14', 'Aquisição, Desenvolvimento e Manutenção de Sistemas', 'Requisitos de segurança de sistemas', None, None, None, None),
        ('A.15', 'Relacionamento na Cadeia de Suprimento', 'Segurança da informação na cadeia de suprimento', None, None, None, None),
        ('A.16', 'Gestão de Incidente de Segurança da Informação', 'Gestão de incidentes e melhorias', None, None, None, None),
        ('A.17', 'Aspectos da Segurança da Informação na Gestão de Continuidade de Negócio', 'Continuidade de segurança da informação', None, None, None, None),
        ('A.18', 'Conformidade / Compliance', 'Conformidade com requisitos legais e contratuais', None, None, None, None),
    ]
    
    c.execute('SELECT COUNT(*) FROM modulos')
    if c.fetchone()[0] == 0:
        c.executemany('''
            INSERT INTO modulos (codigo, nome, descricao, data_planejada_inicio, data_planejada_fim, data_inicio, data_conclusao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', modulos_padrao)
        
        # Inserir passos de ação padrão para cada módulo
        passos_padrao = [
            # A.5 - Política de Segurança
            ('A.5', 1, 'Definir escopo do SGSI', 'Documentar o escopo do Sistema de Gestão de Segurança da Informação', 0, None, None),
            ('A.5', 2, 'Elaborar políticas de segurança', 'Criar políticas de segurança da informação conforme requisitos da organização', 0, None, None),
            ('A.5', 3, 'Aprovação pela direção', 'Submeter políticas para aprovação da alta direção', 0, None, None),
            ('A.5', 4, 'Comunicar políticas', 'Publicar e comunicar políticas a todos os funcionários e partes interessadas', 0, None, None),
            ('A.5', 5, 'Estabelecer processo de revisão', 'Definir frequência e processo de revisão das políticas', 0, None, None),
            
            # A.6 - Organização da Segurança
            ('A.6', 1, 'Definir funções e responsabilidades', 'Atribuir responsabilidades de segurança da informação a funções específicas', 0, None, None),
            ('A.6', 2, 'Implementar separação de funções', 'Garantir segregação de deveres conflitantes', 0, None, None),
            ('A.6', 3, 'Estabelecer contatos externos', 'Definir contatos com autoridades e grupos especializados', 0, None, None),
            ('A.6', 4, 'Criar políticas de trabalho remoto', 'Desenvolver políticas para trabalho móvel e teletrabalho', 0, None, None),
            
            # A.7 - Segurança em Recursos Humanos
            ('A.7', 1, 'Implementar processo de screening', 'Estabelecer verificações de antecedentes para candidatos', 0, None, None),
            ('A.7', 2, 'Definir termos de emprego', 'Incluir responsabilidades de segurança nos contratos', 0, None, None),
            ('A.7', 3, 'Programa de treinamento', 'Desenvolver e implementar programa de conscientização em segurança', 0, None, None),
            ('A.7', 4, 'Processo disciplinar', 'Estabelecer processo para ações disciplinares', 0, None, None),
            ('A.7', 5, 'Processo de desligamento', 'Definir procedimentos para término de emprego', 0, None, None),
            
            # A.8 - Gestão de Ativos
            ('A.8', 1, 'Inventariar todos os ativos', 'Identificar e catalogar todos os ativos de informação', 0, None, None),
            ('A.8', 2, 'Designar proprietários', 'Atribuir proprietários para cada ativo', 0, None, None),
            ('A.8', 3, 'Regras de uso aceitável', 'Documentar políticas de uso aceitável de ativos', 0, None, None),
            ('A.8', 4, 'Classificação de informação', 'Implementar esquema de classificação de informação', 0, None, None),
            ('A.8', 5, 'Rotulagem de informação', 'Desenvolver procedimentos de rotulagem', 0, None, None),
            
            # A.9 - Controle de Acesso
            ('A.9', 1, 'Política de controle de acesso', 'Desenvolver e documentar política de acesso', 0, None, None),
            ('A.9', 2, 'Gestão de usuários', 'Implementar processo de registro e cancelamento de usuários', 0, None, None),
            ('A.9', 3, 'Gestão de privilégios', 'Controlar atribuição de direitos de acesso privilegiado', 0, None, None),
            ('A.9', 4, 'Autenticação de usuários', 'Implementar métodos seguros de autenticação', 0, None, None),
            ('A.9', 5, 'Revisão de acessos', 'Estabelecer processo de revisão periódica de acessos', 0, None, None),
            
            # A.10 - Criptografia
            ('A.10', 1, 'Política de criptografia', 'Desenvolver política de uso de controles criptográficos', 0, None, None),
            ('A.10', 2, 'Gestão de chaves', 'Implementar processo de gestão de chaves criptográficas', 0, None, None),
            
            # A.11 - Segurança Física
            ('A.11', 1, 'Definir perímetros físicos', 'Estabelecer áreas seguras e controles de perímetro', 0, None, None),
            ('A.11', 2, 'Controles de entrada', 'Implementar controles de acesso físico', 0, None, None),
            ('A.11', 3, 'Proteção de equipamentos', 'Garantir proteção física de equipamentos', 0, None, None),
            ('A.11', 4, 'Segurança de cablagem', 'Proteger cablagem de dados e energia', 0, None, None),
            ('A.11', 5, 'Manutenção de equipamentos', 'Estabelecer procedimentos de manutenção', 0, None, None),
            
            # A.12 - Segurança nas Operações
            ('A.12', 1, 'Documentar procedimentos', 'Documentar procedimentos operacionais', 0, None, None),
            ('A.12', 2, 'Gestão de mudanças', 'Implementar processo de controle de mudanças', 0, None, None),
            ('A.12', 3, 'Controles contra malware', 'Implementar proteção contra malware', 0, None, None),
            ('A.12', 4, 'Backup de informações', 'Estabelecer processo de backup e recuperação', 0, None, None),
            ('A.12', 5, 'Registros de eventos', 'Implementar sistema de logging e monitoramento', 0, None, None),
            ('A.12', 6, 'Gestão de vulnerabilidades', 'Estabelecer processo de gestão de vulnerabilidades', 0, None, None),
            
            # A.13 - Segurança nas Comunicações
            ('A.13', 1, 'Controles de rede', 'Implementar controles de segurança de rede', 0, None, None),
            ('A.13', 2, 'Política de transferência', 'Desenvolver políticas para transferência de informação', 0, None, None),
            ('A.13', 3, 'Segurança de mensagens', 'Proteger mensagens eletrônicas', 0, None, None),
            
            # A.14 - Aquisição e Desenvolvimento
            ('A.14', 1, 'Requisitos de segurança', 'Incluir requisitos de segurança em especificações', 0, None, None),
            ('A.14', 2, 'Desenvolvimento seguro', 'Estabelecer práticas de desenvolvimento seguro', 0, None, None),
            ('A.14', 3, 'Testes de segurança', 'Implementar testes de segurança no desenvolvimento', 0, None, None),
            ('A.14', 4, 'Proteção de dados de teste', 'Garantir proteção de dados usados em testes', 0, None, None),
            
            # A.15 - Cadeia de Suprimento
            ('A.15', 1, 'Política de fornecedores', 'Desenvolver política de segurança para fornecedores', 0, None, None),
            ('A.15', 2, 'Acordos com fornecedores', 'Incluir requisitos de segurança em acordos', 0, None, None),
            ('A.15', 3, 'Monitoramento de fornecedores', 'Implementar processo de monitoramento', 0, None, None),
            
            # A.16 - Gestão de Incidentes
            ('A.16', 1, 'Procedimentos de incidentes', 'Desenvolver procedimentos de gestão de incidentes', 0, None, None),
            ('A.16', 2, 'Canais de reporte', 'Estabelecer canais para reportar eventos', 0, None, None),
            ('A.16', 3, 'Processo de resposta', 'Implementar processo de resposta a incidentes', 0, None, None),
            ('A.16', 4, 'Aprendizado de incidentes', 'Estabelecer processo de análise e aprendizado', 0, None, None),
            
            # A.17 - Continuidade de Negócio
            ('A.17', 1, 'Planejamento de continuidade', 'Desenvolver plano de continuidade de segurança', 0, None, None),
            ('A.17', 2, 'Implementar controles', 'Implementar controles de continuidade', 0, None, None),
            ('A.17', 3, 'Testes e revisões', 'Realizar testes e revisões periódicas', 0, None, None),
            
            # A.18 - Conformidade
            ('A.18', 1, 'Identificar requisitos legais', 'Identificar legislação e requisitos aplicáveis', 0, None, None),
            ('A.18', 2, 'Proteção de registros', 'Implementar proteção de registros organizacionais', 0, None, None),
            ('A.18', 3, 'Revisão independente', 'Estabelecer processo de revisão independente', 0, None, None),
            ('A.18', 4, 'Verificação de conformidade', 'Implementar verificações de conformidade', 0, None, None),
        ]
        
        c.executemany('''
            INSERT INTO passos_acao (modulo_codigo, ordem, titulo, descricao, concluido, data_conclusao, responsavel)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', passos_padrao)
    
    # Inserir TODOS os controles padrão da ISO 27001 (completos)
    controles_padrao = [
        # A.5 - Política de Segurança
        ('A.5.1.1', 'Políticas para segurança da informação', 'Políticas devem ser definidas, documentadas e revisadas em intervalos planejados ou quando houver mudanças significativas', 'A.5 - Política de Segurança'),
        ('A.5.1.2', 'Revisão das políticas para segurança da informação', 'As políticas devem ser aprovadas pela direção e publicadas e comunicadas a todos os funcionários e partes interessadas relevantes', 'A.5 - Política de Segurança'),
        
        # A.6 - Organização da Segurança da Informação
        ('A.6.1.1', 'Funções e responsabilidades de segurança', 'Todas as responsabilidades de segurança devem ser definidas e alocadas', 'A.6 - Organização da Segurança da Informação'),
        ('A.6.1.2', 'Separação de funções', 'Deveres e áreas de responsabilidade conflitantes devem ser segregados para reduzir oportunidades de modificação não autorizada ou uso indevido de ativos da organização', 'A.6 - Organização da Segurança da Informação'),
        ('A.6.1.3', 'Contato com autoridades', 'Deve ser mantido contato apropriado com autoridades relevantes', 'A.6 - Organização da Segurança da Informação'),
        ('A.6.1.4', 'Contato com grupos especiais', 'Deve ser mantido contato apropriado com grupos ou associações especializadas em segurança', 'A.6 - Organização da Segurança da Informação'),
        ('A.6.1.5', 'Segurança da informação em gestão de projetos', 'A segurança da informação deve ser tratada em gestão de projetos, independentemente do tipo de projeto', 'A.6 - Organização da Segurança da Informação'),
        ('A.6.2.1', 'Políticas de trabalho móvel e teletrabalho', 'As políticas de segurança e medidas de apoio devem ser implementadas para proteger informações acessadas, processadas ou armazenadas em locais de trabalho móvel', 'A.6 - Organização da Segurança da Informação'),
        ('A.6.2.2', 'Dispositivos móveis', 'Deve ser estabelecida uma política e medidas de apoio para gerenciamento do uso de dispositivos móveis', 'A.6 - Organização da Segurança da Informação'),
        
        # A.7 - Segurança em Recursos Humanos
        ('A.7.1.1', 'Screenings', 'Screenings devem ser realizados para todos os candidatos a emprego, contratados e terceiros', 'A.7 - Segurança em Recursos Humanos'),
        ('A.7.1.2', 'Termos e condições de emprego', 'Termos e condições de emprego devem estabelecer as responsabilidades do funcionário pela segurança da informação', 'A.7 - Segurança em Recursos Humanos'),
        ('A.7.2.1', 'Conscientização e treinamento em segurança', 'O pessoal da organização e pessoas relevantes terceirizadas devem receber conscientização e treinamento em segurança apropriados e atualizados regularmente', 'A.7 - Segurança em Recursos Humanos'),
        ('A.7.2.2', 'Processo disciplinar', 'Deve haver um processo disciplinar formal e comunicado que tome ação contra funcionários que tenham comprometido a segurança da informação', 'A.7 - Segurança em Recursos Humanos'),
        ('A.7.3.1', 'Processo de término ou mudança de responsabilidades', 'Responsabilidades e deveres de emprego que permanecem válidos após término ou mudança de emprego devem ser definidos, comunicados ao funcionário ou terceirizado e aplicados', 'A.7 - Segurança em Recursos Humanos'),
        
        # A.8 - Gestão de Ativos
        ('A.8.1.1', 'Inventário de ativos', 'Todos os ativos devem ser identificados e inventariados', 'A.8 - Gestão de Ativos'),
        ('A.8.1.2', 'Proprietário dos ativos', 'Ativos mantidos no inventário devem ter proprietário designado', 'A.8 - Gestão de Ativos'),
        ('A.8.1.3', 'Uso aceitável de ativos', 'Regras para uso aceitável de informações e ativos associados com recursos de processamento de informação devem ser identificadas, documentadas e implementadas', 'A.8 - Gestão de Ativos'),
        ('A.8.1.4', 'Retorno de ativos', 'Todos os ativos devem ser retornados quando o emprego, contratos ou acordos são encerrados', 'A.8 - Gestão de Ativos'),
        ('A.8.2.1', 'Classificação da informação', 'Informação deve ser classificada de acordo com requisitos legais, valor, criticidade e sensibilidade para divulgação não autorizada', 'A.8 - Gestão de Ativos'),
        ('A.8.2.2', 'Rótulos de informação', 'Um conjunto apropriado de procedimentos para rotulagem de informação deve ser desenvolvido e implementado de acordo com o esquema de classificação adotado pela organização', 'A.8 - Gestão de Ativos'),
        ('A.8.2.3', 'Tratamento de ativos', 'Procedimentos para tratamento de ativos devem ser desenvolvidos e implementados de acordo com o esquema de classificação adotado pela organização', 'A.8 - Gestão de Ativos'),
        ('A.8.3.1', 'Gestão de mídia removível', 'Procedimentos devem ser implementados para o uso de mídia removível de acordo com o esquema de classificação adotado pela organização', 'A.8 - Gestão de Ativos'),
        ('A.8.3.2', 'Descarte de mídia', 'Mídia deve ser descartada de forma segura quando não for mais necessária, usando procedimentos formais', 'A.8 - Gestão de Ativos'),
        ('A.8.3.3', 'Mídia física em trânsito', 'Mídia física contendo informação deve ser protegida contra acesso não autorizado, uso indevido ou corrupção durante o transporte além dos limites físicos', 'A.8 - Gestão de Ativos'),
        
        # A.9 - Controle de Acesso
        ('A.9.1.1', 'Política de controle de acesso', 'Política de controle de acesso deve ser estabelecida, documentada e revisada com base em requisitos de negócio e segurança', 'A.9 - Controle de Acesso'),
        ('A.9.1.2', 'Acesso a redes e serviços de rede', 'Usuários devem ser fornecidos apenas com acesso a rede e serviços de rede que tenham sido explicitamente autorizados', 'A.9 - Controle de Acesso'),
        ('A.9.2.1', 'Registro e cancelamento de usuário', 'Formal processo de registro e cancelamento deve ser implementado para permitir e revogar acesso a sistemas de informação e serviços', 'A.9 - Controle de Acesso'),
        ('A.9.2.2', 'Provisionamento de acesso de usuário', 'Deve ser estabelecido um processo formal de provisionamento de acesso de usuário para atribuir ou revogar direitos de acesso para todos os tipos de usuários para todos os sistemas e serviços', 'A.9 - Controle de Acesso'),
        ('A.9.2.3', 'Gestão de direitos de acesso privilegiado', 'O uso e alocação de direitos de acesso privilegiado deve ser restrito e controlado', 'A.9 - Controle de Acesso'),
        ('A.9.2.4', 'Gestão de informações de autenticação secretas', 'Procedimentos de gestão de informações de autenticação secretas devem ser implementados através de todo o ciclo de vida', 'A.9 - Controle de Acesso'),
        ('A.9.2.5', 'Revisão dos direitos de acesso de usuário', 'Proprietários de ativos devem revisar os direitos de acesso de usuários regularmente', 'A.9 - Controle de Acesso'),
        ('A.9.2.6', 'Remoção ou ajuste dos direitos de acesso', 'Rights of access de todos os funcionários e terceirizados externos para informações e instalações de processamento devem ser removidos após término de emprego ou ajustados após mudança', 'A.9 - Controle de Acesso'),
        ('A.9.3.1', 'Uso de segredos para autenticação', 'Sistemas devem usar métodos seguros de autenticação de usuários, adequados para o método de acesso usado', 'A.9 - Controle de Acesso'),
        ('A.9.4.1', 'Política de informação e restrição de acesso', 'Acesso a informação e funções de aplicação deve ser restrito de acordo com a política de controle de acesso', 'A.9 - Controle de Acesso'),
        ('A.9.4.2', 'Procedimento de logon seguro', 'Onde exigido por política de controle de acesso, procedimento de logon seguro deve ser estabelecido e operado para sistemas de informação e aplicações', 'A.9 - Controle de Acesso'),
        ('A.9.4.3', 'Sistema de gestão de senhas', 'Sistema de gestão de senhas deve ser interativo e deve garantir qualidade de senha', 'A.9 - Controle de Acesso'),
        ('A.9.4.4', 'Uso de utilitários de privilégios do sistema', 'O uso de utilitários que podem ser capazes de sobrescrever sistema e controles de aplicação deve ser restrito e rigorosamente controlado', 'A.9 - Controle de Acesso'),
        ('A.9.4.5', 'Segregação em aplicações', 'Aplicações devem ser segregadas para limitar o risco', 'A.9 - Controle de Acesso'),
        ('A.9.4.6', 'Informações limitadas sobre políticas e procedimentos de acesso', 'Informações sobre políticas e procedimentos de controle de acesso deve estar disponível apenas para usuários que tenham direito a ela', 'A.9 - Controle de Acesso'),
        
        # A.10 - Criptografia
        ('A.10.1.1', 'Política de uso de controles criptográficos', 'Políticas sobre uso de controles criptográficos devem ser desenvolvidas e implementadas', 'A.10 - Criptografia'),
        ('A.10.1.2', 'Gestão de chaves', 'Gestão de chaves deve ser implementada através de todo o ciclo de vida da criptografia', 'A.10 - Criptografia'),
        
        # A.11 - Segurança Física e do Ambiente
        ('A.11.1.1', 'Perímetros físicos e controles de segurança', 'Perímetros físicos devem ser definidos e usados para proteger áreas que contêm informações e sistemas de processamento de informação', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.1.2', 'Controles físicos de entrada', 'Áreas seguras devem ser protegidas por controles apropriados de entrada para assegurar que apenas pessoas autorizadas têm acesso', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.1.3', 'Salas seguras e câmaras fortificadas', 'Salas seguras e câmaras fortificadas devem ser projetadas e implementadas', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.1.4', 'Perímetros físicos monitorados e de segurança', 'Perímetros físicos devem ser monitorados e revisados', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.1.5', 'Proteção contra ameaças físicas e ambientais', 'Proteção física contra desastres naturais, acidentes, ataques maliciosos e deliberados deve ser projetada e aplicada', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.1.6', 'Áreas de trabalho seguras', 'Áreas de trabalho seguras devem ser projetadas e protegidas', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.1', 'Equipamento de localização e proteção', 'Equipamento deve ser posicionado e protegido para reduzir riscos de ameaças ambientais e perigos e oportunidades de acesso não autorizado', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.2', 'Serviços de suporte', 'Equipamento deve ser protegido de falhas de energia e outros interrupções causadas por falhas nos serviços de suporte', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.3', 'Segurança de cablagem', 'Cablagem de energia e telecomunicações carregando dados ou suportando serviços de informação deve ser protegida contra interceptação ou dano', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.4', 'Manutenção de equipamento', 'Equipamento deve ser mantido corretamente para assegurar sua disponibilidade e integridade continuada', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.5', 'Remoção de ativos', 'Equipamento, informação ou software não devem ser retirados de instalações sem autorização', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.6', 'Segurança de equipamento e ativos fora das instalações', 'Segurança deve ser aplicada a ativos fora das instalações da organização, levando em conta diferentes riscos de trabalhar fora das instalações', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.7', 'Reutilização ou descarte seguro de equipamento', 'Todos os itens de equipamento contendo mídia de armazenamento devem ser verificados para garantir que qualquer informação sensível e licenciado software tenha sido removido ou sobrescrito de forma segura antes do descarte', 'A.11 - Segurança Física e do Ambiente'),
        ('A.11.2.8', 'Equipamento não utilizado', 'Equipamento não utilizado deve ser removido ou o uso de recursos de mídia removível e interface de rede deve ser desabilitado ou removido fisicamente', 'A.11 - Segurança Física e do Ambiente'),
        
        # A.12 - Segurança nas Operações
        ('A.12.1.1', 'Documentação de procedimentos operacionais', 'Procedimentos operacionais devem ser documentados e disponibilizados para todos os usuários que precisem deles', 'A.12 - Segurança nas Operações'),
        ('A.12.1.2', 'Gestão de mudanças', 'Mudanças em organização, processos de negócio, sistemas de informação e instalações devem ser controladas', 'A.12 - Segurança nas Operações'),
        ('A.12.1.3', 'Gestão de capacidade', 'Uso de recursos deve ser monitorado, ajustado e projeções futuras de requisitos de capacidade devem ser feitas para assegurar capacidade de sistema requerida', 'A.12 - Segurança nas Operações'),
        ('A.12.1.4', 'Separação de ambientes de desenvolvimento, teste e produção', 'Ambientes de desenvolvimento, teste e produção devem ser separados para reduzir riscos de acesso não autorizado ou mudanças aos sistemas de informação operacionais', 'A.12 - Segurança nas Operações'),
        ('A.12.2.1', 'Controles contra malware', 'Controles de detecção, prevenção e recuperação devem ser implementados, combinados com conscientização apropriada do usuário', 'A.12 - Segurança nas Operações'),
        ('A.12.3.1', 'Backup de informação', 'Backups de informações, software e imagens de sistema devem ser tomadas regularmente e testadas de acordo com o acordo de nível de serviço acordado', 'A.12 - Segurança nas Operações'),
        ('A.12.4.1', 'Registros de eventos', 'Logs de eventos que registram exceções, falhas e outros eventos relevantes devem ser produzidos, mantidos e revisados regularmente', 'A.12 - Segurança nas Operações'),
        ('A.12.4.2', 'Proteção de informação de log', 'Logging facilities and log information must be protected against tampering and unauthorized access', 'A.12 - Segurança nas Operações'),
        ('A.12.4.3', 'Logs de administrador e operador', 'Atividades de administradores de sistema e operadores devem ser registradas e logs protegidos e revisados regularmente', 'A.12 - Segurança nas Operações'),
        ('A.12.4.4', 'Sincronização de relógio', 'Relógios de todos os sistemas de informação relevantes devem ser sincronizados com uma fonte de tempo preciso e acordado', 'A.12 - Segurança nas Operações'),
        ('A.12.5.1', 'Instalação de software em sistemas operacionais', 'Procedimentos devem ser estabelecidos para controlar instalação de software em sistemas operacionais', 'A.12 - Segurança nas Operações'),
        ('A.12.6.1', 'Gestão de vulnerabilidades técnicas', 'Informação sobre vulnerabilidades técnicas de sistemas de informação em uso deve ser obtida, avaliada em termos de negócio e medidas apropriadas tomadas para tratar os riscos associados', 'A.12 - Segurança nas Operações'),
        ('A.12.6.2', 'Restrições em instalação de software', 'Regras que governam instalação de software por usuários devem ser estabelecidas e implementadas', 'A.12 - Segurança nas Operações'),
        ('A.12.7.1', 'Políticas e procedimentos de segurança de informação em uso de sistemas de informação', 'Regras, medidas e controles de segurança de informação devem ser estabelecidos e implementados quando sistemas de informação são utilizados', 'A.12 - Segurança nas Operações'),
        
        # A.13 - Segurança nas Comunicações
        ('A.13.1.1', 'Controles de rede', 'Redes devem ser gerenciadas e controladas para proteger informações em sistemas e aplicações', 'A.13 - Segurança nas Comunicações'),
        ('A.13.1.2', 'Política de transferência de informação', 'Políticas e procedimentos de transferência de informação devem ser estabelecidos para proteger transferência de informação através de todos os tipos de facilidades de comunicação', 'A.13 - Segurança nas Comunicações'),
        ('A.13.1.3', 'Mensagens eletrônicas', 'Informações contidas em mensagens eletrônicas devem ser adequadamente protegidas', 'A.13 - Segurança nas Comunicações'),
        ('A.13.2.1', 'Política de desenvolvimento de informação', 'Políticas e procedimentos devem ser estabelecidos para proteger informações aplicadas a desenvolvimento de sistemas de informação', 'A.13 - Segurança nas Comunicações'),
        ('A.13.2.2', 'Acordos de não divulgação', 'Acordos de não divulgação devem ser identificados, revisados regularmente e documentados para refletir necessidades atuais da organização para proteção de informação', 'A.13 - Segurança nas Comunicações'),
        ('A.13.2.3', 'Armazenamento de informação', 'Regras para armazenamento de informação, incluindo período de retenção e descarte, devem ser estabelecidas para aplicar proteção adequada de informação', 'A.13 - Segurança nas Comunicações'),
        ('A.13.2.4', 'Política de desenvolvimento de informação', 'Políticas e procedimentos devem ser estabelecidos para proteger informações aplicadas a desenvolvimento de sistemas de informação', 'A.13 - Segurança nas Comunicações'),
        
        # A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas
        ('A.14.1.1', 'Análise e especificação de requisitos de segurança', 'Requisitos de segurança de informação devem ser incluídos em requisitos para novos sistemas de informação ou melhorias em sistemas existentes', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.1.2', 'Segurança em aplicações em uso público', 'Informações envolvidas em aplicações públicas devem ser protegidas contra atividades fraudulentas, disputas contratuais e divulgação não autorizada e modificação', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.1.3', 'Proteção de serviços de transações online', 'Informações envolvidas em serviços de transações online devem ser protegidas para prevenir atividade incompleta, transmissão incorreta, roteamento incorreto, alteração não autorizada de mensagens, divulgação, duplicação ou replay de mensagens', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.1', 'Política de desenvolvimento seguro', 'Regras para desenvolvimento de software e sistemas devem ser estabelecidas e aplicadas em desenvolvimentos dentro da organização', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.2', 'Gestão de mudanças em sistemas de segurança', 'Mudanças em sistemas durante todo o ciclo de vida de desenvolvimento devem ser controladas pelo uso de gestão formal de controle de mudanças, incluindo mudanças em sistemas de informação, políticas de negócio, processos e procedimentos de segurança e controle', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.3', 'Revisão técnica de aplicações após mudanças em plataformas operacionais', 'Quando plataformas operacionais mudam, aplicações de negócio críticas devem ser revisadas e testadas para assegurar que não haja impacto adverso na segurança de informação organizacional ou operações', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.4', 'Restrições em mudanças em pacotes de software', 'Modificações a pacotes de software devem ser desencorajadas, limitadas a mudanças necessárias e todas as mudanças devem ser estritamente controladas', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.5', 'Princípios de engenharia de sistemas seguros', 'Princípios de engenharia devem ser estabelecidos, documentados, mantidos e aplicados a qualquer iniciativa de engenharia de sistemas de informação', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.6', 'Ambiente de desenvolvimento seguro', 'Organizações devem estabelecer e documentar adequadamente ambientes de desenvolvimento seguro para desenvolvimento e integração de componentes de sistema de informação em toda o ciclo de vida', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.7', 'Subcontratação de desenvolvimento', 'Organizações devem supervisionar e monitorar atividade de subcontratação de desenvolvimento de sistema', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.8', 'Teste de segurança em desenvolvimento', 'Testes de segurança devem ser conduzidos durante desenvolvimento', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.2.9', 'Teste de aceitação de sistema', 'Critérios de teste e planos de aceitação para novos sistemas de informação, atualizações e novas versões devem ser estabelecidos para sistemas de informação', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        ('A.14.3.1', 'Proteção de dados de teste', 'Dados de teste devem ser selecionados, protegidos e controlados cuidadosamente', 'A.14 - Aquisição, Desenvolvimento e Manutenção de Sistemas'),
        
        # A.15 - Relacionamento na Cadeia de Suprimento
        ('A.15.1.1', 'Política de segurança da informação na cadeia de suprimento', 'Políticas de segurança da informação devem ser estabelecidas e aplicadas na cadeia de suprimento de acordo com o tipo de acordos de negócio', 'A.15 - Relacionamento na Cadeia de Suprimento'),
        ('A.15.1.2', 'Controles de segurança em acordos de cadeia de suprimento', 'Acordos com fornecedores devem incluir requisitos para abordar os riscos de segurança da informação e dos serviços de segurança associados', 'A.15 - Relacionamento na Cadeia de Suprimento'),
        ('A.15.1.3', 'Processo de gestão de cadeia de suprimento de tecnologia de informação e comunicação', 'Processos e procedimentos devem ser estabelecidos e aplicados para gerenciar segurança da informação e riscos de serviços de segurança associados com uso de serviços de tecnologia de informação e comunicação que são acessados, processados, gerenciados ou comunicados por fornecedores externos', 'A.15 - Relacionamento na Cadeia de Suprimento'),
        ('A.15.2.1', 'Monitoramento e revisão de serviços de fornecedores', 'Organizações devem monitorar, revisar e auditar regularmente prestação de serviços de fornecedores', 'A.15 - Relacionamento na Cadeia de Suprimento'),
        ('A.15.2.2', 'Gestão de mudanças em fornecimento de serviços', 'Mudanças nos fornecimentos de serviços, incluindo manutenção e melhorias de sistemas, processos e procedimentos existentes, devem ser gerenciadas, levando em conta a criticidade dos processos de negócio, sistemas de informação e segurança envolvidos e re-reavaliação de riscos', 'A.15 - Relacionamento na Cadeia de Suprimento'),
        
        # A.16 - Gestão de Incidente de Segurança da Informação
        ('A.16.1.1', 'Responsabilidades e procedimentos', 'Funcionalidades de gestão e responsabilidades de gestão de incidentes de segurança da informação devem ser estabelecidas e aplicadas de acordo com políticas de segurança da informação da organização', 'A.16 - Gestão de Incidente de Segurança da Informação'),
        ('A.16.1.2', 'Reportar eventos de segurança da informação', 'Eventos de segurança da informação devem ser reportados através de canais de comunicação apropriados da gestão o mais rapidamente possível', 'A.16 - Gestão de Incidente de Segurança da Informação'),
        ('A.16.1.3', 'Reportar fraquezas de segurança da informação', 'Fraquezas de segurança da informação devem ser reportadas e corrigidas', 'A.16 - Gestão de Incidente de Segurança da Informação'),
        ('A.16.1.4', 'Análise e decisão sobre eventos de segurança da informação', 'Eventos de segurança da informação devem ser avaliados e decididos se devem ser classificados como incidentes de segurança da informação', 'A.16 - Gestão de Incidente de Segurança da Informação'),
        ('A.16.1.5', 'Resposta a incidentes de segurança da informação', 'Respostas a incidentes de segurança da informação devem ser coordenadas de acordo com procedimentos documentados', 'A.16 - Gestão de Incidente de Segurança da Informação'),
        ('A.16.1.6', 'Aprendizado com incidentes de segurança da informação', 'Conhecimento obtido de análise e resolução de incidentes de segurança da informação deve ser usado para reduzir a probabilidade ou impacto de futuros incidentes', 'A.16 - Gestão de Incidente de Segurança da Informação'),
        ('A.16.1.7', 'Coleção de evidências', 'Organizações devem definir e aplicar procedimentos para identificação, coleta, aquisição e preservação de informações que podem servir como evidências', 'A.16 - Gestão de Incidente de Segurança da Informação'),
        
        # A.17 - Aspectos da Segurança da Informação na Gestão de Continuidade de Negócio
        ('A.17.1.1', 'Planejamento de continuidade de segurança da informação', 'A organização deve determinar seus requisitos de continuidade de segurança da informação considerando requisitos de continuidade de negócio', 'A.17 - Gestão de Continuidade de Negócio'),
        ('A.17.1.2', 'Implementação de continuidade de segurança da informação', 'A organização deve estabelecer, documentar, implementar e manter processos, procedimentos e controles para garantir o nível requerido de continuidade de segurança da informação durante uma situação adversa', 'A.17 - Gestão de Continuidade de Negócio'),
        ('A.17.1.3', 'Verificar, revisar e avaliar continuidade de segurança da informação', 'A organização deve verificar regularmente os controles de continuidade de segurança da informação estabelecidos e implementados para garantir que são válidos e eficazes durante uma situação adversa', 'A.17 - Gestão de Continuidade de Negócio'),
        ('A.17.2.1', 'Disponibilidade de instalações de processamento de informação', 'Instalações de processamento de informação devem ser implementadas com redundância suficiente para atender requisitos de disponibilidade', 'A.17 - Gestão de Continuidade de Negócio'),
        
        # A.18 - Conformidade / Compliance
        ('A.18.1.1', 'Identificação de legislação e requisitos contratuais aplicáveis', 'Todas as legislações estatutárias, regulamentares e requisitos contratuais relevantes e abordagem da organização para atender a esses requisitos devem ser explicitamente identificados, documentados e mantidos atualizados para cada sistema de informação e organização', 'A.18 - Conformidade / Compliance'),
        ('A.18.1.2', 'Propriedade intelectual', 'Propriedade intelectual adequada deve ser implementada', 'A.18 - Conformidade / Compliance'),
        ('A.18.1.3', 'Proteção de registros organizacionais', 'Registros devem ser protegidos contra perda, destruição, falsificação, acesso não autorizado e liberação não autorizada, em conformidade com requisitos legislativos, regulamentares, contratuais e de negócios', 'A.18 - Conformidade / Compliance'),
        ('A.18.1.4', 'Privacidade e proteção de informações pessoais identificáveis', 'Privacidade e proteção de informações pessoais identificáveis devem ser asseguradas conforme exigido em legislação e regulamentação relevantes quando aplicável', 'A.18 - Conformidade / Compliance'),
        ('A.18.1.5', 'Regulamentação sobre controles criptográficos', 'Controles criptográficos devem ser usados em conformidade com todas as leis, regulamentos e acordos relevantes', 'A.18 - Conformidade / Compliance'),
        ('A.18.2.1', 'Revisão independente de segurança da informação', 'A abordagem da organização para gerenciar segurança da informação e sua implementação devem ser revisadas independentemente em intervalos planejados ou quando mudanças significativas ocorrerem', 'A.18 - Conformidade / Compliance'),
        ('A.18.2.2', 'Conformidade com políticas de segurança e padrões', 'A conformidade com políticas, regras e padrões de segurança da informação deve ser verificada regularmente', 'A.18 - Conformidade / Compliance'),
        ('A.18.2.3', 'Análise técnica de conformidade', 'Sistemas de informação devem ser verificados regularmente para conformidade com políticas e padrões de segurança da informação da organização', 'A.18 - Conformidade / Compliance'),
    ]
    
    c.execute('SELECT COUNT(*) FROM controles')
    if c.fetchone()[0] == 0:
        c.executemany('''
            INSERT INTO controles (codigo, titulo, descricao, categoria)
            VALUES (?, ?, ?, ?)
        ''', controles_padrao)
    
    conn.commit()
    conn.close()

@app.route('/')
@login_required
def index():
    """Dashboard principal"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Estatísticas
    c.execute('SELECT COUNT(*) FROM controles WHERE status = "Implementado"')
    controles_implementados = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM controles')
    total_controles = c.fetchone()[0]
    
    # Estatísticas de obrigatórios vs boas práticas
    c.execute('SELECT COUNT(*) FROM controles WHERE obrigatorio = 1')
    total_obrigatorios = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM controles WHERE (obrigatorio = 0 OR obrigatorio IS NULL)')
    total_boas_praticas = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM controles WHERE obrigatorio = 1 AND status = "Implementado"')
    obrigatorios_implementados = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM controles WHERE (obrigatorio = 0 OR obrigatorio IS NULL) AND status = "Implementado"')
    boas_praticas_implementadas = c.fetchone()[0]
    
    # Calcular porcentagens
    perc_obrigatorios = (total_obrigatorios / total_controles * 100) if total_controles > 0 else 0
    perc_boas_praticas = (total_boas_praticas / total_controles * 100) if total_controles > 0 else 0
    perc_obrigatorios_impl = (obrigatorios_implementados / total_obrigatorios * 100) if total_obrigatorios > 0 else 0
    perc_boas_praticas_impl = (boas_praticas_implementadas / total_boas_praticas * 100) if total_boas_praticas > 0 else 0
    
    c.execute('SELECT COUNT(*) FROM nao_conformidades WHERE status = "Aberto"')
    nc_abertas = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM politicas WHERE status = "Aprovada"')
    politicas_aprovadas = c.fetchone()[0]
    
    # Controles por categoria
    c.execute('''
        SELECT categoria, COUNT(*) as total,
               SUM(CASE WHEN status = "Implementado" THEN 1 ELSE 0 END) as implementados
        FROM controles
        GROUP BY categoria
    ''')
    controles_categoria = c.fetchall()
    
    # Estatísticas de módulos
    c.execute('SELECT COUNT(*) FROM modulos WHERE concluido = 1')
    modulos_concluidos = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM modulos')
    total_modulos = c.fetchone()[0]
    
    # Módulos com progresso
    c.execute('SELECT * FROM modulos ORDER BY codigo')
    modulos_rows = c.fetchall()
    modulos_progresso = []
    for modulo_row in modulos_rows:
        modulo = parse_modulo_row(modulo_row)
        mod_codigo = modulo['codigo']
        mod_nome = modulo['nome']
        mod_concluido = modulo['concluido']
        c.execute('SELECT COUNT(*) FROM controles WHERE codigo LIKE ? OR categoria LIKE ?', (f'{mod_codigo}.%', f'Controle {mod_codigo}:%'))
        total_mod = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM controles WHERE (codigo LIKE ? OR categoria LIKE ?) AND status = "Implementado"', (f'{mod_codigo}.%', f'Controle {mod_codigo}:%'))
        impl_mod = c.fetchone()[0]
        percentual_mod = (impl_mod / total_mod * 100) if total_mod > 0 else 0
        modulos_progresso.append({
            'codigo': mod_codigo,
            'nome': mod_nome,
            'concluido': bool(mod_concluido),
            'percentual': round(percentual_mod, 1)
        })
    
    # Estatísticas por norma
    normas_progresso = []
    normas_faltantes = 0
    try:
        c.execute('SELECT * FROM normas ORDER BY codigo')
        normas_rows = c.fetchall()
    except sqlite3.OperationalError:
        # Tabela normas não existe ainda, pular esta seção
        normas_rows = []
    
    for norma_row in normas_rows:
        norma_id, codigo, nome, descricao, tipo, data_criacao = norma_row
        
        # Contar controles da norma
        c.execute('''
            SELECT COUNT(DISTINCT c.id)
            FROM controles c
            INNER JOIN controle_normas cn ON c.id = cn.controle_id
            WHERE cn.norma_id = ?
        ''', (norma_id,))
        total_norma = c.fetchone()[0]
        
        # Contar controles implementados da norma
        c.execute('''
            SELECT COUNT(DISTINCT c.id)
            FROM controles c
            INNER JOIN controle_normas cn ON c.id = cn.controle_id
            WHERE cn.norma_id = ? AND c.status = "Implementado"
        ''', (norma_id,))
        impl_norma = c.fetchone()[0]
        
        # Contar tasks da norma (incluindo compartilhadas)
        c.execute('''
            SELECT COUNT(DISTINCT tc.id)
            FROM tasks_controle tc
            INNER JOIN controles c ON tc.controle_id = c.id
            INNER JOIN controle_normas cn ON c.id = cn.controle_id
            WHERE cn.norma_id = ?
        ''', (norma_id,))
        total_tasks_norma = c.fetchone()[0]
        
        # Contar tasks concluídas
        c.execute('''
            SELECT COUNT(DISTINCT tc.id)
            FROM tasks_controle tc
            INNER JOIN controles c ON tc.controle_id = c.id
            INNER JOIN controle_normas cn ON c.id = cn.controle_id
            WHERE cn.norma_id = ? AND tc.concluido = 1
        ''', (norma_id,))
        tasks_concluidas_norma = c.fetchone()[0]
        
        percentual_norma = (impl_norma / total_norma * 100) if total_norma > 0 else 0
        percentual_tasks = (tasks_concluidas_norma / total_tasks_norma * 100) if total_tasks_norma > 0 else 0
        
        # Considerar norma como faltante se não tiver 100% dos controles implementados
        if percentual_norma < 100:
            normas_faltantes += 1
        
        normas_progresso.append({
            'id': norma_id,
            'codigo': codigo,
            'nome': nome,
            'descricao': descricao,
            'tipo': tipo,
            'total_controles': total_norma,
            'controles_implementados': impl_norma,
            'percentual': round(percentual_norma, 1),
            'total_tasks': total_tasks_norma,
            'tasks_concluidas': tasks_concluidas_norma,
            'percentual_tasks': round(percentual_tasks, 1),
            'completa': percentual_norma == 100
        })
    
    # Contar tasks compartilhadas (tasks que aparecem em múltiplas normas)
    tasks_compartilhadas_count = 0
    try:
        c.execute('''
            SELECT COUNT(*)
            FROM (
                SELECT tn.task_id
                FROM tasks_normas tn
                GROUP BY tn.task_id
                HAVING COUNT(DISTINCT tn.norma_id) > 1
            )
        ''')
        tasks_compartilhadas_count = c.fetchone()[0] or 0
    except sqlite3.OperationalError:
        # Tabela não existe ainda
        pass
    
    conn.close()
    
    return render_template('dashboard.html', 
                         controles_implementados=controles_implementados,
                         total_controles=total_controles,
                         nc_abertas=nc_abertas,
                         politicas_aprovadas=politicas_aprovadas,
                         controles_categoria=controles_categoria,
                         modulos_concluidos=modulos_concluidos,
                         total_modulos=total_modulos,
                         modulos_progresso=modulos_progresso,
                         total_obrigatorios=total_obrigatorios,
                         total_boas_praticas=total_boas_praticas,
                         obrigatorios_implementados=obrigatorios_implementados,
                         boas_praticas_implementadas=boas_praticas_implementadas,
                         perc_obrigatorios=round(perc_obrigatorios, 1),
                         perc_boas_praticas=round(perc_boas_praticas, 1),
                         perc_obrigatorios_impl=round(perc_obrigatorios_impl, 1),
                         perc_boas_praticas_impl=round(perc_boas_praticas_impl, 1),
                         normas_progresso=normas_progresso,
                         normas_faltantes=normas_faltantes,
                         total_normas=len(normas_progresso),
                         tasks_compartilhadas_count=tasks_compartilhadas_count)

@app.route('/controles')
@login_required
def controles():
    """Lista de controles"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Parâmetros de filtro
    filtro_tipo = request.args.get('tipo', '')  # 'obrigatorio' ou 'boas_praticas'
    filtro_status = request.args.get('status', '')
    filtro_categoria = request.args.get('categoria', '')
    filtro_grupo = request.args.get('grupo', '')
    filtro_norma = request.args.get('norma', '')
    busca = request.args.get('busca', '')
    
    # Construir query com filtros
    if filtro_norma:
        # Se filtro por norma, usar JOIN
        query = '''
            SELECT DISTINCT c.* 
            FROM controles c
            INNER JOIN controle_normas cn ON c.id = cn.controle_id
            WHERE cn.norma_id = ?
        '''
        params = [filtro_norma]
    else:
        query = 'SELECT * FROM controles WHERE 1=1'
        params = []
    
    if filtro_tipo == 'obrigatorio':
        query += ' AND obrigatorio = 1'
    elif filtro_tipo == 'boas_praticas':
        query += ' AND (obrigatorio = 0 OR obrigatorio IS NULL)'
    
    if filtro_status:
        query += ' AND status = ?'
        params.append(filtro_status)
    
    if filtro_categoria:
        query += ' AND categoria LIKE ?'
        params.append(f'%{filtro_categoria}%')
    
    if filtro_grupo:
        query += ' AND grupo_implementacao LIKE ?'
        params.append(f'%{filtro_grupo}%')
    
    if busca:
        query += ' AND (codigo LIKE ? OR titulo LIKE ? OR descricao LIKE ?)'
        busca_param = f'%{busca}%'
        params.extend([busca_param, busca_param, busca_param])
    
    query += ' ORDER BY codigo'
    
    c.execute(query, params)
    controles = c.fetchall()
    
    # Buscar categorias e grupos únicos para filtros
    c.execute('SELECT DISTINCT categoria FROM controles WHERE categoria IS NOT NULL AND categoria != "" ORDER BY categoria')
    categorias = [row[0] for row in c.fetchall()]
    
    c.execute('SELECT DISTINCT grupo_implementacao FROM controles WHERE grupo_implementacao IS NOT NULL AND grupo_implementacao != "" ORDER BY grupo_implementacao')
    grupos = [row[0] for row in c.fetchall()]
    
    # Buscar normas para filtro
    try:
        c.execute('SELECT id, codigo, nome FROM normas ORDER BY codigo')
        normas_list = [{'id': row[0], 'codigo': row[1], 'nome': row[2]} for row in c.fetchall()]
    except sqlite3.OperationalError:
        # Tabela normas não existe ainda
        normas_list = []
    
    # Mapear colunas na ordem correta do banco
    # Ordem: id, codigo, titulo, descricao, categoria, status, responsavel, 
    #        data_criacao, data_atualizacao, obrigatorio, grupo_implementacao
    column_names_db = ['id', 'codigo', 'titulo', 'descricao', 'categoria', 
                       'status', 'responsavel', 'data_criacao', 'data_atualizacao',
                       'obrigatorio', 'grupo_implementacao']
    
    controles_dict = []
    for row in controles:
        controle = {}
        for i, col_name in enumerate(column_names_db):
            if i < len(row):
                controle[col_name] = row[i]
            else:
                # Valores padrão para colunas que podem não existir
                controle[col_name] = 0 if col_name == 'obrigatorio' else None
        controles_dict.append(controle)
    
    # Buscar normas para cada controle
    for controle in controles_dict:
        try:
            c.execute('''
                SELECT n.id, n.codigo, n.nome
                FROM normas n
                INNER JOIN controle_normas cn ON n.id = cn.norma_id
                WHERE cn.controle_id = ?
            ''', (controle['id'],))
            controle['normas'] = [{'id': row[0], 'codigo': row[1], 'nome': row[2]} for row in c.fetchall()]
        except sqlite3.OperationalError:
            # Tabela não existe ainda
            controle['normas'] = []
    
    conn.close()
    
    return render_template('controles.html', 
                         controles=controles_dict, 
                         categorias=categorias,
                         grupos=grupos,
                         normas=normas_list,
                         filtro_tipo=filtro_tipo,
                         filtro_status=filtro_status,
                         filtro_categoria=filtro_categoria,
                         filtro_grupo=filtro_grupo,
                         filtro_norma=filtro_norma,
                         busca=busca)

@app.route('/controles/add', methods=['GET', 'POST'])
@login_required
def adicionar_controle():
    """Adicionar novo controle"""
    if request.method == 'POST':
        data = request.get_json()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO controles (codigo, titulo, descricao, categoria, status, responsavel)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['codigo'], data['titulo'], data['descricao'], 
              data['categoria'], data['status'], data.get('responsavel', '')))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    
    return render_template('form_controle.html')

@app.route('/controles/<int:id>/edit', methods=['POST'])
@login_required
def editar_controle(id):
    """Editar controle existente"""
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        UPDATE controles 
        SET codigo=?, titulo=?, descricao=?, categoria=?, status=?, responsavel=?, data_atualizacao=CURRENT_TIMESTAMP
        WHERE id=?
    ''', (data['codigo'], data['titulo'], data['descricao'], 
          data['categoria'], data['status'], data.get('responsavel', ''), id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/controles/<int:id>/delete', methods=['POST'])
@login_required
def deletar_controle(id):
    """Deletar controle"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Deletar anexos relacionados
    c.execute('SELECT nome_arquivo FROM anexos_controles WHERE controle_id = ?', (id,))
    anexos = c.fetchall()
    for anexo in anexos:
        arquivo_path = app.config['UPLOAD_FOLDER'] / anexo[0]
        if arquivo_path.exists():
            arquivo_path.unlink()
    
    c.execute('DELETE FROM anexos_controles WHERE controle_id = ?', (id,))
    c.execute('DELETE FROM controles WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/controles/<int:id>')
@login_required
def controle_detalhe(id):
    """Página de detalhes de um controle com anexos, tasks e documentos"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Buscar controle
    c.execute('SELECT * FROM controles WHERE id = ?', (id,))
    controle_row = c.fetchone()
    
    if not controle_row:
        conn.close()
        return redirect(url_for('controles'))
    
    # Mapear colunas na ordem correta do banco
    column_names_db = ['id', 'codigo', 'titulo', 'descricao', 'categoria', 
                       'status', 'responsavel', 'data_criacao', 'data_atualizacao',
                       'obrigatorio', 'grupo_implementacao']
    controle = dict(zip(column_names_db, controle_row))
    
    # Buscar tasks
    c.execute('SELECT * FROM tasks_controle WHERE controle_id = ? ORDER BY ordem', (id,))
    tasks_rows = c.fetchall()
    tasks_columns = ['id', 'controle_id', 'ordem', 'titulo', 'descricao', 'concluido', 'responsavel', 'data_conclusao', 'data_criacao']
    tasks = [dict(zip(tasks_columns, row)) for row in tasks_rows]
    
    # Calcular progresso das tasks
    total_tasks = len(tasks)
    tasks_concluidas = sum(1 for t in tasks if t['concluido'] == 1)
    progresso_tasks = (tasks_concluidas / total_tasks * 100) if total_tasks > 0 else 0
    
    # Buscar documentos necessários
    c.execute('SELECT * FROM documentos_controle WHERE controle_id = ? ORDER BY obrigatorio DESC, nome_documento', (id,))
    documentos_rows = c.fetchall()
    documentos_columns = ['id', 'controle_id', 'nome_documento', 'tipo_documento', 'descricao', 'obrigatorio', 'template', 'data_criacao']
    documentos = [dict(zip(documentos_columns, row)) for row in documentos_rows]
    
    # Buscar anexos (documentos gerados/uploadados)
    c.execute('SELECT * FROM anexos_controles WHERE controle_id = ? ORDER BY data_upload DESC', (id,))
    anexos_rows = c.fetchall()
    anexos_columns = ['id', 'controle_id', 'nome_arquivo', 'nome_original', 'tamanho', 'tipo', 'descricao', 'data_upload']
    anexos = [dict(zip(anexos_columns, row)) for row in anexos_rows]
    
    # Buscar normas associadas ao controle
    try:
        c.execute('''
            SELECT n.id, n.codigo, n.nome, n.descricao
            FROM normas n
            INNER JOIN controle_normas cn ON n.id = cn.norma_id
            WHERE cn.controle_id = ?
            ORDER BY n.codigo
        ''', (id,))
        normas_controle = [{'id': row[0], 'codigo': row[1], 'nome': row[2], 'descricao': row[3]} for row in c.fetchall()]
    except sqlite3.OperationalError:
        # Tabela não existe ainda
        normas_controle = []
    
    conn.close()
    
    return render_template('controle_detalhe.html', 
                         controle=controle, 
                         tasks=tasks,
                         progresso_tasks=round(progresso_tasks, 1),
                         documentos=documentos,
                         anexos=anexos,
                         normas=normas_controle)

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/controles/<int:id>/upload', methods=['POST'])
@login_required
def upload_anexo(id):
    """Upload de arquivo para um controle"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Nenhum arquivo selecionado'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Tipo de arquivo não permitido'}), 400
    
    # Verificar se o controle existe
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id FROM controles WHERE id = ?', (id,))
    if not c.fetchone():
        conn.close()
        return jsonify({'success': False, 'error': 'Controle não encontrado'}), 404
    
    # Salvar arquivo
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
    unique_filename = f"{id}_{timestamp}{filename}"
    file_path = app.config['UPLOAD_FOLDER'] / unique_filename
    file.save(file_path)
    
    # Salvar informações no banco
    descricao = request.form.get('descricao', '')
    tamanho = file_path.stat().st_size
    tipo = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    c.execute('''
        INSERT INTO anexos_controles (controle_id, nome_arquivo, nome_original, tamanho, tipo, descricao)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id, unique_filename, filename, tamanho, tipo, descricao))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Arquivo enviado com sucesso'})

@app.route('/controles/<int:id>/anexo/<int:anexo_id>/delete', methods=['POST'])
@login_required
def deletar_anexo(id, anexo_id):
    """Deleta um anexo"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Buscar informações do anexo
    c.execute('SELECT nome_arquivo FROM anexos_controles WHERE id = ? AND controle_id = ?', (anexo_id, id))
    anexo = c.fetchone()
    
    if not anexo:
        conn.close()
        return jsonify({'success': False, 'error': 'Anexo não encontrado'}), 404
    
    # Deletar arquivo
    arquivo_path = app.config['UPLOAD_FOLDER'] / anexo[0]
    if arquivo_path.exists():
        arquivo_path.unlink()
    
    # Deletar do banco
    c.execute('DELETE FROM anexos_controles WHERE id = ? AND controle_id = ?', (anexo_id, id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/controles/<int:id>/anexo/<int:anexo_id>/download')
@login_required
def download_anexo(id, anexo_id):
    """Download de um anexo"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT nome_arquivo, nome_original FROM anexos_controles WHERE id = ? AND controle_id = ?', (anexo_id, id))
    anexo = c.fetchone()
    conn.close()
    
    if not anexo:
        return redirect(url_for('controle_detalhe', id=id))
    
    nome_arquivo, nome_original = anexo
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        nome_arquivo,
        as_attachment=True,
        download_name=nome_original
    )

@app.route('/controles/<int:id>/task/<int:task_id>/concluir', methods=['POST'])
@login_required
def concluir_task(id, task_id):
    """Marca uma task como concluída"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Verificar se a task pertence ao controle
    c.execute('SELECT id FROM tasks_controle WHERE id = ? AND controle_id = ?', (task_id, id))
    if not c.fetchone():
        conn.close()
        return jsonify({'success': False, 'error': 'Task não encontrada'}), 404
    
    # Marcar como concluída
    from datetime import date
    c.execute('''
        UPDATE tasks_controle 
        SET concluido = 1, data_conclusao = ?
        WHERE id = ?
    ''', (date.today(), task_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/controles/<int:id>/task/<int:task_id>/reabrir', methods=['POST'])
@login_required
def reabrir_task(id, task_id):
    """Reabre uma task (marca como não concluída)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Verificar se a task pertence ao controle
    c.execute('SELECT id FROM tasks_controle WHERE id = ? AND controle_id = ?', (task_id, id))
    if not c.fetchone():
        conn.close()
        return jsonify({'success': False, 'error': 'Task não encontrada'}), 404
    
    # Marcar como não concluída
    c.execute('''
        UPDATE tasks_controle 
        SET concluido = 0, data_conclusao = NULL
        WHERE id = ?
    ''', (task_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/politicas')
@login_required
def politicas():
    """Lista de políticas"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM politicas ORDER BY codigo')
    politicas = c.fetchall()
    conn.close()
    
    columns = ['id', 'codigo', 'titulo', 'descricao', 'versao', 'status', 'aprovador', 'data_aprovacao', 'data_revisao', 'data_criacao']
    politicas_dict = [dict(zip(columns, row)) for row in politicas]
    
    return render_template('politicas.html', politicas=politicas_dict)

@app.route('/politicas/add', methods=['GET', 'POST'])
@login_required
def adicionar_politica():
    """Adicionar nova política"""
    if request.method == 'POST':
        data = request.get_json()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO politicas (codigo, titulo, descricao, versao, status, aprovador, data_aprovacao, data_revisao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['codigo'], data['titulo'], data['descricao'], 
              data['versao'], data['status'], data.get('aprovador', ''), 
              data.get('data_aprovacao'), data.get('data_revisao')))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    
    return render_template('form_politica.html')

@app.route('/nao-conformidades')
@login_required
def nao_conformidades():
    """Lista de não conformidades"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM nao_conformidades ORDER BY data_criacao DESC')
    ncs = c.fetchall()
    conn.close()
    
    columns = ['id', 'codigo', 'titulo', 'descricao', 'severidade', 'status', 'responsavel', 'acao_corretiva', 'prazo', 'data_criacao', 'data_resolucao']
    ncs_dict = [dict(zip(columns, row)) for row in ncs]
    
    return render_template('nao_conformidades.html', nao_conformidades=ncs_dict)

@app.route('/nao-conformidades/add', methods=['GET', 'POST'])
@login_required
def adicionar_nao_conformidade():
    """Adicionar nova não conformidade"""
    if request.method == 'POST':
        data = request.get_json()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO nao_conformidades (codigo, titulo, descricao, severidade, status, responsavel, acao_corretiva, prazo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['codigo'], data['titulo'], data['descricao'], 
              data['severidade'], data['status'], data.get('responsavel', ''), 
              data.get('acao_corretiva', ''), data.get('prazo')))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    
    return render_template('form_nc.html')

@app.route('/auditorias')
@login_required
def auditorias():
    """Lista de auditorias"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM auditorias ORDER BY data_auditoria DESC')
    auditorias = c.fetchall()
    conn.close()
    
    columns = ['id', 'codigo', 'tipo', 'escopo', 'data_auditoria', 'auditor', 'resultado', 'observacoes', 'data_criacao']
    auditorias_dict = [dict(zip(columns, row)) for row in auditorias]
    
    return render_template('auditorias.html', auditorias=auditorias_dict)

@app.route('/auditorias/add', methods=['GET', 'POST'])
@login_required
def adicionar_auditoria():
    """Adicionar nova auditoria"""
    if request.method == 'POST':
        data = request.get_json()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO auditorias (codigo, tipo, escopo, data_auditoria, auditor, resultado, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['codigo'], data['tipo'], data['escopo'], 
              data['data_auditoria'], data.get('auditor', ''), 
              data.get('resultado', ''), data.get('observacoes', '')))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    
    return render_template('form_auditoria.html')

@app.route('/modulos')
@login_required
def modulos():
    """Lista de módulos com progresso"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Buscar todos os módulos
    c.execute('SELECT * FROM modulos ORDER BY codigo')
    modulos = c.fetchall()
    
    # Calcular progresso para cada módulo
    modulos_com_progresso = []
    for modulo_row in modulos:
        modulo = parse_modulo_row(modulo_row)
        codigo = modulo['codigo']
        mod_id = modulo['id']
        nome = modulo['nome']
        descricao = modulo['descricao']
        concluido = modulo['concluido']
        data_planejada_inicio = modulo['data_planejada_inicio']
        data_planejada_fim = modulo['data_planejada_fim']
        data_inicio = modulo['data_inicio']
        data_conclusao = modulo['data_conclusao']
        observacoes = modulo['observacoes']
        
        # Contar controles do módulo (buscar por código do controle que começa com o código do módulo)
        c.execute('SELECT COUNT(*) FROM controles WHERE codigo LIKE ? OR categoria LIKE ?', (f'{codigo}.%', f'Controle {codigo}:%'))
        total_controles = c.fetchone()[0]
        
        # Contar controles implementados
        c.execute('SELECT COUNT(*) FROM controles WHERE (codigo LIKE ? OR categoria LIKE ?) AND status = "Implementado"', (f'{codigo}.%', f'Controle {codigo}:%'))
        controles_implementados = c.fetchone()[0]
        
        # Calcular percentual
        percentual = (controles_implementados / total_controles * 100) if total_controles > 0 else 0
        
        modulos_com_progresso.append({
            'id': mod_id,
            'codigo': codigo,
            'nome': nome,
            'descricao': descricao,
            'concluido': bool(concluido),
            'data_planejada_inicio': data_planejada_inicio,
            'data_planejada_fim': data_planejada_fim,
            'data_inicio': data_inicio,
            'data_conclusao': data_conclusao,
            'observacoes': observacoes,
            'total_controles': total_controles,
            'controles_implementados': controles_implementados,
            'percentual': round(percentual, 1)
        })
    
    conn.close()
    
    return render_template('modulos.html', modulos=modulos_com_progresso)

@app.route('/modulos/<codigo>')
@login_required
def modulo_detalhe(codigo):
    """Detalhes de um módulo específico com seus controles"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Buscar módulo
    c.execute('SELECT * FROM modulos WHERE codigo = ?', (codigo,))
    modulo = c.fetchone()
    
    if not modulo:
        conn.close()
        return redirect(url_for('modulos'))
    
    modulo_dict = parse_modulo_row(modulo)
    mod_id = modulo_dict['id']
    cod = modulo_dict['codigo']
    nome = modulo_dict['nome']
    descricao = modulo_dict['descricao']
    concluido = modulo_dict['concluido']
    data_planejada_inicio = modulo_dict['data_planejada_inicio']
    data_planejada_fim = modulo_dict['data_planejada_fim']
    data_inicio = modulo_dict['data_inicio']
    data_conclusao = modulo_dict['data_conclusao']
    observacoes = modulo_dict['observacoes']
    
    # Buscar controles do módulo (buscar por código do controle ou categoria)
    c.execute('SELECT * FROM controles WHERE codigo LIKE ? OR categoria LIKE ? ORDER BY codigo', (f'{cod}.%', f'Controle {cod}:%'))
    controles = c.fetchall()
    
    # Mapear colunas na ordem correta do banco
    # Ordem: id, codigo, titulo, descricao, categoria, status, responsavel, 
    #        data_criacao, data_atualizacao, obrigatorio, grupo_implementacao
    column_names_db = ['id', 'codigo', 'titulo', 'descricao', 'categoria', 
                       'status', 'responsavel', 'data_criacao', 'data_atualizacao',
                       'obrigatorio', 'grupo_implementacao']
    
    controles_dict = []
    for row in controles:
        controle = {}
        for i, col_name in enumerate(column_names_db):
            if i < len(row):
                controle[col_name] = row[i]
            else:
                controle[col_name] = 0 if col_name == 'obrigatorio' else None
        controles_dict.append(controle)
    
    # Calcular estatísticas
    total = len(controles)
    implementados = sum(1 for c in controles_dict if c['status'] == 'Implementado')
    percentual = (implementados / total * 100) if total > 0 else 0
    
    # Buscar passos de ação do módulo
    c.execute('SELECT * FROM passos_acao WHERE modulo_codigo = ? ORDER BY ordem', (cod,))
    passos = c.fetchall()
    
    columns_passos = ['id', 'modulo_codigo', 'ordem', 'titulo', 'descricao', 'concluido', 'data_conclusao', 'responsavel']
    passos_dict = [dict(zip(columns_passos, row)) for row in passos]
    
    # Atualizar modulo_dict com valores corretos
    modulo_dict.update({
        'id': mod_id,
        'codigo': cod,
        'nome': nome,
        'descricao': descricao,
        'concluido': bool(concluido),
        'data_planejada_inicio': data_planejada_inicio,
        'data_planejada_fim': data_planejada_fim,
        'data_inicio': data_inicio,
        'data_conclusao': data_conclusao,
        'observacoes': observacoes
    })
    
    conn.close()
    
    return render_template('modulo_detalhe.html', modulo=modulo_dict, controles=controles_dict, 
                         passos=passos_dict, total=total, implementados=implementados, percentual=round(percentual, 1))

@app.route('/modulos/<codigo>/concluir', methods=['POST'])
@login_required
def concluir_modulo(codigo):
    """Marcar módulo como concluído"""
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    from datetime import date
    hoje = date.today().isoformat()
    
    c.execute('''
        UPDATE modulos 
        SET concluido = 1, data_conclusao = ?, observacoes = ?
        WHERE codigo = ?
    ''', (hoje, data.get('observacoes', ''), codigo))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/modulos/<codigo>/reabrir', methods=['POST'])
@login_required
def reabrir_modulo(codigo):
    """Reabrir módulo (desmarcar como concluído)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        UPDATE modulos 
        SET concluido = 0, data_conclusao = NULL
        WHERE codigo = ?
    ''', (codigo,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/modulos/<codigo>/cronograma', methods=['POST'])
@login_required
def atualizar_cronograma(codigo):
    """Atualizar cronograma do módulo"""
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        UPDATE modulos 
        SET data_planejada_inicio = ?, data_planejada_fim = ?, data_inicio = ?
        WHERE codigo = ?
    ''', (data.get('data_planejada_inicio'), data.get('data_planejada_fim'), 
          data.get('data_inicio'), codigo))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/passos/<int:passo_id>/concluir', methods=['POST'])
@login_required
def concluir_passo(passo_id):
    """Marcar passo de ação como concluído"""
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    from datetime import date
    hoje = date.today().isoformat()
    
    c.execute('''
        UPDATE passos_acao 
        SET concluido = 1, data_conclusao = ?, responsavel = ?
        WHERE id = ?
    ''', (hoje, data.get('responsavel', ''), passo_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/passos/<int:passo_id>/reabrir', methods=['POST'])
@login_required
def reabrir_passo(passo_id):
    """Reabrir passo de ação"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        UPDATE passos_acao 
        SET concluido = 0, data_conclusao = NULL
        WHERE id = ?
    ''', (passo_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/cronograma')
@login_required
def cronograma():
    """Página de cronograma geral"""
    from datetime import date
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT * FROM modulos ORDER BY codigo')
    modulos_rows = c.fetchall()
    
    # Converter usando parse_modulo_row para compatibilidade
    modulos_dict = [parse_modulo_row(row) for row in modulos_rows]
    
    conn.close()
    
    today = date.today().isoformat()
    
    return render_template('cronograma.html', modulos=modulos_dict, today=today)

@app.route('/api/stats')
def api_stats():
    """API para estatísticas do dashboard"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    stats = {}
    
    c.execute('SELECT COUNT(*) FROM controles WHERE status = "Implementado"')
    stats['controles_implementados'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM controles')
    stats['total_controles'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM nao_conformidades WHERE status = "Aberto"')
    stats['nc_abertas'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM politicas WHERE status = "Aprovada"')
    stats['politicas_aprovadas'] = c.fetchone()[0]
    
    conn.close()
    
    return jsonify(stats)

if __name__ == '__main__':
    init_db()
    # Em produção, usar gunicorn ao invés de app.run()
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
