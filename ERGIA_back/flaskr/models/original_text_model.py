from flaskr.database import db_singleton

class OriginalTextModel():

    def get_all_original_texts(self):
        """ Récupérer tous les textes originaux. """
        query = "SELECT * FROM original_texts;"
        return db_singleton.execute_query(query) 


    def get_original_text(self, id_original_text):
        """ Récupérer un texte original par son identifiant. """
        query = "SELECT * FROM original_texts WHERE id_original_text = %s;"
        return db_singleton.execute_query(query, (id_original_text,)) 



    def create_original_text(self, path, campaign_id):
        """ Créer un nouveau texte original. """
        query = """
            INSERT INTO original_texts (path, campaign_id)
            VALUES (%s, %s);
        """
        return db_singleton.execute_query(query, (path, campaign_id))  



    def update_original_text(self, id_original_text, path=None, campaign_id=None):
        """ Mettre à jour les propriétés d'un texte original existant. """
        updates = []
        params = []

        if path is not None:
            updates.append("path = %s")
            params.append(path)

        if campaign_id is not None:
            updates.append("campaign_id = %s")
            params.append(campaign_id)

        if not updates:
            print("Aucune mise à jour à effectuer.")
            return None

        query = f"""
            UPDATE original_texts
            SET {', '.join(updates)}
            WHERE id_original_text = %s;
        """
        params.append(id_original_text)

        return db_singleton.execute_query(query, tuple(params)) 



    def delete_original_text(self, id_original_text):
        """ Supprimer un texte original par son identifiant. """
        query = "DELETE FROM original_texts WHERE id_original_text = %s;"
        return db_singleton.execute_query(query, (id_original_text,))  


    def get_original_text_by_campaign_id(self, campaign_id):
            """ Récupérer les textes par leur numéro de campagne"""
            query = "SELECT * FROM original_texts WHERE campaign_id = %s;"
            return db_singleton.execute_query(query, (campaign_id,)) 