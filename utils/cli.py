import click
from flask import Flask
from utils.models import db, User
from getpass import getpass

def init_cli(app: Flask):
    @app.cli.command('init-db')
    def init_db():
        """Инициализировать базу данных"""
        db.create_all()
        click.echo('Database initialized.')
    
    @app.cli.command('create-admin')
    def create_admin():
        """Создать администратора"""
        username = click.prompt('Username', type=str)
        
        if User.query.filter_by(username=username).first():
            click.echo(f'User {username} already exists.')
            return
        
        password = getpass('Password: ')
        password_confirm = getpass('Confirm password: ')
        
        if password != password_confirm:
            click.echo('Passwords do not match.')
            return
        
        if len(password) < 6:
            click.echo('Password must be at least 6 characters.')
            return
        
        user = User(username=username, role='admin')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        click.echo(f'Admin user {username} created successfully.')
    
    @app.cli.command('list-users')
    def list_users():
        """Список всех пользователей"""
        users = User.query.all()
        if not users:
            click.echo('No users found.')
            return
        
        click.echo(f"{'ID':<5} {'Username':<20} {'Role':<10} {'Active':<10} {'Created'}")
        click.echo('-' * 70)
        for user in users:
            click.echo(f"{user.id:<5} {user.username:<20} {user.role:<10} {'Yes' if user.is_active else 'No':<10} {user.created_at.strftime('%Y-%m-%d %H:%M')}")
