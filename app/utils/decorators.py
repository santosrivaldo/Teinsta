"""Decorators para autenticação"""

from functools import wraps
from flask import redirect, url_for, session

def login_required(f):
    """Decorator para proteger rotas que requerem autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

