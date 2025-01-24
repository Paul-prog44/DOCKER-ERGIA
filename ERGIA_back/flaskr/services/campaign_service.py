from werkzeug.exceptions import BadRequest, NotFound

from flaskr.models.campaign_model import CampaignModel
from flaskr.entities.campaigns.create_campaign_request_dto import CreateCampaignRequestDTO
from datetime import datetime
import logging
import json


class CampaignService:

    campaign_model = CampaignModel
    def __init__(self):
        self.campaign_model = CampaignModel()


    def exec_get_all_campaigns(self):
        list_campagnes = self.campaign_model.get_all_campaigns()
        return list_campagnes

    def exec_get_campaign(self, campaign_id):
        campagne = self.campaign_model.get_campaign(campaign_id)
        return campagne
    
    def exec_get_created_campaigns(self, ownerid):
        campagnes = self.campaign_model.get_created_campaigns(ownerid)
        return campagnes
    
    def exec_get_joined_campaigns(self, ownerid):
        campagnes = self.campaign_model.get_joined_campaigns(ownerid)
        return campagnes


    def exec_create_campaign(self, create_campaign_data : CreateCampaignRequestDTO):

        if ((create_campaign_data.date_phase_1 is not None and create_campaign_data.date_phase_1 < datetime.now())
                or (create_campaign_data.date_phase_2 is not None and create_campaign_data.date_phase_2 < datetime.now())):
            raise BadRequest("La date est  invalide")

        if create_campaign_data.date_phase_2 is not None:
            if create_campaign_data.date_phase_2 < datetime.today():
                raise BadRequest("La date est  invalide")

        if create_campaign_data.owner_id is None:

            raise BadRequest("L'id est invalide")

        campaign_id = self.campaign_model.create_campaign(create_campaign_data)
        return campaign_id, 200

    def add_user_to_campaign(self, campaign_id, user_id):
        """Ajouter un utilisateur à une campagne après vérification."""
        # Appeler le modèle pour ajouter l'utilisateur
        self.campaign_model.add_campaign_user(campaign_id, user_id)

        # Si tout s'est bien passé
        return {"message": f"L'utilisateur {user_id} a été ajouté à la campagne {campaign_id}."}



    def delete_user_to_campaign(self, campaign_id, user_id):
        """Ajouter un utilisateur à une campagne après vérification."""
        # Appeler le modèle pour supprimer l'utilisateur
        self.campaign_model.delete_campaign_user(campaign_id, user_id)

        # Si tout s'est bien passé
        return {"message": f"L'utilisateur {user_id} a été supprimé de la campagne {campaign_id}."}, 200

        


    def campaign_by_name(self, campaign_name):
        # Appeler le modèle pour supprimer l'utilisateur
        campaigne = self.campaign_model.find_campaign_by_name(campaign_name)

        if campaigne is None:
            raise NotFound("L'ID entré n'existe pas ou est mal formaté")

        # Si tout s'est bien passé
        return campaigne, 200



    def campaigns_owner(self, campaign_id, user_id):
        # Appeler le modèle pour vérifier la propriété
        return self.campaign_model.owner_campaign(campaign_id, user_id)
    

    def update_campaign_status(self, campaign_id, status_id):
        # Appeler le modèle pour vérifier si la campagne existe
        if not self.campaign_model.campaign_exists(campaign_id):
            raise ValueError(f"La campagne avec l'ID {campaign_id} n'existe pas.")
    
        # Appeler le modèle pour vérifier si le statut existe
        if not self.campaign_model.status_exists(status_id):
            raise ValueError(f"Le statut avec l'ID {status_id} n'existe pas.")

        # Appeler le modèle pour mettre à jour le statut
        self.campaign_model.update_campaign_status(campaign_id, status_id)


    def get_all_campagns_owner(self, owner_id):

        result = self.campaign_model.get_campagn_ids_by_owners(owner_id)

        # Vérifier si le résultat est vide
        if not result:  
            return {"message": "Vous étes propriétaire d'aucune compagne."}
             
        return result  # Retourne la liste si des résultats existent
    
    
    def get_all_user_on_campagn(self, campagn_id):

        # Appeler le modèle pour vérifier si la campagne existe
        if not self.campaign_model.campaign_exists(campagn_id):
            raise ValueError(f"La campagne avec l'ID {campagn_id} n'existe pas.")

        result = self.campaign_model.get_user_on_campagne(campagn_id)

        # Vérifier si le résultat est vide
        if not result:  
            return {"message": "Personne inscrit sur cette campagne."}
        
        # Extraire uniquement les IDs des résultats
        id_user = [row['users_id_user'] for row in result]
        return {"personne inscrite à cette campagne": id_user}
             


    def get_campagns_status(self, campagn_id):

        # Appeler le modèle pour récupérer le status de la campagn
        if not self.campaign_model.campaign_exists(campagn_id):
            raise ValueError(f"La campagne avec l'ID {campagn_id} n'existe pas.")

        # resultat
        result = self.campaign_model.get_status_campagns(campagn_id)
        
        # return le resultat
        return {f"La campagne {campagn_id} à le status ": result}
    


    def get_nbr_annotateur(self, campagn_id):

        # Appeler le modèle pour récupérer le status de la campagn
        if not self.campaign_model.campaign_exists(campagn_id):
            raise ValueError(f"La campagne avec l'ID {campagn_id} n'existe pas.")

        # resultat
        result = self.campaign_model.get_nombre_annotateur(campagn_id)
        
        # return le resultat
        return result


