from flaskr.database import db_singleton
import hashlib

from flaskr.entities.users.create_user_request_dto import CreateUserRequestDTO
from flaskr.entities.users.delete_user_request_dto import DeleteUserRequestDTO

class UserModel():

    def get_all_users(self):
        query = "SELECT * FROM users;"
        return db_singleton.execute_query(query)

    def get_user(self,user_id):
        query = "SELECT * FROM users WHERE id_user = %s;"
        return db_singleton.execute_query(query, (user_id,))

    def get_user_by_email(self,email):
        query = "SELECT * FROM users WHERE email = %s;"
        return db_singleton.execute_query(query, (email,))


    def get_user_id_by_email(self,email):
        query = "SELECT id_user FROM users WHERE email = %s;"
        return db_singleton.execute_query(query, (email,))

    def create_user(self, register_data: CreateUserRequestDTO):
        # Hasher le mot de passe en bytes
        hashed_password = hashlib.sha256(register_data.password.encode()).hexdigest()

        query = """
            INSERT INTO users (lastname, firstname, email, password, accept_cgu)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_user;
        """
        return db_singleton.execute_query(query, (register_data.lastname, register_data.firstname, register_data.email, hashed_password, register_data.acceptCgu))

    def update_user(self, user_id, lastname=None, firstname=None, email=None, password=None):
        updates = []
        params = []

        if lastname is not None:
            updates.append("lastname = %s")
            params.append(lastname)

        if firstname is not None:
            updates.append("firstname = %s")
            params.append(firstname)

        if email is not None:
            updates.append("email = %s")
            params.append(email)

        if password is not None:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            updates.append("password = %s")
            params.append(hashed_password)

        if not updates:
            print("Aucune mise à jour à effectuer.")
            return None
        print("tuple", tuple(params))

        query = f"""
            UPDATE users
            SET {', '.join(updates)}
            WHERE id_user = %s;
        """
        params.append(user_id)

        return db_singleton.execute_query_for_put(query, tuple(params))

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id_user = %s;"
        return db_singleton.execute_query(query, (user_id,))

    def delete_user_by_email(self, delete_data: DeleteUserRequestDTO):
        query = "DELETE FROM users WHERE email = %s;"
        return db_singleton.execute_query(query, (delete_data.email,))

    def update_password(self, user_id, new_password):
        """
        Met à jour le mot de passe de l'utilisateur dans la base de données.
        """
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        query = """
            UPDATE users
            SET password = %s
            WHERE id_user = %s
        """
        db_singleton.execute_query_for_put(query, (hashed_password, user_id))

    def get_password_by_id(self, user_id):
        """
        Récupère le mot de passe hashé d'un utilisateur par son identifiant.
        """
        query = """
            SELECT password
            FROM users
            WHERE id_user = %s
        """
        result = db_singleton.execute_query(query, (user_id,))
        return result[0]['password'] if result else None

