import json
import time

from flask import g, request, jsonify, current_app

from flaskr.app_logging.logs_gestion import LogService


def register_error_handler(app, error_logger):
    @app.errorhandler(Exception)
    def handle_exception(e):
        duration = round((time.time()) - g.get("start_time", time.time())) * 1000
        status_code = e.code if hasattr(e, "code") else 500
        log_data = LogService.format_error_log(
            request=request,
            status_code=status_code,
            error_message=str(e),
            error_type=type(e).__name__,
            duration=duration,
        )
        error_logger.error(log_data)
        return jsonify({"error": e.args}), status_code