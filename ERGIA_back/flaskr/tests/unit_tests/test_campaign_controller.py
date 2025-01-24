import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from io import BytesIO
from flaskr.controllers.campaign_controller import campaigns_bp
from werkzeug.datastructures import FileStorage
import os

class TestCampaignController(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(campaigns_bp)
        self.client = self.app.test_client()

  
    def test_create_campaign_without_file(self):
        data = {
            'owner_id': '1',
            'status_id': '1',
            'campaign_name': 'Test Campaign',
            'date_phase_1': '2025-01-01',
            'date_phase_2': '2025-02-01',
        }

        response = self.client.post('/campaigns', data=data, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 400)

    def test_create_campaign_with_invalid_file_type(self):
        data = {
            'owner_id': '1',
            'status_id': '1',
            'campaign_name': 'Test Campaign',
            'date_phase_1': '2025-01-01',
            'date_phase_2': '2025-02-01',
            'file': (BytesIO(b'This is a test text file'), 'test.txt'),
        }

        response = self.client.post('/campaigns', data=data, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 400)

    @patch('flaskr.controllers.campaign_controller.campaign_service.exec_get_all_campaigns')
    def test_get_campaigns(self, mock_exec_get_all_campaigns):
        mock_exec_get_all_campaigns.return_value = [{'id': 1, 'name': 'Test Campaign'}]

        response = self.client.get('/campaigns')
        self.assertEqual(response.status_code, 200)

    @patch('flaskr.controllers.campaign_controller.campaign_service.exec_get_campaign')
    def test_get_campaign(self, mock_exec_get_campaign):
        mock_exec_get_campaign.return_value = {'id': 1, 'name': 'Test Campaign'}

        response = self.client.get('/campaigns/1')
        self.assertEqual(response.status_code, 200)

    @patch('flaskr.controllers.campaign_controller.campaign_service.add_user_to_campaign')
    def test_join_campaign(self, mock_add_user_to_campaign):
        mock_add_user_to_campaign.return_value = {"message": "User added successfully"}, 200

        data = {'campaign_id': 1, 'user_id': 123}
        response = self.client.post('/add_user_to_campaign', json=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User added successfully", response.data)

    @patch('flaskr.controllers.campaign_controller.campaign_service.delete_user_to_campaign')
    def test_quit_campaign(self, mock_delete_user_to_campaign):
        mock_delete_user_to_campaign.return_value = {"message": "User removed successfully"}, 200

        data = {'campaign_id': 1, 'user_id': 123}
        response = self.client.post('/delete_user_to_campaign', json=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User removed successfully", response.data)

    @patch('flaskr.controllers.campaign_controller.campaign_service.campaign_by_name')
    def test_get_campaign_by_name(self, mock_campaign_by_name):
        mock_campaign_by_name.return_value = {'id': 1, 'name': 'Test Campaign'}, 200

        response = self.client.get('/campaignsName/Test Campaign')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Campaign", response.data)

    @patch('flaskr.controllers.campaign_controller.campaign_service.campaigns_owner')
    def test_is_owner_valid(self, mock_campaigns_owner):
        # Test cas où la campagne appartient à l'utilisateur
        mock_campaigns_owner.return_value = True
        response = self.client.get('/campaigns/is_owner', json={"campaign_id": 1, "user_id": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"is_owner": True})

    def test_is_owner_missing_fields(self):
        # Test cas où les champs manquent
        response = self.client.get('/campaigns/is_owner', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Les champs 'campaign_id' et 'user_id' sont obligatoires"})

    @patch('flaskr.controllers.campaign_controller.campaign_service.campaigns_owner')
    def test_is_owner_value_error(self, mock_campaigns_owner):
        # Test cas où une erreur de campagne ou utilisateur introuvable se produit
        mock_campaigns_owner.side_effect = ValueError("Campagne ou utilisateur introuvable")
        response = self.client.get('/campaigns/is_owner', json={"campaign_id": 1, "user_id": 2})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Campagne ou utilisateur introuvable"})

    @patch('flaskr.controllers.campaign_controller.campaign_service.campaigns_owner')
    def test_is_owner_internal_error(self, mock_campaigns_owner):
        # Test cas d'erreur interne
        mock_campaigns_owner.side_effect = Exception("Erreur interne")
        response = self.client.get('/campaigns/is_owner', json={"campaign_id": 1, "user_id": 2})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Une erreur est survenue."})

    @patch('flaskr.controllers.campaign_controller.campaign_service.update_campaign_status')
    def test_update_campaign_status_valid(self, mock_update_campaign_status):
        # Test mise à jour du statut valide
        mock_update_campaign_status.return_value = None
        response = self.client.put('/campaigns/update_status', json={"campaign_id": 1, "status_id": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Le statut de la campagne a été mis à jour avec succès"})

    def test_update_campaign_status_missing_fields(self):
        # Test si les champs sont manquants
        response = self.client.put('/campaigns/update_status', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Les champs 'campaign_id' et 'status_id' sont obligatoires"})

    @patch('flaskr.controllers.campaign_controller.campaign_service.update_campaign_status')
    def test_update_campaign_status_value_error(self, mock_update_campaign_status):
        # Test d'erreur de validation (par exemple, statut ou campagne invalides)
        mock_update_campaign_status.side_effect = ValueError("Statut ou campagne invalides")
        response = self.client.put('/campaigns/update_status', json={"campaign_id": 1, "status_id": 2})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Statut ou campagne invalides"})

    @patch('flaskr.controllers.campaign_controller.campaign_service.update_campaign_status')
    def test_update_campaign_status_internal_error(self, mock_update_campaign_status):
        # Test d'erreur interne
        mock_update_campaign_status.side_effect = Exception("Erreur inattendue")
        response = self.client.put('/campaigns/update_status', json={"campaign_id": 1, "status_id": 2})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Une erreur inattendue s'est produite"})

    @patch('flaskr.controllers.campaign_controller.campaign_service.get_all_campagns_owner')
    def test_campaigns_owner_valid(self, mock_get_all_campagns_owner):
        # Test si la liste des campagnes est récupérée avec succès
        mock_get_all_campagns_owner.return_value = [{"campaign_id": 1, "campaign_name": "Campaign 1"}]
        response = self.client.get('/campaigns/getOwnerCampagn/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"campagne dont vous étes propriétaire": [{"campaign_id": 1, "campaign_name": "Campaign 1"}]})

    def test_campaigns_owner_missing_owner_id(self):
        # Test si le champ owner_id est manquant
        response = self.client.get('/campaigns/getOwnerCampagn/0')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "owner_id est requis"})

    @patch('flaskr.controllers.campaign_controller.campaign_service.get_all_campagns_owner')
    def test_campaigns_owner_value_error(self, mock_get_all_campagns_owner):
        # Test si une erreur se produit lors de la récupération des campagnes
        mock_get_all_campagns_owner.side_effect = ValueError("Propriétaire introuvable")
        response = self.client.get('/campaigns/getOwnerCampagn/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Propriétaire introuvable"})

    @patch('flaskr.controllers.campaign_controller.campaign_service.get_all_campagns_owner')
    def test_campaigns_owner_internal_error(self, mock_get_all_campagns_owner):
        # Test si une erreur interne se produit
        mock_get_all_campagns_owner.side_effect = Exception("Erreur interne")
        response = self.client.get('/campaigns/getOwnerCampagn/1')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Une erreur inattendue s'est produite"})

    @patch('flaskr.controllers.campaign_controller.campaign_service.get_all_user_on_campagn')
    def test_user_subscript_campagn_valid(self, mock_get_all_user_on_campagn):
        # Test récupération des utilisateurs inscrits à une campagne
        mock_get_all_user_on_campagn.return_value = [{"user_id": 1, "user_name": "John Doe"}]
        response = self.client.get('/campaigns/getUserCampagn/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"user_id": 1, "user_name": "John Doe"}])

    def test_user_subscript_campagn_missing_campaign_id(self):
        # Test si le champ campagn_id est manquant
        response = self.client.get('/campaigns/getUserCampagn/0')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "campagn_id est requis"})

    @patch('flaskr.controllers.campaign_controller.campaign_service.get_all_user_on_campagn')
    def test_user_subscript_campagn_value_error(self, mock_get_all_user_on_campagn):
        # Test si une erreur se produit lors de la récupération des utilisateurs
        mock_get_all_user_on_campagn.side_effect = ValueError("Campagne introuvable")
        response = self.client.get('/campaigns/getUserCampagn/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Campagne introuvable"})

    @patch('flaskr.controllers.campaign_controller.campaign_service.get_all_user_on_campagn')
    def test_user_subscript_campagn_internal_error(self, mock_get_all_user_on_campagn):
        # Test si une erreur interne se produit
        mock_get_all_user_on_campagn.side_effect = Exception("Erreur interne")
        response = self.client.get('/campaigns/getUserCampagn/1')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Une erreur inattendue s'est produite"})
    
if __name__ == '__main__':
    unittest.main()
