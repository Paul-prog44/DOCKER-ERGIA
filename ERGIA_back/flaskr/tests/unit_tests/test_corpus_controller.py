import unittest
from unittest.mock import patch, MagicMock, mock_open
from flask import Flask
from flaskr.controllers.corpus_controller import corpus_bp
import os
TARGET_DIRECTORY = os.path.expanduser("~/Desktop/CorpusSAE")


class TestCorpusController(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(corpus_bp)
        self.client = self.app.test_client()

    @patch('flaskr.services.corpus_service.CorpusService.exec_getAllTexts')
    def test_corpus(self, mock_exec_getAllTexts):
        """Test pour la route '/corpus'"""
        mock_exec_getAllTexts.return_value = {"texts": ["Text1", "Text2"]}

        response = self.client.get('/corpus')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"texts": ["Text1", "Text2"]})
        mock_exec_getAllTexts.assert_called_once()



    @patch('flaskr.services.corpus_service.CorpusService.exec_getSummary')
    def test_read_summary_not_found(self, mock_exec_getSummary):
        """Test pour la route '/summary/<int:summary_id>' avec un résumé introuvable"""
        mock_exec_getSummary.return_value = None

        response = self.client.get('/summary/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Résumé introuvable"})
        mock_exec_getSummary.assert_called_once_with(999)

    @patch('flaskr.services.corpus_service.CorpusService.exec_getSummary')
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_read_summary_file_not_found(self, mock_open, mock_exec_getSummary):
        """Test pour la route '/summary/<int:summary_id>' avec fichier introuvable"""
        mock_exec_getSummary.return_value = [{"path": "non_existing_summary.txt"}]

        response = self.client.get('/summary/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Fichier introuvable"})
        mock_exec_getSummary.assert_called_once_with(1)


    @patch('flaskr.services.corpus_service.CorpusService.exec_getText')
    def test_read_text_not_found(self, mock_exec_getText):
        """Test pour la route '/text/<int:text_id>' avec un texte introuvable"""
        mock_exec_getText.return_value = None

        response = self.client.get('/text/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Résumé introuvable"})
        mock_exec_getText.assert_called_once_with(999)

    @patch('flaskr.services.corpus_service.CorpusService.exec_getText')
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_read_text_file_not_found(self, mock_open, mock_exec_getText):
        """Test pour la route '/text/<int:text_id>' avec fichier introuvable"""
        mock_exec_getText.return_value = [{"path": "non_existing_text.txt"}]

        response = self.client.get('/text/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Fichier introuvable"})
        mock_exec_getText.assert_called_once_with(1)

    @patch('flaskr.services.corpus_service.CorpusService.exec_getSummary')
    def test_read_summary_internal_error(self, mock_exec_getSummary):
        """Test pour la route '/summary/<int:summary_id>' avec une erreur inattendue"""
        mock_exec_getSummary.side_effect = Exception("Une erreur interne est survenue")

        response = self.client.get('/summary/1')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Une erreur interne est survenue"})
        mock_exec_getSummary.assert_called_once_with(1)

    @patch('flaskr.services.corpus_service.CorpusService.exec_getText')
    def test_read_text_internal_error(self, mock_exec_getText):
        """Test pour la route '/text/<int:text_id>' avec une erreur inattendue"""
        mock_exec_getText.side_effect = Exception("Une erreur interne est survenue")

        response = self.client.get('/text/1')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Une erreur interne est survenue"})
        mock_exec_getText.assert_called_once_with(1)

    
    @patch('flaskr.services.corpus_service.CorpusService.exec_get_texts_by_campaign_id')
    def test_get_texts_by_campaign_id_not_found(self, mock_exec_get_texts_by_campaign_id):
        """Test pour la route '/texts/<int:campaign_id>' avec aucun texte trouvé."""
        mock_exec_get_texts_by_campaign_id.return_value = []

        response =  self.client.get('/texts/1')

        assert response.status_code == 404
        assert response.json == {"error": "Aucun texte trouvé pour cette campagne"}
        mock_exec_get_texts_by_campaign_id.assert_called_once_with(1)

    @patch('flaskr.services.corpus_service.CorpusService.exec_get_texts_by_campaign_id')
    def test_get_texts_by_campaign_id_internal_error(self, mock_exec_get_texts_by_campaign_id):
        """Test pour la route '/texts/<int:campaign_id>' avec une erreur inattendue."""
        mock_exec_get_texts_by_campaign_id.side_effect = Exception("Erreur serveur")

        response =  self.client.get('/texts/1')
        assert response.status_code == 500
        assert response.json == {"error": "Erreur serveur"}
        mock_exec_get_texts_by_campaign_id.assert_called_once_with(1)

    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='Contenu fictif pour valid_path.txt')
    @patch('flaskr.services.corpus_service.CorpusService.exec_get_texts_by_campaign_id')
    def test_get_texts_by_campaign_id_success(self, mock_exec_get_texts_by_campaign_id, mock_open_file, mock_isfile):
        """Test avec un fichier valide."""
        mock_exec_get_texts_by_campaign_id.return_value = [
            {"id_original_text": 1, "path": "valid_path.txt"},
            {"id_original_text": 2, "path": None},
        ]

        response = self.client.get('/texts/1')

        assert response.status_code == 200
        assert response.json == [
            {
                "text_id": 1,
                "path": "valid_path.txt",
                "content": "Contenu fictif pour valid_path.txt"
            },
            {
                "text_id": 2,
                "error": "Chemin introuvable pour ce résumé"
            }
        ]
        mock_exec_get_texts_by_campaign_id.assert_called_once_with(1)
        mock_isfile.assert_called_with(os.path.join(TARGET_DIRECTORY, "valid_path.txt"))


    @patch('flaskr.services.corpus_service.CorpusService.exec_get_summaries_by_text_id')
    def test_get_summaries_by_campaign_id_not_found(self, mock_exec_get_summaries_by_text_id):
        """Test lorsque aucun résumé n'est trouvé."""
        mock_exec_get_summaries_by_text_id.return_value = []

        response = self.client.get('/summaries/42')

        assert response.status_code == 404
        assert response.json == {"error": "Aucun texte trouvé pour cette campagne"}
        mock_exec_get_summaries_by_text_id.assert_called_once_with(42)

    @patch('os.path.isfile', return_value=False)
    @patch('flaskr.services.corpus_service.CorpusService.exec_get_summaries_by_text_id')
    def test_get_summaries_by_campaign_id_file_not_found(self, mock_exec_get_summaries_by_text_id, mock_isfile):
        """Test lorsque le fichier d'un résumé est introuvable."""
        mock_exec_get_summaries_by_text_id.return_value = [
            {"id_summary": 1, "path": "missing_path.txt", "original_text_id": 42, "annotator_id": 123}
        ]

        response = self.client.get('/summaries/42')

        assert response.status_code == 200
        assert response.json == [
            {
                "id_summary": 1,
                "error": "Fichier introuvable"
            }
        ]
        mock_exec_get_summaries_by_text_id.assert_called_once_with(42)
        mock_isfile.assert_called_once_with(os.path.join(TARGET_DIRECTORY, "missing_path.txt"))

    @patch('flaskr.services.corpus_service.CorpusService.exec_get_summaries_by_text_id')
    def test_get_summaries_by_campaign_id_missing_path(self, mock_exec_get_summaries_by_text_id):
        """Test lorsque le chemin d'un résumé est manquant."""
        mock_exec_get_summaries_by_text_id.return_value = [
            {"id_summary": 1, "path": None, "original_text_id": 42, "annotator_id": 123}
        ]

        response = self.client.get('/summaries/42')

        assert response.status_code == 200
        assert response.json == [
            {
                "id_summary": 1,
                "error": "Chemin introuvable pour ce résumé"
            }
        ]
        mock_exec_get_summaries_by_text_id.assert_called_once_with(42)

    @patch('flaskr.services.corpus_service.CorpusService.exec_get_summaries_by_text_id')
    def test_get_summaries_by_campaign_id_internal_error(self, mock_exec_get_summaries_by_text_id):
        """Test lorsqu'une erreur inattendue survient."""
        mock_exec_get_summaries_by_text_id.side_effect = Exception("Erreur serveur")

        response = self.client.get('/summaries/42')

        assert response.status_code == 500
        assert response.json == {"error": "Erreur serveur"}
        mock_exec_get_summaries_by_text_id.assert_called_once_with(42)

if __name__ == '__main__':
    unittest.main()
