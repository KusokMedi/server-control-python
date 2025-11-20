# WebControl 🖥️

## Introduction 📖

WebControl is a web application for remote computer control through a browser. It provides full access to file management, processes, system monitoring, windows, keyboard/mouse input, screenshots, clipboard, and logs. The project is developed in Python using the Flask framework and is designed for convenient system administration from anywhere with internet access.

The application allows administrators to control a computer without physical access, which is useful for servers, workstations, or home PCs. The interface is intuitive and includes a sidebar navigation for quick access to various modules.

## Key Features ⚡

WebControl offers a wide range of functions for system management:

### File Manager 📁
- Browse file and folder structures
- Create, delete, and rename files and directories
- Edit text files directly in the browser
- Upload and download files
- Run executable files

### Process Management ⚙️
- View list of all running processes
- Terminate processes
- Monitor process status

### System Monitoring 📊
- Real-time CPU, RAM, disk, and network statistics
- Graphical display of load
- System information (OS, version, uptime)

### Window Management 🪟
- View list of open windows
- Hide/show windows
- Minimize/maximize windows
- Move and focus on windows

### Input Simulation ⌨️
- Simulate keyboard key presses
- Control mouse cursor (movements, clicks)
- Useful for task automation

### Screenshots 📸
- Capture screen images
- View and download screenshots
- Automatic saving to screenshots folder

### Clipboard 📋
- Read clipboard contents
- Write text to clipboard
- Clear clipboard

### Logs 📝
- View system action logs
- Filter and search logs
- Automatic recording of all operations

## Project Architecture 🏗️

The project is built with a modular architecture:

- **app.py**: Main Flask application file
- **run.py**: Server startup script
- **api/**: API modules for various functions
  - clipboard.py: Clipboard operations
  - input.py: Input simulation
  - logs.py: Log management
  - monitoring.py: System monitoring
  - processes.py: Process management
  - screenshots.py: Screenshots
  - windows.py: Window management
- **static/**: Static files (CSS, JS, images)
- **templates/**: HTML templates
- **utils/**: Utility modules
  - logger.py: Logging
  - system_utils.py: System utilities
- **logs/**: Logs folder
- **resources/**: Resources (icons, logos)

## Installation 🔧

### Requirements
- Python 3.7+
- Windows (project optimized for Windows)
- Browser for web interface access

### Installation Steps

1. **Clone the repository or download project files:** 📥
   ```
   git clone <repository-url>
   cd server-control-python
   ```

2. **Install dependencies:** 📦
   Open command line in the project folder and run:
   ```
   pip install -r requirements.txt
   ```
   This will install all necessary libraries, including Flask, psutil, and others.

3. **Configure admin password:** 🔑
   Open the `admin.password` file and set the password for interface access. The password should be in the first line of the file.

4. **Run the application:** ▶️
   Use one of the methods:
   - `python run.py`
   - Or double-click `start.bat`

   The application will start on port 5000.

## Configuration ⚙️

### Server Configuration
By default, the server starts on localhost:5000. To change the port or host, edit `run.py`.

### Security
- Use a strong password in `admin.password`
- For production, consider using HTTPS
- Restrict server access through firewall

## Usage 🚀

1. **Access the interface:** 🌐
   Open your browser and go to: http://localhost:5000

2. **Authentication:** 🔐
   Enter the password from the `admin.password` file

3. **Navigation:** 🧭
   Use the sidebar to switch between modules:
   - Files: File system management
   - Processes: View and manage processes
   - Monitoring: System statistics
   - Windows: Window management
   - Input: Keyboard/mouse simulation
   - Screenshots: Screen capture
   - Clipboard: Clipboard operations
   - Logs: View logs

### Usage Examples

#### File Management 📂
- Go to the "Files" section
- Browse the file tree
- Right-click for context menu
- For text editing, select a file and click "Edit"

#### System Monitoring 📈
- The "Monitoring" section displays real-time graphs
- Updates every 5 seconds

#### Screenshots 🖼️
- Click "Take Screenshot" to capture the screen
- Images are saved in static/screenshots/

## API

WebControl provides a REST API for programmatic access:

### Base URL
http://localhost:5000/api/

### Available Endpoints

#### /api/clipboard
- GET: Get clipboard contents
- POST: Set text to clipboard
- DELETE: Clear clipboard

#### /api/input
- POST: Simulate input (keyboard/mouse)

#### /api/logs
- GET: Get logs

#### /api/monitoring
- GET: Get system statistics

#### /api/processes
- GET: List of processes
- DELETE: Terminate process

#### /api/screenshots
- GET: Get screenshot
- POST: Take new screenshot

#### /api/windows
- GET: List of windows
- POST: Window control (show/hide, etc.)

All requests require authentication via the Authorization header.

## Security

- All communications occur via HTTP (use HTTPS for production)
- Password-based authentication
- Logging of all actions for audit
- Recommended to run on local network or with VPN

## Development

### Code Structure
- Follow modular architecture
- Use utils/ for common functions
- Add logging through logger.py

### Adding New Features
1. Create a new module in api/
2. Add route in app.py
3. Update templates and JavaScript

### Testing
- Run `python run.py` for local testing
- Check all modules through the web interface

## License

The project is distributed under the MIT license. See the LICENSE file for details.

## Support

If you encounter issues or have questions:
- Check logs in the logs/ folder
- Ensure all dependencies are installed
- Check firewall settings

## Changelog

### v1.0.0
- First stable version
- Full set of PC control features
- Flask-based web interface