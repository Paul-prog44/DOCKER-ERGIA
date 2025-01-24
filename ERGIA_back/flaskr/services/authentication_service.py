import hashlib

from werkzeug.exceptions import BadRequest

from flaskr.entities.users.login_request_dto import LoginRequestDTO
from flaskr.mappers.impl.user_mapper import UserMapper
from flaskr.models.user_model import UserModel


class AuthenticationService:

    user_model: UserModel

    def __init__(self):
        self.user_model = UserModel()

    def exec_login(self, login_data: LoginRequestDTO):

        user_data = self.user_model.get_user_by_email(login_data.email)
        if not user_data:
            raise BadRequest('Identifiants incorrects')

        json_password = hashlib.sha256(login_data.password.encode()).hexdigest()
        if (user_data
                and login_data.email == user_data[0]["email"]
                and json_password == user_data[0]["password"]):
            # print(" OK ")
            return user_data, 200

        raise BadRequest('Identifiants incorrects')
    
    def exec_getUser(self, id):

        user_data = self.user_model.get_user(id)
        # print("Tokn", user_data)

        return user_data, 200

        # raise BadRequest('Token Incorrect')
    
    def exec_getUserID(self, email):

        id = self.user_model.get_user_id_by_email(email)
        # print("Id récup", id)

        return id



