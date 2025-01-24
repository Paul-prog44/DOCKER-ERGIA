from flasgger import swag_from
from flask import request, Blueprint, jsonify

from flaskr.entities.users.create_user_request_dto import CreateUserRequestDTO
from flaskr.entities.users.delete_user_request_dto import DeleteUserRequestDTO
from flaskr.entities.users.update_password_request_dto import UpdatePasswordRequestDTO
from flaskr.entities.users.update_user_request_dto import UpdateUserDTO
from flaskr.entities.users.user_response_dto import UserResponseDTO
from flaskr.mappers.impl.user_mapper import UserMapper
from flaskr.services.register_service import RegisterService
from flask_jwt_extended import jwt_required
import json

register_bp = Blueprint('register', __name__)

register_service = RegisterService()
mapper = UserMapper()

@swag_from("../../resources/docs/authentication/register.yml")
@register_bp.route('/register', methods=['POST'])
def register() -> json:
    try:
        register_data = CreateUserRequestDTO(**request.get_json())
        reponse = register_service.exec_create_user(register_data)
        return jsonify(reponse), 200
    except ValueError as e:
        print(e)
        return jsonify({"error": "L'email existe déja"}), 409

@swag_from("../../resources/docs/authentication/delete.yml")
@register_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_user() -> json:
    try:
        email = DeleteUserRequestDTO(**request.json)
        register_service.exec_delete_user(email)
        return jsonify({"message": "Utilisateur supprimé avec succès"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@register_bp.route('/register/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    update_dto = UpdateUserDTO(**data)

    try:
        rows_affected = register_service.exec_update_user(user_id, update_dto)

        if rows_affected > 0:
            return jsonify({"message": "Utilisateur mis à jour avec succès."}), 200
        else:
            return jsonify({"message": "Aucune mise à jour effectuée."}), 400
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": "Erreur interne du serveur. Veuillez réessayer plus tard."}), 500


@register_bp.route('/register/password/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_password(user_id):
    try:
        data = request.json
        password_data = UpdatePasswordRequestDTO(
            old_password=data["old_password"],
            new_password=data["new_password"]
        )
        response = register_service.exec_update_user_password(user_id, password_data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

