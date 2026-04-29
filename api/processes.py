from flask import Blueprint, request, jsonify
import psutil
import logging
from utils.auth import require_auth, log_audit
from utils.api_utils import handle_errors

logger = logging.getLogger(__name__)
processes_bp = Blueprint('processes', __name__)

@processes_bp.route('/processes', methods=['GET'])
@require_auth
@handle_errors
def list_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cpu_percent', 'memory_percent']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'exe': proc.info['exe'],
                'cpu': round(proc.info['cpu_percent'], 2),
                'memory': round(proc.info['memory_percent'], 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    logger.info(f"Listed {len(processes)} processes")
    return jsonify(processes)

@processes_bp.route('/processes/kill', methods=['POST'])
@require_auth
@handle_errors
def kill_process():
    data = request.get_json()
    if not data or 'pid' not in data:
        raise ValueError('Missing pid')
    
    pid = int(data['pid'])
    proc = psutil.Process(pid)
    proc_name = proc.name()
    proc.kill()
    
    logger.info(f"Process {pid} killed")
    log_audit('process_killed', f'PID: {pid}, Name: {proc_name}')
    return jsonify({'success': True})

@processes_bp.route('/processes/priority', methods=['POST'])
@require_auth
@handle_errors
def set_priority():
    data = request.get_json()
    if not data or 'pid' not in data or 'priority' not in data:
        raise ValueError('Missing pid or priority')
    
    pid = int(data['pid'])
    priority = int(data['priority'])
    proc = psutil.Process(pid)
    proc.nice(priority)
    
    logger.info(f"Process {pid} priority set to {priority}")
    log_audit('process_priority_changed', f'PID: {pid}, Name: {proc.name()}, Priority: {priority}')
    return jsonify({'success': True})