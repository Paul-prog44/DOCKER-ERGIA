from datetime import datetime
import logging
from urllib.parse import unquote

from flaskr.database import db_singleton
from flaskr.entities.campaigns.create_campaign_request_dto import CreateCampaignRequestDTO


class CampaignModel():

    def get_all_campaigns(self):
        """ Récupérer toutes les campagnes. """
        connection = db_singleton.get_connection()
        try:
            query = "SELECT * FROM campaigns;"
            return db_singleton.execute_query(query)  # Utilisation de db_singleton
        finally:
            db_singleton.release_connection(connection)


    def get_campaign(self, id_campaign):
        """ Récupérer une campagne par son identifiant. """

        query = "SELECT * FROM campaigns WHERE id_campaign = %s;"
        return db_singleton.execute_query(query, (id_campaign,))  # Utilisation de db_singleton



    def create_campaign(self, data: CreateCampaignRequestDTO):
        """ Créer une nouvelle campagne. """
        query = """
            INSERT INTO campaigns (owner_id, name, status_id, creation_date, date_phase_1, date_phase_2)
            VALUES (%s, %s, %s, %s, %s, %s) returning id_campaign;
        """
        return db_singleton.execute_query(query, (data.owner_id, data.name, data.status_id, datetime.today(), data.date_phase_1, data.date_phase_2))  # Ajout de la date de creation



    def update_campaign(self, id_campaign, name=None, owner_id=None, status_id=None, creation_date=None, date_phase_1=None, date_phase_2=None):
        """ Mettre à jour les propriétés d'une campagne existante. """
        updates = []
        params = []
        if id_campaign is None:
            raise TypeError("Le champ id_campagne ne peut pas etre vide")

        if name is not None:
            updates.append("name = %s")
            params.append(name)

        if owner_id is not None:
            updates.append("owner_id = %s")
            params.append(owner_id)

        if status_id is not None:
            updates.append("status_id = %s")
            params.append(status_id)

        if creation_date is not None:
            updates.append("creation_date = %s")
            params.append(creation_date)

        if date_phase_1 is not None:
            updates.append("date_phase_1 = %s")
            params.append(date_phase_1)

        if date_phase_2 is not None:
            updates.append("date_phase_2 = %s")
            params.append(date_phase_2)

        if not updates:
            print("Aucune mise à jour à effectuer.")
            return None

        query = f"""
            UPDATE campaigns
            SET {', '.join(updates)}
            WHERE id_campaign = %s;
        """
        params.append(id_campaign)

        return db_singleton.execute_query(query, tuple(params))  # Utilisation de db_singleton



    def delete_campaign(self, id_campaign):
        """ Supprimer une campagne par son identifiant. """
        query = "DELETE FROM campaigns WHERE id_campaign = %s;"
        return db_singleton.execute_query(query, (id_campaign,))  # Utilisation de db_singleton


    
    def add_campaign_user(self, campaign_id, user_id):
        """Ajouter un utilisateur à une campagne après vérification."""
            # Vérifier si la campagne existe
        check_campaign_query = """
        SELECT 1 FROM campaigns
        WHERE id_campaign = %s;
        """
        result_campaign_found = db_singleton.execute_query(check_campaign_query, (campaign_id,))

        if not result_campaign_found:  # Si aucune campagne n'est trouvée
            raise ValueError(f"La campagne {campaign_id} n'existe pas.")

        # Vérifier si l'utilisateur existe
        check_user_query = """
        SELECT 1 FROM users 
        WHERE id_user = %s;
        """
        result_user_found = db_singleton.execute_query(check_user_query, (user_id,))

        if not result_user_found:  # Si aucun utilisateur n'est trouvé
            raise ValueError(f"L'utilisateur {user_id} n'existe pas.")

        # Vérifier si l'utilisateur est déjà inscrit à la campaigne
        check_user_in_campaign_query = """
        SELECT 1 FROM campaigns_users
        WHERE campaigns_id_campaign = %s AND users_id_user = %s
        """

        result_user_in_campaign_found = db_singleton.execute_query(check_user_in_campaign_query,(campaign_id,user_id))

        if result_user_in_campaign_found:  # Si utilisateur trouvé dans là campaigne
            raise ValueError(f"L'utilisateur {user_id} est déjà inscrit dans là campagne {campaign_id}")

        # Ajouter l'utilisateur à la campagne
        insert_query = """
        INSERT INTO campaigns_users (campaigns_id_campaign, users_id_user)
        VALUES (%s, %s) RETURNING campaigns_id_campaign, users_id_user;
        """
        return db_singleton.execute_query(insert_query, (campaign_id, user_id))







    def delete_campaign_user(self, campaign_id, user_id):
        """supprimer un utilisateur à une campagne après vérification."""
        connection = db_singleton.get_connection()
        try:
            # Vérifier si la campagne existe
            check_campaign_query = """
            SELECT 1 FROM campaigns
            WHERE id_campaign = %s;
            """
            result_campaign_found = db_singleton.execute_query(check_campaign_query, (campaign_id,))
            
            if not result_campaign_found:  # Si aucune campagne n'est trouvée
                raise ValueError(f"La campagne {campaign_id} n'existe pas.")
            
            # Vérifier si l'utilisateur existe
            check_user_query = """
            SELECT 1 FROM users 
            WHERE id_user = %s;
            """
            result_user_found = db_singleton.execute_query(check_user_query, (user_id,))

            if not result_user_found:  # Si aucun utilisateur n'est trouvé
                raise ValueError(f"L'utilisateur {user_id} n'existe pas.")

            # Vérifier si l'utilisateur est inscrit à la campaigne
            check_user_in_campaign_query = """
            SELECT 1 FROM campaigns_users
            WHERE campaigns_id_campaign = %s AND users_id_user = %s
            """

            result_user_in_campaign_found = db_singleton.execute_query(check_user_in_campaign_query,(campaign_id,user_id))

            if result_user_in_campaign_found:  # Si utilisateur trouvé dans là campaigne
                # Supprimer l'utilisateur de la campagne
                insert_query = """
                DELETE FROM campaigns_users 
                WHERE campaigns_id_campaign = %s AND users_id_user = %s
                """
                db_singleton.execute_query(insert_query, (campaign_id, user_id))
            else:
                raise ValueError(f"L'utilisateur {user_id} n'existe pas dans la campaigne {campaign_id}")

            
            
        finally:
            db_singleton.release_connection(connection)



    def find_campaign_by_name(self, campaign_name):
        connection = db_singleton.get_connection()
        decoded_name = unquote(campaign_name) # permet de transformer les %20 du front en espace
        try:
            

            query = """
            SELECT * 
            FROM campaigns
            WHERE name ILIKE %s;
            """
                    
            result = db_singleton.execute_query(query, (f'%{decoded_name}%',))

            if len(result) == 0:
                raise ValueError(f"La compaigne {campaign_name} n'existe pas.")  # La campagne n'existe pas
            else:  
                return result
        finally:
            db_singleton.release_connection(connection)

    def get_created_campaigns(self, id):
        connection = db_singleton.get_connection()
        try:
            query = "SELECT * FROM campaigns WHERE owner_id = %s;"
            return db_singleton.execute_query(query, (id,)) 
        finally:
            db_singleton.release_connection(connection)

    def get_joined_campaigns(self, id):
        connection = db_singleton.get_connection()
        try:
            query = "SELECT * from campaigns INNER JOIN campaigns_users ON campaigns.id_campaign = campaigns_users.campaigns_id_campaign WHERE users_id_user = %s;"
            return db_singleton.execute_query(query, (id,))  # Utilisation de db_singleton
        finally:
            db_singleton.release_connection(connection)
   
        

    def owner_campaign(self, campaign_id, user_id):
        # Vérifier si l'utilisateur est propriétaire de la campagne
        is_owner_query = """
        SELECT COUNT(*) > 0 AS is_owner
        FROM campaigns
        WHERE id_campaign = %s AND owner_id = %s;
        """
        
        result = db_singleton.execute_query(is_owner_query, (campaign_id, user_id))

        if result:
            return result[0]['is_owner']  # Renvoie True ou False
        else:
            raise ValueError("Campagne ou utilisateur introuvable.")
        
    def status_exists(self, status_id):
        # Vérifier si le statut existe dans la base de données
        query = """
        SELECT 1 FROM statuses
        WHERE id_status = %s;
        """
        result = db_singleton.execute_query(query, (status_id,))
        return bool(result)
    
    def update_campaign_status(self, campaign_id, status_id):
        # Mettre à jour le statut de la campagne
        query = """
        UPDATE campaigns
        SET status_id = %s
        WHERE id_campaign = %s;
        """
        db_singleton.execute_query(query, (status_id, campaign_id))

    def campaign_exists(self, campaign_id):
        # Vérifier si la campagne existe dans la base de données
        query = """
        SELECT 1 FROM campaigns
        WHERE id_campaign = %s;
        """
        result = db_singleton.execute_query(query, (campaign_id,))
        return bool(result)
    

    def get_campagn_ids_by_owners(self, owner_id):
        # requête pour récupérer les campagne du l'utilisateur dont il est propriétaire
        query = """
                SELECT id_campaign 
                FROM campaigns
                WHERE owner_id = %s;
            """
        
        result = db_singleton.execute_query(query, (owner_id,))
        return result
    

    def get_user_on_campagne(self, campagn_id):
        # requête pour récupérer les campagne du l'utilisateur dont il est propriétaire
        query = """
                SELECT users_id_user 
                FROM campaigns_users
                WHERE campaigns_id_campaign = %s;
            """
        
        result = db_singleton.execute_query(query, (campagn_id,))
        return result
    

    def get_status_campagns(self, campagn_id):

        # requête pour récupérer les campagne du l'utilisateur dont il est propriétaire
        query = """
                SELECT status_id 
                FROM campaigns
                WHERE id_campaign = %s;
            """
        
        result = db_singleton.execute_query(query, (campagn_id,))
        return result
    


    def get_nombre_annotateur(self, campagn_id):

        # requête pour récupérer les campagne du l'utilisateur dont il est propriétaire
        query = """
            SELECT COUNT(*) AS nombre_annotateur
            FROM campaigns_users
            WHERE campaigns_id_campaign = %s;
            """
        
        result = db_singleton.execute_query(query, (campagn_id,))
        return result