"""Rotas de autenticação"""

from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import current_app

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == current_app.config['PASSWORD']:
            session['logged_in'] = True
            next_page = request.args.get('next', url_for('dashboard.index'))
            return redirect(next_page)
        else:
            return render_template('login.html', error='Senha incorreta!')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    """Logout"""
    session.pop('logged_in', None)
    return redirect(url_for('auth.login'))

