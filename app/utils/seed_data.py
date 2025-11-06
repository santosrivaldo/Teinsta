"""
Script para importar dados padrão no banco de dados
Pode ser executado no início do app ou via comando
"""

import sqlite3
from pathlib import Path

def import_default_data(db_path):
    """Importa dados padrão (módulos, passos e controles) se não existirem"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Verificar e inserir módulos
    c.execute('SELECT COUNT(*) FROM modulos')
    if c.fetchone()[0] == 0:
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
        
        c.executemany('''
            INSERT INTO modulos (codigo, nome, descricao, data_planejada_inicio, data_planejada_fim, data_inicio, data_conclusao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', modulos_padrao)
        
        # Inserir passos de ação padrão
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
        print("✓ Módulos e passos de ação importados")
    
    # Verificar e inserir controles
    c.execute('SELECT COUNT(*) FROM controles')
    total_controles = c.fetchone()[0]
    
    if total_controles == 0:
        # Importar controles padrão da ISO 27001
        try:
            from app.utils.default_controls import get_default_controls
            controles_padrao = get_default_controls()
        except ImportError:
            # Se o módulo não existir, os controles serão importados pelo app.py
            # Não fazer nada aqui para evitar duplicação
            controles_padrao = []
            print("⚠ Módulo default_controls não encontrado. Controles serão importados pelo app.py")
        
        if controles_padrao:
            controles_padrao_com_obrigatorio = [
                (codigo, titulo, descricao, categoria, 0)  # obrigatorio = 0 (boas práticas por padrão)
                for codigo, titulo, descricao, categoria in controles_padrao
            ]
            c.executemany('''
                INSERT INTO controles (codigo, titulo, descricao, categoria, obrigatorio)
                VALUES (?, ?, ?, ?, ?)
            ''', controles_padrao_com_obrigatorio)
            print(f"✓ {len(controles_padrao)} controles importados")
    
    conn.commit()
    conn.close()
    return True

