"""Rotas de não conformidades"""

from flask import Blueprint, render_template, request, jsonify
from flask import current_app
from app.utils.decorators import login_required
import sqlite3

bp = Blueprint('nao_conformidades', __name__, url_prefix='/nao-conformidades')

@bp.route('')
@login_required
def listar():
    """Lista de não conformidades"""
    conn = sqlite3.connect(current_app.config['DB_PATH'])
    c = conn.cursor()
    c.execute('SELECT * FROM nao_conformidades ORDER BY data_criacao DESC')
    ncs = c.fetchall()
    conn.close()
    
    columns = ['id', 'codigo', 'titulo', 'descricao', 'severidade', 'status', 'responsavel', 'acao_corretiva', 'prazo', 'data_criacao', 'data_resolucao']
    ncs_dict = [dict(zip(columns, row)) for row in ncs]
    
    return render_template('nao_conformidades.html', nao_conformidades=ncs_dict)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def adicionar():
    """Adicionar nova não conformidade"""
    if request.method == 'POST':
        data = request.get_json()
        conn = sqlite3.connect(current_app.config['DB_PATH'])
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

