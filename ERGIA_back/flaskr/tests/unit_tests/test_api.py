from unittest.mock import patch
import unittest
import os


os.environ['TESTING'] = 'True'
from flaskr.main import create_app


class APITestCase(unittest.TestCase):
    
    def setUp(self):
        # Créer une instance de l'application pour les tests
        self.app = create_app()
        self.app.config['TESTING'] = 'True'
        self.client = self.app.test_client()

    def tearDown(self):
        # Effectuez les opérations nécessaires après les tests, si nécessaire
        pass


if __name__ == '__main__':
    unittest.main()