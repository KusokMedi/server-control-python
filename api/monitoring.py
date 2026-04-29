from flask import Blueprint, jsonify
import psutil
import socket
import requests
import logging
from utils.auth import require_auth
from utils.api_utils import handle_errors

logger = logging.getLogger(__name__)
monitoring_bp = Blueprint('monitoring', __name__)

# Кеш для внешнего IP
_external_ip_cache = {'ip': None, 'timestamp': 0}

@monitoring_bp.route('/monitoring', methods=['GET'])
@require_auth
@handle_errors
def get_stats():
    import time
    
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    net = psutil.net_io_counters()
    net_in = net.bytes_recv
    net_out = net.bytes_sent

    # Get local IP
    local_ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        logger.warning(f"Failed to get local IP: {e}")

    # Get external IP (кешируем на 5 минут)
    external_ip = "N/A"
    current_time = time.time()
    if _external_ip_cache['ip'] and (current_time - _external_ip_cache['timestamp']) < 300:
        external_ip = _external_ip_cache['ip']
    else:
        try:
            response = requests.get('https://api.ipify.org', timeout=2)
            if response.status_code == 200:
                external_ip = response.text.strip()
                _external_ip_cache['ip'] = external_ip
                _external_ip_cache['timestamp'] = current_time
        except Exception as e:
            logger.warning(f"Failed to get external IP: {e}")

    return jsonify({
        'cpu': cpu,
        'ram': ram,
        'disk': disk,
        'net_in': net_in,
        'net_out': net_out,
        'local_ip': local_ip,
        'external_ip': external_ip
    })