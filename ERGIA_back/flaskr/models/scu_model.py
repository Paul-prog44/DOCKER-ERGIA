from flaskr.database import db_singleton
from flaskr.entities.scus.create_scu_request_dto import CreateScuRequestDTO


class ScuModel():

    def get_all_scu(self):
        """ Récupérer tous les SCU. """
        query = "SELECT * FROM scus;"
        return db_singleton.execute_query(query) 



    def get_scu(self, id_scu):
        """ Récupérer un SCU par son identifiant. """
        query = "SELECT * FROM scus WHERE id_scu = %s;"
        return db_singleton.execute_query(query, (id_scu,)) 



    def create_scu(self, idea):
        """ Créer un nouveau SCU. """
        query = """
            INSERT INTO scus ("idea", "weight")
            VALUES (%s, %s) returning id_scu;
        """
        return db_singleton.execute_query(query, (idea, 1)) 



    def update_scu(self, id_scu, idea=None, weight=None):
        """ Mettre à jour les propriétés d'un SCU existant. """

        updates = []
        params = []

        if idea is not None:
            updates.append("idea = %s")
            params.append(idea)

        if weight is not None:
            updates.append("weight = %s")
            params.append(weight)

        if not updates:
            print("Aucune mise à jour à effectuer.")
            return None

        query = f"""
            UPDATE scus
            SET {', '.join(updates)}
            WHERE id_scu = %s;
        """
        params.append(id_scu)

        return db_singleton.execute_query(query, tuple(params))


    def delete_scu(self, id_scu):
        """ Supprimer un SCU par son identifiant. """
        query = "DELETE FROM scus WHERE id_scu = %s;"
        return db_singleton.execute_query(query, (id_scu,))

