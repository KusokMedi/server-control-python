# WebControl - Remote Computer Control System

> **[Читать на русском](README.md)**

Secure remote computer control system via web interface with support for multiple users, roles, and action auditing.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API](#api)
- [Configuration](#configuration)
- [Security](#security)
- [Project Structure](#project-structure)
- [Development](#development)
- [License](#license)

## ✨ Features

### 🔐 Security
- Password hashing (Werkzeug)
- Rate limiting (brute force protection)
- CSRF protection on all forms
- SQL injection protection (SQLAlchemy ORM)
- Audit trail - complete action logging

### 👥 User Management
- Create, edit, delete users
- Role system: **admin** and **user**
- User activation/deactivation
- Password and settings management

### 🌍 Multilingual
- Russian (default)
- English
- Language selection per user
- Easy to add new languages

### 📊 System Monitoring
- CPU, RAM, Disk, Network in real-time
- Resource usage graphs
- Local and external IP

### 🖥️ Process Management
- View all processes
- Kill processes
- Change priority
- Search and sort

### 🪟 Window Management
- List all windows
- Hide/show windows
- Move and resize
- Close windows

### ⌨️ Input Emulation
- Mouse control (move, click, scroll)
- Keyboard control (type text, press keys)
- Get mouse position

### 📸 Screenshots
- Capture current monitor
- Capture all monitors
- Capture selected monitor
- Show cursor on screenshot

### 📋 Clipboard
- Read content
- Write text
- Clear

### 🎥 Screen Streaming
- View screen in real-time
- Select monitor
- Quality settings

### 📝 Logging
- Structured logs (app.log, error.log)
- Log rotation (10MB, 10 files)
- Audit logs in database
- View and download logs (admin only)

## 🚀 Quick Start

### Windows

```cmd
REM 1. Install dependencies
install.bat

REM 2. Initialize database
flask init-db

REM 3. Create administrator
flask create-admin

REM 4. Start application
start.bat
```

### Linux

```bash
# 1. Install dependencies
./install.sh

# 2. Initialize database
flask init-db

# 3. Create administrator
flask create-admin

# 4. Start application
./start.sh
```

Open browser: **http://localhost:5000**

## 📦 Installation

### Requirements

- Python 3.8+
- Windows (for window management features)
- Administrator rights (for some features)

### Step 1: Clone repository

```bash
git clone <repository-url>
cd server-control-python
```

### Step 2: Install dependencies

**Windows:**
```cmd
install.bat
```

**Linux:**
```bash
chmod +x install.sh start.sh clear.sh
./install.sh
```

### Step 3: Start application

```bash
python main.py
```

Open browser: **http://localhost:5000**

On first run, you will see a setup page where you need to create the first administrator.

### Step 4: Create administrator

On the setup page, enter:
- Username (minimum 3 characters)
- Password (minimum 6 characters)
- Confirm password
- Select interface language

After creating the administrator, you will be redirected to the login page.

## 💻 Usage

### Start application

**Development mode:**
```bash
python main.py
```

**Production mode (Windows):**
```cmd
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 main:app
```

**Production mode (Linux):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

### CLI Commands

```bash
# Initialize database
flask init-db

# Create administrator
flask create-admin

# List users
flask list-users
```

### Clear data

Removes database, logs and screenshots:

**Windows:**
```cmd
clear.bat
```

**Linux:**
```bash
./clear.sh
```

## 🔌 API

All API endpoints require authentication. Some require admin role.

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | Login |
| GET | `/logout` | Logout |

### Users (admin only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | List users |
| POST | `/api/users` | Create user |
| PUT | `/api/users/<id>` | Update user |
| DELETE | `/api/users/<id>` | Delete user |
| GET | `/api/users/me` | Current user |

**Example create user:**
```json
POST /api/users
{
  "username": "user1",
  "password": "password123",
  "role": "user",
  "language": "en"
}
```

### Processes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/processes` | List processes |
| POST | `/api/processes/kill` | Kill process |
| POST | `/api/processes/priority` | Change priority |

### Monitoring

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/monitoring` | System stats |

### Windows

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/windows` | List windows |
| POST | `/api/windows/hide` | Hide window |
| POST | `/api/windows/show` | Show window |
| POST | `/api/windows/minimize` | Minimize window |
| POST | `/api/windows/maximize` | Maximize window |
| POST | `/api/windows/close` | Close window |
| POST | `/api/windows/move` | Move window |
| POST | `/api/windows/focus` | Focus window |

### Input

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/input/mouse/position` | Mouse position |
| POST | `/api/input/mouse/move` | Move mouse |
| POST | `/api/input/mouse/click` | Mouse click |
| POST | `/api/input/mouse/scroll` | Scroll |
| POST | `/api/input/keyboard/type` | Type text |
| POST | `/api/input/keyboard/press` | Press key |

### Screenshots

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/monitors` | List monitors |
| POST | `/api/screenshot` | Take screenshot |

**Example screenshot request:**
```json
POST /api/screenshot
{
  "mode": "current",
  "show_cursor": true,
  "cursor_style": "crosshair"
}
```

### Clipboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/clipboard/read` | Read |
| POST | `/api/clipboard/write` | Write |
| POST | `/api/clipboard/clear` | Clear |

### Logs (admin only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/logs` | Application logs |
| GET | `/api/logs/audit` | Audit logs |
| GET | `/api/logs/download` | Download logs |
| POST | `/api/logs/clear` | Clear logs |

### Streaming

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/monitors` | List monitors |
| POST | `/api/stream` | Get frame |

## ⚙️ Configuration

### Environment variables (.env)

```env
# Flask
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
FLASK_DEBUG=False

# Server
HOST=0.0.0.0
PORT=5000

# Database
DATABASE_URL=sqlite:///webcontrol.db

# Security
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=3600

# Rate Limiting
RATELIMIT_STORAGE_URL=memory://
RATELIMIT_ENABLED=True
```

### Adding new language

1. Create file `translations/xx.yml` (where xx is language code)
2. Copy structure from `ru.yml` or `en.yml`
3. Translate all strings
4. Add language to validation in `api/users.py`

## 🔒 Security

### Implemented measures

- ✅ Password hashing (Werkzeug)
- ✅ Rate limiting (5 login attempts/minute)
- ✅ CSRF protection on all forms
- ✅ SQL injection impossible (SQLAlchemy ORM)
- ✅ HttpOnly cookies
- ✅ Safe logging (no passwords)
- ✅ Audit trail in database

### Recommendations

1. **Use strong SECRET_KEY** - generate random key
2. **HTTPS** - use HTTPS in production
3. **Firewall** - restrict port access
4. **Strong passwords** - require complex passwords
5. **Regular updates** - update dependencies
6. **Audit** - check logs regularly

### Rate Limiting

- Login: **5 attempts per minute**
- API: **200 requests per day, 50 per hour**

## 📁 Project Structure

```
server-control-python/
├── api/                    # API endpoints
│   ├── clipboard.py
│   ├── control.py
│   ├── input.py
│   ├── logs.py
│   ├── monitoring.py
│   ├── processes.py
│   ├── screenshots.py
│   ├── users.py
│   └── windows.py
├── static/                 # Static files
│   ├── css/
│   ├── js/
│   ├── images/
│   └── screenshots/
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── 404.html
├── translations/           # Translations
│   ├── ru.yml
│   └── en.yml
├── utils/                  # Utilities and modules
│   ├── api_utils.py
│   ├── auth.py
│   ├── cli.py
│   ├── config.py
│   ├── i18n.py
│   ├── logger.py
│   ├── models.py
│   └── system_utils.py
├── logs/                   # Logs
├── main.py                 # Main file
├── run.py                  # Alternative run
├── requirements.txt        # Dependencies
├── .env.example            # Configuration example
├── install.bat / .sh       # Installation
├── start.bat / .sh         # Start
├── clear.bat / .sh         # Clear data
└── README.md
```

## 🛠️ Development

### Adding new API endpoint

1. Create function in appropriate file in `api/`
2. Add decorators `@require_auth` or `@require_role('admin')`
3. Use `@handle_errors` for error handling
4. Add `log_audit()` for important actions

**Example:**
```python
@my_bp.route('/my-endpoint', methods=['POST'])
@require_auth
@handle_errors
def my_endpoint():
    data = request.get_json()
    # Your code
    log_audit('my_action', 'Description')
    return jsonify({'success': True})
```

### Adding new model

1. Add class to `utils/models.py`
2. Run `flask init-db` to create tables

### Testing

```bash
# Run in development mode
export FLASK_DEBUG=True
python main.py
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🤝 Support

For questions and suggestions, create an issue in the repository.

---

**WebControl** - Full control of your computer through browser 🚀
