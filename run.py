#!/usr/bin/env python3
"""
Ponto de entrada da aplicação
"""

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Em produção, usar gunicorn ao invés de app.run()
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

