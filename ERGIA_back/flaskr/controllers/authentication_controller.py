import json

from flasgger import swag_from
from flask import request, Blueprint, session, jsonify

from flaskr.entities.users.login_request_dto import LoginRequestDTO
import hashlib

from flaskr.mappers.impl.user_mapper import UserMapper
from flaskr.services.authentication_service import AuthenticationService
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

#test

login_bp = Blueprint('login', __name__)


auth_service = AuthenticationService()
mapper = UserMapper()

# BLUEPRINT
@swag_from("../../resources/docs/authentication/login.yml")
@login_bp.route('/login',methods=['POST'])
def login():
    username = request.json.get('email', None)
    id = auth_service.exec_getUserID(username)
    id = id[0]

    json_data = LoginRequestDTO(**request.get_json())
    reponse = auth_service.exec_login(json_data)
    user_reponse = mapper.map(reponse)
    
    access_token = create_access_token(identity= str(id['id_user']))
    return jsonify(({"token": access_token, "id_user": id['id_user']}))
    
    
@login_bp.route('/user', methods=['GET'])
@jwt_required()
def user_profile():
    id = get_jwt_identity()
    user_data = auth_service.exec_getUser(id)

    if not user_data:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    user_info = mapper.map(user_data)
    # print(user_data)

    return jsonify(user_info), 200