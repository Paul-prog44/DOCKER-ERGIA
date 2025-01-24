from flaskr.database import db_singleton

class AnnotationModel():

    def get_all_annotations(self):
        """ Récupérer toutes les annotations. """
        query = "SELECT * FROM annotations;"
        return db_singleton.execute_query(query) 


    def get_annotation(self, id_annotation):
        """ Récupérer une annotation par son identifiant. """

        query = "SELECT * FROM annotations WHERE id_annotation = %s;"
        return db_singleton.execute_query(query, (id_annotation,)) 


    def create_annotation(self, scu_id, color, summary_id, index, length, creator):
        """ Créer une nouvelle annotation. """
        query = """
            INSERT INTO annotations (scu_id, color, summary_id, index, length, creator)
            VALUES (%s, %s, %s, %s, %s, %s) returning id_annotation;
        """
        return db_singleton.execute_query(query, (scu_id, color, summary_id, index, length, creator)) 


    def update_annotation(self, id_annotation, scu_id=None, color=None, summary_id=None, index=None, length=None, creator=None):
        """ Mettre à jour les propriétés d'une annotation existante. """
        updates = []
        params = []

        if scu_id is not None:
            updates.append("scu_id = %s")
            params.append(scu_id)

        if color is not None:
            updates.append("color = %s")
            params.append(color)

        if summary_id is not None:
            updates.append("summary_id = %s")
            params.append(summary_id)

        if index is not None:
            updates.append("index = %s")
            params.append(index)

        if length is not None:
            updates.append("length = %s")
            params.append(length)

        if creator is not None:
            updates.append("creator = %s")
            params.append(creator)

        if not updates:
            print("Aucune mise à jour à effectuer.")
            return None

        query = f"""
            UPDATE annotations
            SET {', '.join(updates)}
            WHERE id_annotation = %s;
        """
        params.append(id_annotation)

        return db_singleton.execute_query(query, tuple(params))  # Utilisation de db_singleton


    def delete_annotation(self, id_annotation):
        """ Supprimer une annotation par son identifiant. """

        query = "DELETE FROM annotations WHERE id_annotation = %s;"
        return db_singleton.execute_query(query, (id_annotation,))  # Utilisation de db_singleton

