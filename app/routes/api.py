"""Rotas de API"""

from flask import Blueprint, jsonify
from flask import current_app
import sqlite3

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/stats')
def stats():
    """API para estatísticas do dashboard"""
    conn = sqlite3.connect(current_app.config['DB_PATH'])
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

