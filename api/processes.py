from flask import Blueprint, request, jsonify
import psutil
import logging

logger = logging.getLogger(__name__)
processes_bp = Blueprint('processes', __name__)

@processes_bp.route('/processes', methods=['GET'])
def list_processes():
    try:
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
    except Exception as e:
        logger.error(f"Error listing processes: {e}")
        return jsonify({'error': 'Failed to list processes'}), 500

@processes_bp.route('/processes/kill', methods=['POST'])
def kill_process():
    try:
        data = request.get_json()
        if not data or 'pid' not in data:
            return jsonify({'error': 'Missing pid'}), 400
        pid = int(data['pid'])
        proc = psutil.Process(pid)
        proc.kill()
        logger.info(f"Process {pid} killed")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'error': 'Invalid pid'}), 400
    except psutil.NoSuchProcess:
        return jsonify({'error': 'Process not found'}), 404
    except Exception as e:
        logger.error(f"Error killing process {pid}: {e}")
        return jsonify({'error': 'Failed to kill process'}), 500

@processes_bp.route('/processes/priority', methods=['POST'])
def set_priority():
    try:
        data = request.get_json()
        if not data or 'pid' not in data or 'priority' not in data:
            return jsonify({'error': 'Missing pid or priority'}), 400
        pid = int(data['pid'])
        priority = int(data['priority'])
        proc = psutil.Process(pid)
        proc.nice(priority)
        logger.info(f"Process {pid} priority set to {priority}")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'error': 'Invalid pid or priority'}), 400
    except psutil.NoSuchProcess:
        return jsonify({'error': 'Process not found'}), 404
    except Exception as e:
        logger.error(f"Error setting priority for process {pid}: {e}")
        return jsonify({'error': 'Failed to set priority'}), 500