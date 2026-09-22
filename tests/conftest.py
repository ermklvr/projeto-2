import os

import pytest
from dotenv import load_dotenv

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL não configurada")

os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from app.database import Base, engine


@pytest.fixture(autouse=True)
def setup_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield



@pytest.fixture
def category_id():
    from tests.test_products import client

    response = client.post(
        "/categories",
        json={
            "name": "Categoria Teste"
        }
    )

    assert response.status_code == 200

    return response.json()["id"]



