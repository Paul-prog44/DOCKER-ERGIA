import hashlib

from werkzeug.exceptions import Conflict, BadRequest, NotFound

from flaskr.entities.users.create_user_request_dto import CreateUserRequestDTO
from flaskr.entities.users.delete_user_request_dto import DeleteUserRequestDTO
from flaskr.entities.users.update_password_request_dto import UpdatePasswordRequestDTO
from flaskr.entities.users.update_user_request_dto import UpdateUserDTO
#from flaskr.exceptions.exceptions import *
from flaskr.models.user_model import UserModel
import re



class RegisterService:

    user_model: UserModel


    def __init__(self):
        self.user_model = UserModel()

    def is_password_valid(self, password, regex_mdp):
        if (len(password) > 8 and re.search(r"[A-Z]", password)
                and re.search(r"[a-z]", password) and re.search(r"\d", password)
                and re.search(regex_mdp, password)):
            return True
        else:
            raise BadRequest(
                "Mot de passe invalide (Taille min. 8 caractères, au moins 1 chiffre, 1 lettre, 1 majuscule, 1 caractère spécial.)")

    def is_email_valid(self, email, regex_email):
        if re.search(regex_email, email):
            return True
        else:
            raise BadRequest("Format du mail invalide")

    def exec_create_user(self, register_data: CreateUserRequestDTO):
        regex_mdp = r"[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};':\",<>\.\?/\\|`~]"
        regex_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


        def is_email_available(email):
            user = self.user_model.get_user_by_email(email)
            if not user:
                return True
            else:
                raise Conflict("Un compte existe déjà à cet email.")

        if (self.is_password_valid(register_data.password, regex_mdp) and self.is_email_valid(register_data.email, regex_email) and is_email_available(register_data.email)):
            response = self.user_model.create_user(register_data)
            user_id = response[0]['id_user']
            return user_id


        raise ValueError("Mot de passe invalide (Taille min. 8 caractères, au moins 1 chiffre, 1 lettre, 1 majuscule, 1 caractère spécial.)")


    def exec_delete_user(self, delete_data: DeleteUserRequestDTO):
        if len(self.user_model.get_user_by_email(delete_data.email)) != 0:
            return self.user_model.delete_user_by_email(delete_data)
        raise NotFound("Aucun compte n'existe à cet email.", 404)

    def exec_update_user(self, user_id, update_dto: UpdateUserDTO):
        regex_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        regex_password = r"[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};':\",<>\.\?/\\|`~]"

        if update_dto.email is not None:
            if len(self.user_model.get_user_by_email(update_dto.email)) != 0:
                raise Conflict("Un compte existe déjà à cet email.")
            if not re.match(regex_email, update_dto.email):
                raise ValueError("Email invalide")

        if update_dto.password is not None:
            if not (len(update_dto.password) > 8 and
                    re.search(r"[A-Z]", update_dto.password) and
                    re.search(r"[a-z]", update_dto.password) and
                    re.search(r"\d", update_dto.password) and
                    re.search(regex_password, update_dto.password)):
                raise ValueError("Mot de passe invalide. Il doit contenir au moins 8 caractères, une majuscule, une minuscule, un chiffre, et un caractère spécial.")

        return self.user_model.update_user(user_id, update_dto.lastname, update_dto.firstname, update_dto.email, update_dto.password)


    def exec_update_user_password(self, user_id, password_data: UpdatePasswordRequestDTO):

        regex_mdp = r"[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};':\",<>\.\?/\\|`~]"
        old_password_hashed = hashlib.sha256(password_data.old_password.encode()).hexdigest()

        current_password_hashed = self.user_model.get_password_by_id(user_id)

        if not current_password_hashed:
            raise NotFound("Utilisateur introuvable.")

        if current_password_hashed != old_password_hashed:
            raise BadRequest("L'ancien mot de passe est incorrect.")

        self.is_password_valid(password_data.new_password, regex_mdp)

        self.user_model.update_password(user_id, password_data.new_password)

        return {"message": "Mot de passe mis à jour avec succès."}


