import yaml
import os
from flask import session

_translations = {}

def load_translations():
    """Загрузить все переводы из файлов"""
    global _translations
    translations_dir = 'translations'
    
    for filename in os.listdir(translations_dir):
        if filename.endswith('.yml'):
            lang = filename[:-4]
            with open(os.path.join(translations_dir, filename), 'r', encoding='utf-8') as f:
                _translations[lang] = yaml.safe_load(f)

def get_language():
    """Получить текущий язык пользователя"""
    from utils.auth import get_current_user
    user = get_current_user()
    if user:
        return user.language
    return session.get('language', 'ru')

def t(key, lang=None):
    """Получить перевод по ключу"""
    if not _translations:
        load_translations()
    
    if lang is None:
        lang = get_language()
    
    return _translations.get(lang, {}).get(key, key)

def init_i18n(app):
    """Инициализировать i18n для Flask приложения"""
    load_translations()
    
    @app.context_processor
    def inject_i18n():
        return {'t': t, 'lang': get_language()}
