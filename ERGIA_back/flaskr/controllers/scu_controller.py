from flasgger import swag_from
from flask import request, Blueprint, jsonify

from flaskr.entities.scus.create_scu_request_dto import CreateScuRequestDTO
from flaskr.services.scu_service import ScuService
from flask_jwt_extended import jwt_required

scu_bp = Blueprint('scus', __name__)

scu_service = ScuService()

# @swag_from("../../resources/docs/scus/scus.yml")
@scu_bp.route('/scus',methods=['GET', 'POST'])
@jwt_required()
def scus():
        if request.method == 'GET':
            try:
                scus = scu_service.exec_get_all_scus()
                return scus, 200
            except Exception as e:
                return str(e), 500

        if request.method == 'POST':
            try:
                print("ici")
                scu_data = CreateScuRequestDTO(**request.get_json())
                print(scu_data)
                response = scu_service.exec_create_scu(scu_data)
                return jsonify(response), 201
            except Exception as e:
                return str(e), 500

        return "Wrong request method or missing credentials", 405

