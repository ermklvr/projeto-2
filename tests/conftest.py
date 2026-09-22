import pytest

from tests.test_products import client


#---------------------FIXTURE-----------------------
@pytest.fixture
def category_id():
    response = client.post(
        "/categories",
        json = {
            "name": "Categoria Teste"
        }
    )
    
    assert response.status_code == 200

    return response.json()["id"]