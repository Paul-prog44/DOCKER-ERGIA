import pytest



@pytest.mark.skip(reason="Pas testable avec Jenkins") #Commentez la ligne avant de lancer les tests
class TestAuthentication(object):
    """Lancer la classe pour les tests d'intégration. Ne pas lancer les tests individuellement,
        ils sont fait pour être exécutés les uns après les autres"""


    @pytest.fixture
    def app(self):
        from flaskr.main import create_app
        app = create_app()
        yield app

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_post_register(self, client):
        response = client.post('/register', json={
            "email": "elon.mousse@example.com",
            "password": "Password123!",
            "firstname": "Elon",
            "lastname": "Mousse",
            "acceptCgu": True
        })

        assert response.status_code == 200


    def test_post_login(self, client):
        response = client.post("/login", json={
            "email": "elon.mousse@example.com",
            "password": "Password123!"
        })
        print()
        assert response.status_code == 200

        token = response.get_json()['token']
        response = client.get("/user", headers={"Authorization": "Bearer " + token})
        assert response.status_code == 200

    def test_delete_user(self, client):
        response = client.delete("/delete", json={
            "email": "elon.mousse@example.com"
        })

        assert response.status_code == 200
