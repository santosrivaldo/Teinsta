"""Rotas de políticas"""

from flask import Blueprint, render_template, request, jsonify
from flask import current_app
from app.utils.decorators import login_required
import sqlite3

bp = Blueprint('politicas', __name__, url_prefix='/politicas')

@bp.route('')
@login_required
def listar():
    """Lista de políticas"""
    conn = sqlite3.connect(current_app.config['DB_PATH'])
    c = conn.cursor()
    c.execute('SELECT * FROM politicas ORDER BY codigo')
    politicas = c.fetchall()
    conn.close()
    
    columns = ['id', 'codigo', 'titulo', 'descricao', 'versao', 'status', 'aprovador', 'data_aprovacao', 'data_revisao', 'data_criacao']
    politicas_dict = [dict(zip(columns, row)) for row in politicas]
    
    return render_template('politicas.html', politicas=politicas_dict)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def adicionar():
    """Adicionar nova política"""
    if request.method == 'POST':
        data = request.get_json()
        conn = sqlite3.connect(current_app.config['DB_PATH'])
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

