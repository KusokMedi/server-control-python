import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from flask import Flask, render_template, Blueprint, request, redirect, url_for, session, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from api.processes import processes_bp
from api.monitoring import monitoring_bp
from api.windows import windows_bp
from api.input import input_bp
from api.screenshots import screenshots_bp
from api.clipboard import clipboard_bp
from api.logs import logs_bp
from utils.logger import log_action

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'webcontrol_secret_key')
app.config['WTF_CSRF_ENABLED'] = True
app.config['CACHE_TYPE'] = 'simple'
csrf = CSRFProtect(app)
cache = Cache(app)

logger = logging.getLogger(__name__)

# Загрузка пароля
PASSWORD_FILE = 'admin.password'
try:
    with open(PASSWORD_FILE, 'r') as f:
        PASSWORD = f.read().strip()
    if not PASSWORD:
        raise ValueError("Password file is empty")
except FileNotFoundError:
    logger.error(f"Password file '{PASSWORD_FILE}' not found. Please create it with a password.")
    PASSWORD = None
except Exception as e:
    logger.error(f"Error reading password: {e}")
    PASSWORD = None

# Регистрация blueprints
app.register_blueprint(processes_bp, url_prefix='/api')
app.register_blueprint(monitoring_bp, url_prefix='/api')
app.register_blueprint(windows_bp, url_prefix='/api')
app.register_blueprint(input_bp, url_prefix='/api')
app.register_blueprint(screenshots_bp, url_prefix='/api')
app.register_blueprint(clipboard_bp, url_prefix='/api')
app.register_blueprint(logs_bp, url_prefix='/api')

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if PASSWORD and password == PASSWORD:
            session['logged_in'] = True
            log_action("User logged in successfully")
            return redirect(url_for('index'))
        log_action("Invalid login attempt")
        return render_template('login.html', error='Неверный пароль')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    log_action("User logged out")
    return redirect(url_for('login'))

@app.route('/processes')
def processes():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/monitoring')
def monitoring():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/windows')
def windows():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/input')
def input_page():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/screenshots')
def screenshots():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/clipboard')
def clipboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logs')
def logs():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {e}")
    return render_template('404.html', error='Внутренняя ошибка сервера'), 500

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=debug_mode)