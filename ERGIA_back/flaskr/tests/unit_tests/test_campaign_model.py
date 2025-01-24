from unittest.mock import patch, MagicMock
import pytest
from flaskr.models.campaign_model import CampaignModel

class TestUpdateCampaign:

    @patch("flaskr.models.campaign_model.db_singleton")
    def test_update_campaign_all_fields(self, mock_db_singleton):
        """Test mise à jour avec tous les champs."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        campaign = CampaignModel()

        id_campaign = 1
        name = "Updated Name"
        owner_id = 2
        status_id = 3
        creation_date = "2023-01-01"
        date_phase_1 = "2023-02-01"
        date_phase_2 = "2023-03-01"

        result = campaign.update_campaign(
            id_campaign=id_campaign,
            name=name,
            owner_id=owner_id,
            status_id=status_id,
            creation_date=creation_date,
            date_phase_1=date_phase_1,
            date_phase_2=date_phase_2,
        )

        expected_query = """
            UPDATE campaigns
            SET name = %s, owner_id = %s, status_id = %s, creation_date = %s, date_phase_1 = %s, date_phase_2 = %s
            WHERE id_campaign = %s;
        """
        expected_params = (name, owner_id, status_id, creation_date, date_phase_1, date_phase_2, id_campaign)

        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.campaign_model.db_singleton")
    def test_update_campaign_some_fields(self, mock_db_singleton):
        """Test mise à jour avec certains champs uniquement."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        campaign = CampaignModel()

        id_campaign = 1
        name = "Partial Update Name"
        owner_id = 2

        result = campaign.update_campaign(
            id_campaign=id_campaign,
            name=name,
            owner_id=owner_id,
        )

        expected_query = """
            UPDATE campaigns
            SET name = %s, owner_id = %s
            WHERE id_campaign = %s;
        """
        expected_params = (name, owner_id, id_campaign)

        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.campaign_model.db_singleton")
    def test_update_campaign_no_updates(self, mock_db_singleton):
        """Test sans champs à mettre à jour."""
        mock_execute_query = MagicMock()
        mock_db_singleton.execute_query = mock_execute_query

        campaign = CampaignModel()

        id_campaign = 1

        result = campaign.update_campaign(id_campaign=id_campaign)

        mock_db_singleton.execute_query.assert_not_called()
        assert result is None

    @patch("flaskr.models.campaign_model.db_singleton")
    def test_update_campaign_only_one_field(self, mock_db_singleton):
        """Test mise à jour avec un seul champ."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        campaign = CampaignModel()

        id_campaign = 1
        status_id = 3

        result = campaign.update_campaign(
            id_campaign=id_campaign,
            status_id=status_id,
        )

        expected_query = """
            UPDATE campaigns
            SET status_id = %s
            WHERE id_campaign = %s;
        """
        expected_params = (status_id, id_campaign)

        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.campaign_model.db_singleton")
    def test_update_campaign_null_id(self, mock_db_singleton):
        """Test mise à jour avec un ID null (cas anormal)."""
        mock_execute_query = MagicMock()
        mock_db_singleton.execute_query = mock_execute_query

        campaign = CampaignModel()

        id_campaign = None

        with pytest.raises(TypeError):
            campaign.update_campaign(id_campaign=id_campaign)

        mock_db_singleton.execute_query.assert_not_called()
