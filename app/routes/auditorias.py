"""Rotas de auditorias"""

from flask import Blueprint, render_template, request, jsonify
from flask import current_app
from app.utils.decorators import login_required
import sqlite3

bp = Blueprint('auditorias', __name__, url_prefix='/auditorias')

@bp.route('')
@login_required
def listar():
    """Lista de auditorias"""
    conn = sqlite3.connect(current_app.config['DB_PATH'])
    c = conn.cursor()
    c.execute('SELECT * FROM auditorias ORDER BY data_auditoria DESC')
    auditorias = c.fetchall()
    conn.close()
    
    columns = ['id', 'codigo', 'tipo', 'escopo', 'data_auditoria', 'auditor', 'resultado', 'observacoes', 'data_criacao']
    auditorias_dict = [dict(zip(columns, row)) for row in auditorias]
    
    return render_template('auditorias.html', auditorias=auditorias_dict)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def adicionar():
    """Adicionar nova auditoria"""
    if request.method == 'POST':
        data = request.get_json()
        conn = sqlite3.connect(current_app.config['DB_PATH'])
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

