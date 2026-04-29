import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logging(app):
    """Настроить логирование для приложения"""
    
    # Основной логгер приложения
    app_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, 'app.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    ))
    
    # Логгер ошибок
    error_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, 'error.log'),
        maxBytes=10485760,
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s\n%(pathname)s:%(lineno)d\n'
    ))
    
    # Консольный вывод
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s'
    ))
    
    # Настройка root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)
    
    # Настройка Flask logger
    app.logger.addHandler(app_handler)
    app.logger.addHandler(error_handler)
    app.logger.addHandler(console_handler)