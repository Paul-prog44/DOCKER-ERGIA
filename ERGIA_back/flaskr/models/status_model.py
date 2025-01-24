from flaskr.database import db_singleton

class StatusModel():

    def get_all_statuses(self):
        """ Récupérer tous les statuts. """
        query = "SELECT * FROM statuses;"
        return db_singleton.execute_query(query)  # Utilisation de db_singleton



    def get_status(self, id_status):
        """ Récupérer un statut par son identifiant. """
        query = "SELECT * FROM statuses WHERE id_status = %s;"
        return db_singleton.execute_query(query, (id_status,))  # Utilisation de db_singleton


    def create_status(self, name):
        """ Créer un nouveau statut. """
        query = """
            INSERT INTO statuses (name)
            VALUES (%s);
        """
        return db_singleton.execute_query(query, (name,))  # Utilisation de db_singleton


    def update_status(self, id_status, name=None):
        """ Mettre à jour les propriétés d'un statut existant. """
        updates = []
        params = []

        if name is not None:
            updates.append("name = %s")
            params.append(name)

        if not updates:
            print("Aucune mise à jour à effectuer.")
            return None

        query = f"""
            UPDATE statuses
            SET {', '.join(updates)}
            WHERE id_status = %s;
        """
        params.append(id_status)

        return db_singleton.execute_query(query, tuple(params))  # Utilisation de db_singleton


    def delete_status(self, id_status):
        """ Supprimer un statut par son identifiant. """
        query = "DELETE FROM statuses WHERE id_status = %s;"
        return db_singleton.execute_query(query, (id_status,))  # Utilisation de db_singleton
