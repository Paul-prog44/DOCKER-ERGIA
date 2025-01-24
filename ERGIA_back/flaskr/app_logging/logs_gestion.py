import json
import time
from ipaddress import ip_address
from venv import create

from flask import g, request, current_app, jsonify


def register_before_request(app):
    @app.before_request
    def start_timer():
        g.start = time.time()

def register_after_request(app, request_logger):
    @app.after_request
    def log_request_info(response):
        duree = (time.time() - g.start) * 1000
        status_code = response.status_code

        if status_code < 400:
            request_log = LogService.format_request_log(request=request, response=response, duration=duree)
            request_logger.info(request_log)
        return response


class LogService():

    @staticmethod
    def format_request_log(request, response, duration):
        log_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "method": request.method,
            "url": request.url,
            "status_code": response.status_code,
            "duration": f"{duration}ms",
            "ip_address": request.remote_addr,
        }
        return json.dumps(log_data)

    @staticmethod
    def format_error_log(request, status_code, error_message, error_type = None, duration = None):
        log_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "method": request.method,
            "url": request.url,
            "status_code": status_code,
            "duration": f"{duration}ms",
            "ip_address": request.remote_addr,
            "error_type": error_type,
            "error_message": error_message,
        }
        return json.dumps(log_data)
