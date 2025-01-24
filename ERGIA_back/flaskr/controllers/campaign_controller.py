import logging

from flasgger import swag_from
from flask import request, Blueprint,jsonify , make_response
from pydantic import ValidationError

from flaskr.entities.campaigns.create_campaign_request_dto import CreateCampaignRequestDTO
from flaskr.models.campaign_model import *
import json
import os
import zipfile
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest

from flaskr.services.campaign_service import CampaignService
from flaskr.services.corpus_service import CorpusService
from flaskr.services.original_texts_service import OriginalTextService


campaigns_bp = Blueprint('campaigns', __name__)

campaign_service = CampaignService()

corpus_service = CorpusService()
original_text_service = OriginalTextService()

#Création du fichier au lancement du script
TARGET_DIRECTORY = os.path.expanduser("~/Desktop/CorpusSAE")
os.makedirs(TARGET_DIRECTORY, exist_ok=True)

@swag_from("../../resources/docs/campaigns/createcampaign.yml")
@campaigns_bp.route('/campaigns', methods=['POST'])
@jwt_required()
def create_campaign():
    owner_id = request.form.get('owner_id')
    status_id = request.form.get('status_id')
    campaign_name = request.form.get('campaign_name')
    date_phase_1 = request.form.get('date_phase_1')
    date_phase_2 = request.form.get('date_phase_2')

    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier n'a été envoyé"}), 400
    
    file = request.files['file']

    if not file.filename.endswith('.zip'):
        return jsonify({"error": "Seuls les fichiers .zip sont acceptés"}), 400


    try:
        create_campaign_data = CreateCampaignRequestDTO(
            owner_id=int(owner_id),
            date_phase_1=datetime.strptime(date_phase_1, "%Y-%m-%d") if date_phase_1 else None,
            date_phase_2=datetime.strptime(date_phase_2, "%Y-%m-%d") if date_phase_2 else None,
            name=campaign_name,
            status_id=int(status_id) if status_id else 1
        )
    except ValueError as ve:
        raise ValueError(f"Erreur de format des données : {e}")
    except ValidationError as ve:
        raise ValueError(f"Erreur de validation des données : {ve}")
    
    try:
        campaign_id, status_code = campaign_service.exec_create_campaign(create_campaign_data)

        if (status_code == 200):
            try :
                campaign_id = campaign_id[0]['id_campaign']
                
                temp_zip_path = os.path.join(TARGET_DIRECTORY, file.filename)

                file.save(temp_zip_path)

                corpus_name = os.path.splitext(file.filename)[0]
                extracted_path = os.path.join(TARGET_DIRECTORY, corpus_name)

                with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extracted_path)

                os.remove(temp_zip_path)

                for f in os.scandir((extracted_path+"/"+corpus_name)):
                    print(f"Traitement du dossier {f.path}")
                    files_and_dirs = sorted(os.scandir(f.path), key=lambda x: x.is_dir())
                    if f.is_dir():
                        for file in files_and_dirs:

                            if file.is_file():
                                relative_path = os.path.relpath(file.path, TARGET_DIRECTORY)
                                id_test = corpus_service.exec_addText(relative_path, campaign_id)
                                id_test = id_test[0]["id_original_text"]

                            elif file.is_dir():
                                print(f"Traitement du sous-dossier {file.path}")
                                if file.name == "resume_ia":
                                    for ia in os.scandir(file.path):
                                        if ia.is_dir() == False:
                                            relative_ia_path = os.path.relpath(ia.path, TARGET_DIRECTORY)
                                            corpus_service.exec_addSummary(relative_ia_path, id_test, True)

                                elif file.name == "resume_ref":
                                    for ref in os.scandir(file.path):
                                        if ref.is_dir() == False:
                                            relative_ref_path = os.path.relpath(ref.path, TARGET_DIRECTORY)
                                            corpus_service.exec_addSummary(relative_ref_path, id_test, False)
                return jsonify({
                    "message": "Corpus téléchargé et extrait avec succès",
                    "extracted_path": extracted_path
                }), 201
            except Exception as e:
                print("ERROR", e)
                return {"Error": str(e)}, 400
        
    except Exception as e:
        return {"Error": str(e)}, 400

    

    
    






@swag_from("../../resources/docs/campaigns/getcampaigns.yml")
@campaigns_bp.route('/campaigns', methods=['GET'])
@jwt_required()
def get_campaigns():
        try:
            campaigns = campaign_service.exec_get_all_campaigns()
            return campaigns, 200
        except Exception as e:
            return {'error': e.args}

@swag_from("../../resources/docs/campaigns/getcampaign.yml")
@campaigns_bp.route('/campaigns/<int:campaign_id>', methods=['GET'])
@jwt_required()
def get_campaign(campaign_id):
    try:
        campaigns = campaign_service.exec_get_campaign(campaign_id)
        return campaigns, 200
    except Exception as e:
        return {'error': e.args}


@swag_from("../../resources/docs/campaigns/joincampaign.yml")
@campaigns_bp.route('/add_user_to_campaign', methods=['POST'])
@jwt_required()
def join_campaign():
    
    data = request.get_json()
    print(data)
    # Récupérer les IDs depuis le corps de la requête
    campaign_id = data.get('campaign_id')
    user_id = data.get('user_id')

    if not campaign_id or not user_id:
         raise BadRequest("Les champs 'campaign_id' et 'user_id' sont obligatoires")
    
    result, status_code = campaign_service.add_user_to_campaign(campaign_id, user_id), 200
    
    # Retourner la réponse basée sur le résultat du service
    return jsonify(result), status_code



@swag_from("../../resources/docs/campaigns/unjoincampaign.yml")
@campaigns_bp.route('/delete_user_to_campaign', methods=['POST'])
@jwt_required()
def quit_campaign():
    """
    Service pour retirer un utilisateur d'une campagne.
    """
    data = request.get_json()


    campaign_id = data.get('campaign_id')
    user_id = data.get('user_id')


    if not campaign_id or not user_id:
         raise BadRequest("Les champs 'campaign_id' et 'user_id' sont obligatoires")


    result, status_code = campaign_service.delete_user_to_campaign(campaign_id, user_id)
    
    # Retourner la réponse basée sur le résultat du service
    return jsonify(result), status_code



@swag_from("../../resources/docs/campaigns/campaignbyname.yml")
@campaigns_bp.route('/campaignsName/<string:campaign_name>', methods=['GET'])
@jwt_required()
def get_campaigns_by_name(campaign_name):
    if not campaign_name:
        return jsonify({"error": "Le champ 'campaign_name' est obligatoire"}), 400
    result, status_code = campaign_service.campaign_by_name(campaign_name)
    
    # Retourner la réponse basée sur le résultat du service
    return jsonify(result), status_code

# @swag_from("../../resources/docs/campaigns/createdbyme.yml")
@campaigns_bp.route('/campaigns/created', methods=['GET'])
@jwt_required()
def get_created_campaigns():
    
    id = get_jwt_identity()
    created_campaigns = campaign_service.exec_get_created_campaigns(id)
    
    return jsonify(created_campaigns)

# @swag_from("../../resources/docs/campaigns/joinedcampaigns.yml")
@campaigns_bp.route('/campaigns/joined', methods=['GET'])
@jwt_required()
def get_joined_campaigns():
    
    id = get_jwt_identity()
    joined_campaigns = campaign_service.exec_get_joined_campaigns(id)
    
    return jsonify(joined_campaigns)


@campaigns_bp.route('/campaigns/is_owner', methods=['GET'])
@jwt_required()
def is_owner():
    data = request.get_json()

    campaign_id = data.get('campaign_id')
    user_id = data.get('user_id')

    # Validation des champs
    if campaign_id is None or user_id is None:
        return jsonify({"error": "Les champs 'campaign_id' et 'user_id' sont obligatoires"}), 400

    try:
        # Appeler le service
        is_owner = campaign_service.campaigns_owner(campaign_id, user_id)
        return jsonify({"is_owner": is_owner}), 200
    except ValueError as e:
        # Gérer les erreurs (ex. campagne ou utilisateur introuvable)
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        # Gérer les erreurs inattendues
        return jsonify({"error": "Une erreur est survenue."}), 500
    

@campaigns_bp.route('/campaigns/update_status', methods=['PUT'])
@jwt_required()
def update_campaign_status():
    data = request.get_json()

    # Récupération des données de la requête
    campaign_id = data.get('campaign_id')
    status_id = data.get('status_id')

    # Vérification des données obligatoires
    if campaign_id is None or status_id is None:
        return jsonify({"error": "Les champs 'campaign_id' et 'status_id' sont obligatoires"}), 400

    try:
        # Appel au service pour mettre à jour le statut de la campagne
        campaign_service.update_campaign_status(campaign_id, status_id)
        return jsonify({"message": "Le statut de la campagne a été mis à jour avec succès"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Une erreur inattendue s'est produite"}), 500


@campaigns_bp.route('/campaigns/getOwnerCampagn/<int:owner_id>', methods=['GET'])
@jwt_required()
def campaigns_owner(owner_id):

    if not owner_id:
        return jsonify({"error": "owner_id est requis"}), 400

    try:
        # Appeler le service
        owner_campagne = campaign_service.get_all_campagns_owner(owner_id)
        return jsonify({"campagne dont vous étes propriétaire": owner_campagne}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Une erreur inattendue s'est produite"}), 500
    

@campaigns_bp.route('/campaigns/getUserCampagn/<int:campagn_id>', methods=['GET'])
@jwt_required()
def user_subscript_campagn(campagn_id):

    if not campagn_id:
        return jsonify({"error": "campagn_id est requis"}), 400

    try:
        # Appeler le service
        user_on_campagne = campaign_service.get_all_user_on_campagn(campagn_id)
        return jsonify(user_on_campagne), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Une erreur inattendue s'est produite"}), 500


@campaigns_bp.route('/campaigns/originalTexts/<int:campaign_id>', methods=['GET'])
@jwt_required()
def get_original_texts(campaign_id):
    try:
        original_texts = original_text_service.exec_get_original_texts_by_campaign_id(campaign_id)
        return original_texts, 200
    except Exception as e:
        raise e
    
    
@campaigns_bp.route('/campaigns/getStatusCampagn/<int:campagn_id>', methods=['GET'])
@jwt_required()
def get_status(campagn_id):

    if not campagn_id:
        return jsonify({"error": "campagn_id est requis"}), 400

    try:
        # Appeler le service
        status_campagne = campaign_service.get_campagns_status(campagn_id)
        return jsonify(status_campagne), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Une erreur inattendue s'est produite"}), 500
    



@campaigns_bp.route('/campaigns/nombreAnnotateur/<int:campagn_id>', methods=['GET'])
@jwt_required()
def nbr_annotateur(campagn_id):

    if not campagn_id:
        return jsonify({"error": "campagn_id est requis"}), 400

    try:
        # Appeler le service
        nbr_annotateur = campaign_service.get_nbr_annotateur(campagn_id)
        return jsonify(nbr_annotateur), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Une erreur inattendue s'est produite"}), 500
    
