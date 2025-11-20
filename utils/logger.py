import logging
import os

LOG_FILE = 'logs/actions.log'
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Создаем отдельный logger для действий
actions_logger = logging.getLogger('actions')
actions_logger.setLevel(logging.DEBUG)

# Создаем handler для файла
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Создаем handler для консоли
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

# Добавляем handlers к logger
actions_logger.addHandler(file_handler)
actions_logger.addHandler(stream_handler)

# Отключаем передачу логов родительским логгерам, чтобы избежать дублирования
actions_logger.propagate = False

def log_action(action):
    actions_logger.info(action)