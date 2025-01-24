from flaskr.database import db_singleton

class SummaryModel():

    def get_all_summaries(self):
        """ Récupérer tous les résumés. """
        query = "SELECT * FROM summaries;"
        return db_singleton.execute_query(query)  # Utilisation de db_singleton



    def get_summary(self, id_summary):
        """ Récupérer un résumé par son identifiant. """
        query = "SELECT * FROM summaries WHERE id_summary = %s;"
        return db_singleton.execute_query(query, (id_summary,))  # Utilisation de db_singleton



    def create_summary(self, path, original_text_id, annotator_id, ia_generated):
        """ Créer un nouveau résumé. """
        query = """
            INSERT INTO summaries (path, original_text_id, annotator_id, ia_generated)
            VALUES (%s, %s, %s, %s);
        """
        return db_singleton.execute_query(query, (path, original_text_id, annotator_id, ia_generated))  # Utilisation de db_singleton



    def update_summary(self, id_summary, path=None, original_text_id=None, annotator_id=None, ia_generated=None):
        """ Mettre à jour les propriétés d'un résumé existant. """
        updates = []
        params = []

        if path is not None:
            updates.append("path = %s")
            params.append(path)

        if original_text_id is not None:
            updates.append("original_text_id = %s")
            params.append(original_text_id)

        if annotator_id is not None:
            updates.append("annotator_id = %s")
            params.append(annotator_id)

        if ia_generated is not None:
            updates.append("ia_generated = %s")
            params.append(ia_generated)

        if not updates:
            print("Aucune mise à jour à effectuer.")
            return None

        query = f"""
            UPDATE summaries
            SET {', '.join(updates)}
            WHERE id_summary = %s;
        """
        params.append(id_summary)

        return db_singleton.execute_query(query, tuple(params))  # Utilisation de db_singleton


    def delete_summary(self,id_summary):
        """ Supprimer un résumé par son identifiant. """
        query = "DELETE FROM summaries WHERE id_summary = %s;"
        return db_singleton.execute_query(query, (id_summary,))  # Utilisation de db_singleton
