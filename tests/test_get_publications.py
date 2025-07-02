import pytest
from unittest.mock import patch, MagicMock
from main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_user_publications_success(client):
    mock_token = "mocktoken"
    mock_user_id = 123
    mock_publications = [
        {
            "_id": "pub123",
            "Id_user": mock_user_id,
            "Text": "Publicación de prueba",
            "Multimedia": None,
            "Status": 1,
            "Datepublish": "2024-01-01T00:00:00",
            "Likes": []
        }
    ]

    with patch("main.jwt.decode") as mock_jwt_decode, \
         patch("services.functions.conection_mongo") as mock_conection_mongo:

        mock_jwt_decode.return_value = {"user_id": mock_user_id}
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_collection.find.return_value = mock_publications
        mock_db.__getitem__.return_value = mock_collection
        mock_conection_mongo.return_value = mock_db

        response = client.get(
            "/my-publications",
            headers={"Authorization": f"Bearer {mock_token}"}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert data[0]["_id"] == "pub123"
        assert data[0]["Id_user"] == mock_user_id
