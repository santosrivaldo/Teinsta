"""Funções auxiliares"""

from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def parse_modulo_row(row):
    """Parse módulo row que pode ter estrutura antiga (8 campos) ou nova (11 campos)"""
    if len(row) == 8:
        # Estrutura antiga
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
        # Estrutura nova
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

