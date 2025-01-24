import pytest
from unittest.mock import MagicMock, patch
from werkzeug.exceptions import BadRequest, NotFound
from datetime import datetime, timedelta
from flaskr.services.campaign_service import CampaignService
from flaskr.entities.campaigns.create_campaign_request_dto import CreateCampaignRequestDTO


class TestCampaignService:

    def setup_method(self):
        self.campaign_service = CampaignService()
        self.campaign_service.campaign_model = MagicMock()

    def test_exec_get_all_campaigns(self):
        self.campaign_service.campaign_model.get_all_campaigns.return_value = [{"id": 1, "name": "Campaign 1"}]
        result = self.campaign_service.exec_get_all_campaigns()
        assert result == [{"id": 1, "name": "Campaign 1"}]
        self.campaign_service.campaign_model.get_all_campaigns.assert_called_once()

    def test_exec_get_campaign(self):
        campaign_id = 1
        self.campaign_service.campaign_model.get_campaign.return_value = {"id": 1, "name": "Campaign 1"}
        result = self.campaign_service.exec_get_campaign(campaign_id)
        assert result == {"id": 1, "name": "Campaign 1"}
        self.campaign_service.campaign_model.get_campaign.assert_called_once_with(campaign_id)

    def test_exec_create_campaign_valid(self):
        dto = CreateCampaignRequestDTO(
            name="Campaign 1",
            date_phase_1=datetime.now() + timedelta(days=1),
            date_phase_2=datetime.now() + timedelta(days=2),
            owner_id=1,
        )
        self.campaign_service.campaign_model.create_campaign.return_value = 1
        campaign_id, status = self.campaign_service.exec_create_campaign(dto)
        assert campaign_id == 1
        assert status == 200
        self.campaign_service.campaign_model.create_campaign.assert_called_once_with(dto)

    def test_exec_create_campaign_invalid_date(self):
        dto = CreateCampaignRequestDTO(
            name="Campaign 1",
            date_phase_1=datetime.now() - timedelta(days=1),
            date_phase_2=None,
            owner_id=1,
        )
        with pytest.raises(BadRequest, match="La date est  invalide"):
            self.campaign_service.exec_create_campaign(dto)

    def test_add_user_to_campaign(self):
        campaign_id = 1
        user_id = 2
        result = self.campaign_service.add_user_to_campaign(campaign_id, user_id)
        assert result == {"message": f"L'utilisateur {user_id} a été ajouté à la campagne {campaign_id}."}
        self.campaign_service.campaign_model.add_campaign_user.assert_called_once_with(campaign_id, user_id)

    def test_delete_user_to_campaign(self):
        campaign_id = 1
        user_id = 2
        result, status = self.campaign_service.delete_user_to_campaign(campaign_id, user_id)
        assert result == {"message": f"L'utilisateur {user_id} a été supprimé de la campagne {campaign_id}."}
        assert status == 200
        self.campaign_service.campaign_model.delete_campaign_user.assert_called_once_with(campaign_id, user_id)

    def test_campaign_by_name(self):
        campaign_name = "Test Campaign"
        self.campaign_service.campaign_model.find_campaign_by_name.return_value = {"id": 1, "name": campaign_name}
        result, status = self.campaign_service.campaign_by_name(campaign_name)
        assert result == {"id": 1, "name": campaign_name}
        assert status == 200
        self.campaign_service.campaign_model.find_campaign_by_name.assert_called_once_with(campaign_name)

    def test_campaign_by_name_not_found(self):
        campaign_name = "Nonexistent Campaign"
        self.campaign_service.campaign_model.find_campaign_by_name.return_value = None
        with pytest.raises(NotFound, match="L'ID entré n'existe pas ou est mal formaté"):
            self.campaign_service.campaign_by_name(campaign_name)

    def test_update_campaign_status_valid(self):
        campaign_id = 1
        status_id = 2
        self.campaign_service.campaign_model.campaign_exists.return_value = True
        self.campaign_service.campaign_model.status_exists.return_value = True
        self.campaign_service.update_campaign_status(campaign_id, status_id)
        self.campaign_service.campaign_model.update_campaign_status.assert_called_once_with(campaign_id, status_id)

    def test_update_campaign_status_invalid_campaign(self):
        campaign_id = 1
        status_id = 2
        self.campaign_service.campaign_model.campaign_exists.return_value = False
        with pytest.raises(ValueError, match="La campagne avec l'ID 1 n'existe pas."):
            self.campaign_service.update_campaign_status(campaign_id, status_id)

    def test_update_campaign_status_invalid_status(self):
        campaign_id = 1
        status_id = 2
        self.campaign_service.campaign_model.campaign_exists.return_value = True
        self.campaign_service.campaign_model.status_exists.return_value = False
        with pytest.raises(ValueError, match="Le statut avec l'ID 2 n'existe pas."):
            self.campaign_service.update_campaign_status(campaign_id, status_id)

    def test_get_all_user_on_campagn_no_users(self):
        campaign_id = 1
        self.campaign_service.campaign_model.campaign_exists.return_value = True
        self.campaign_service.campaign_model.get_user_on_campagne.return_value = []
        result = self.campaign_service.get_all_user_on_campagn(campaign_id)
        assert result == {"message": "Personne inscrit sur cette campagne."}

    def test_get_all_user_on_campagn_with_users(self):
        campaign_id = 1
        self.campaign_service.campaign_model.campaign_exists.return_value = True
        self.campaign_service.campaign_model.get_user_on_campagne.return_value = [{"users_id_user": 10}, {"users_id_user": 20}]
        result = self.campaign_service.get_all_user_on_campagn(campaign_id)
        assert result == {"personne inscrite à cette campagne": [10, 20]}
