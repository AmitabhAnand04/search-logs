from flask import Blueprint, request, jsonify, current_app
from .services import cosmos_db_service

bp = Blueprint('routes', __name__)

@bp.route('/getLogs', methods=['GET'])
def get_logs():
    user_name = request.args.get('user_name')
    from_time = request.args.get('from_time')
    to_time = request.args.get('to_time')
    prompt = request.args.get('prompt')
    log_type = request.args.get('log_type')

    if not all([user_name, from_time, to_time, log_type]):
        return jsonify({"error": "Missing one or more required parameters"}), 400

    if log_type.upper() == "C":
        container_name = current_app.config['CONVERSATION_LOG_CONTAINER']
        date_field = "convDateTime"
    elif log_type.upper() == "E":
        container_name = current_app.config['CONVERSATION_ERROR_CONTAINER']
        date_field = "errorDateTime"
    else:
        return jsonify({"error": "Invalid log type. Use 'C' for conversation logs and 'E' for error logs."}), 400

    items = cosmos_db_service.query_cosmos_db(container_name, date_field, user_name, from_time, to_time, prompt)

    if items:
        return jsonify(items), 200
    else:
        return jsonify({"message": "No matching records found."}), 200
