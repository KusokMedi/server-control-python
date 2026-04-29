import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from utils.models import db, User
from utils.auth import login_user, logout_user, get_current_user, require_auth, log_audit
from utils.logger import setup_logging
from utils.cli import init_cli
from utils.i18n import init_i18n, t
from api import (processes_bp, monitoring_bp, windows_bp, input_bp, 
                 screenshots_bp, clipboard_bp, logs_bp, control_bp, users_bp)

app = Flask(__name__)
app.config.from_object(Config)

# Инициализация расширений
csrf = CSRFProtect(app)
cache = Cache(app)
db.init_app(app)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config['RATELIMIT_STORAGE_URL'],
    enabled=app.config['RATELIMIT_ENABLED']
)

# Настройка логирования
setup_logging(app)

# Инициализация CLI команд
init_cli(app)

# Регистрация blueprints
app.register_blueprint(processes_bp, url_prefix='/api')
app.register_blueprint(monitoring_bp, url_prefix='/api')
app.register_blueprint(windows_bp, url_prefix='/api')
app.register_blueprint(input_bp, url_prefix='/api')
app.register_blueprint(screenshots_bp, url_prefix='/api')
app.register_blueprint(clipboard_bp, url_prefix='/api')
app.register_blueprint(logs_bp, url_prefix='/api')
app.register_blueprint(control_bp, url_prefix='/api')
app.register_blueprint(users_bp, url_prefix='/api')

# Создание таблиц БД при первом запуске
with app.app_context():
    db.create_all()
    # Проверка наличия пользователей
    if User.query.count() == 0:
        app.logger.warning("No users found in database. Please create an admin user using: flask create-admin")

@app.route('/')
@require_auth
def index():
    user = get_current_user()
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            log_audit('login_failed', 'Empty credentials', user_id=None)
            return render_template('login.html', error='Введите имя пользователя и пароль')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.is_active and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        
        log_audit('login_failed', f'Invalid credentials for username: {username}', user_id=None)
        return render_template('login.html', error='Неверное имя пользователя или пароль')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/processes')
@require_auth
def processes():
    return render_template('index.html', user=get_current_user())

@app.route('/monitoring')
@require_auth
def monitoring():
    return render_template('index.html', user=get_current_user())

@app.route('/windows')
@require_auth
def windows():
    return render_template('index.html', user=get_current_user())

@app.route('/input')
@require_auth
def input_page():
    return render_template('index.html', user=get_current_user())

@app.route('/screenshots')
@require_auth
def screenshots():
    return render_template('index.html', user=get_current_user())

@app.route('/clipboard')
@require_auth
def clipboard():
    return render_template('index.html', user=get_current_user())

@app.route('/logs')
@require_auth
def logs():
    return render_template('index.html', user=get_current_user())

@app.route('/control')
@require_auth
def control():
    return render_template('index.html', user=get_current_user())

@app.route('/users')
@require_auth
def users():
    user = get_current_user()
    if user.role != 'admin':
        return redirect(url_for('index'))
    return render_template('index.html', user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    app.logger.error(f"Internal server error: {e}")
    return render_template('404.html', error='Внутренняя ошибка сервера'), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

@app.route('/monitoring')
@require_auth
def monitoring():
    return render_template('index.html', user=get_current_user())

@app.route('/windows')
@require_auth
def windows():
    return render_template('index.html', user=get_current_user())

@app.route('/input')
@require_auth
def input_page():
    return render_template('index.html', user=get_current_user())

@app.route('/screenshots')
@require_auth
def screenshots():
    return render_template('index.html', user=get_current_user())

@app.route('/clipboard')
@require_auth
def clipboard():
    return render_template('index.html', user=get_current_user())

@app.route('/logs')
@require_auth
def logs():
    return render_template('index.html', user=get_current_user())

@app.route('/control')
@require_auth
def control():
    return render_template('index.html', user=get_current_user())

@app.route('/users')
@require_auth
def users():
    user = get_current_user()
    if user.role != 'admin':
        return redirect(url_for('index'))
    return render_template('index.html', user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    app.logger.error(f"Internal server error: {e}")
    return render_template('404.html', error='Внутренняя ошибка сервера'), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port, debug=debug_mode)
