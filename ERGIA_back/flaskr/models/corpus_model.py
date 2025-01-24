from flaskr.database import db_singleton

class CorpusModel():

    def get_all_texts(self):
        connection = db_singleton.get_connection()
        try:
            query = "SELECT * FROM original_texts;"
            return db_singleton.execute_query(query)
        finally:
            db_singleton.release_connection(connection)

    def get_last_text(self):
        connection = db_singleton.get_connection()
        try:
            query = "SELECT * FROM original_texts ORDER BY id_original_text DESC LIMIT 1;"
            return db_singleton.execute_query(query)
        finally:
            db_singleton.release_connection(connection)

    def add_text(self, path, idCampagne):
        connection = db_singleton.get_connection()
        try:
            query = "INSERT INTO original_texts (path, campaign_id) VALUES (%s, %s) returning id_original_text;"
            return db_singleton.execute_query(query, (path, idCampagne,))
        finally:
            db_singleton.release_connection(connection)
            
        
    def add_summary(self, path, idText, iaGenerated):
        connection = db_singleton.get_connection()
        try:
            query = "INSERT INTO summaries (path, original_text_id, ia_generated) VALUES (%s, %s, %s) returning id_summary;"
            return db_singleton.execute_query(query, (path, idText, iaGenerated))
        finally:
            db_singleton.release_connection(connection)

    def get_summary(self, id):
        connection = db_singleton.get_connection()
        try:
            query = "SELECT * FROM summaries WHERE id_summary = %s;"
            return db_singleton.execute_query(query, (id,))
        finally:
            db_singleton.release_connection(connection)

    def get_text(self, text_id):
        connection = db_singleton.get_connection()
        try:
            query = "SELECT * FROM original_texts WHERE id_original_text = %s;"
            return db_singleton.execute_query(query, (text_id,))
        finally:
            db_singleton.release_connection(connection)
            
    def get_texts_by_campaign_id(self, campaign_id):
        connection = db_singleton.get_connection()
        try:
            query = "SELECT * FROM original_texts WHERE campaign_id = %s;"
            return db_singleton.execute_query(query, (campaign_id,))
        finally:
            db_singleton.release_connection(connection)

    def get_summaries_by_text_id(self, original_text_id):
        connection = db_singleton.get_connection()
        try:
            query = "SELECT * FROM summaries WHERE original_text_id = %s;"
            return db_singleton.execute_query(query, (original_text_id,))
        finally:
            db_singleton.release_connection(connection)