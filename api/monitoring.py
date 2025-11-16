from flask import Blueprint, jsonify
import psutil
import socket
import requests
import logging

logger = logging.getLogger(__name__)
monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/monitoring', methods=['GET'])
def get_stats():
    try:
        cpu = psutil.cpu_percent(interval=1)
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

        # Get external IP
        external_ip = "N/A"
        try:
            response = requests.get('https://api.ipify.org', timeout=5)
            if response.status_code == 200:
                external_ip = response.text.strip()
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
    except Exception as e:
        logger.error(f"Error in monitoring: {e}")
        return jsonify({'error': 'Monitoring error'}), 500