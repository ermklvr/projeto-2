from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_app_is_running():
    response = client.get("/products")
    
    assert response.status_code == 200
    
    
def test_create_product():
    response = client.post(
        "/products",
        json={
            "name": "Produto Teste",
            "price": 10.50,
            "stock_quantity": 20,
            "category_id": 1
        }
    )
    
    assert response.status_code == 200
    assert response.json()["name"] == "Produto Teste"
    assert response.json()["price"] == "10.50"
    assert response.json()["stock_quantity"] == 20
    
    
    
def test_create_product_invalid_price():
    response = client.post(
        "/products",
        json={
            "name": "Produto Teste",
            "price": -50,
            "stock_quantity": 20,
            "category_id": 1
            }
        )
    assert response.status_code == 422 


def test_delete_product_soft_delete():
    create_response = client.post(
        "/products",
        json={
            "name": "Produto Soft Delete",
            "price": 50,
            "stock_quantity": 10,
            "category_id": 1
            }
    )
    
    product_id = create_response.json()["id"]
    
    #desativar o produto
    delete_response = client.delete(f"/products/{product_id}")
    
    assert delete_response.status_code == 204
    
    #não aparecer mais como ativo
    get_response = client.get(f"/products/{product_id}")
    
    assert get_response.status_code == 404
    
    
def test_movement_out_insufficient_stock():
    product_response = client.post(
            "/products",
            json={
                "name": "Produto Estoque Insuficiente",
                "price": 100,
                "stock_quantity": 5,
                "category_id": 1
                }
        )
    
    product_id = product_response.json()["id"]
    
    movement_response = client.post(
                "/movements/",
                json={
                    "product_id": product_id,
                    "type" : "OUT",
                    "quantity":10
                    }
            )
    
    assert movement_response.status_code == 409
    
    product_response = client.get(f"/products/{product_id}")
    
    assert product_response.json()["stock_quantity"] == 5
    
    
def test_create_movement_in_updates_stock():
    product_response = client.post(
        "/products",
        json={
            "name": "Produto Movimento IN",
            "price": 100,
            "stock_quantity": 10,
            "category_id": 1
        }
    )

    product_id = product_response.json()["id"]

    movement_response = client.post(
        "/movements/",
        json={
            "product_id": product_id,
            "type": "IN",
            "quantity": 5
        }
    )

    assert movement_response.status_code == 200

    product_response = client.get(f"/products/{product_id}")

    assert product_response.status_code == 200
    assert product_response.json()["stock_quantity"] == 15
    
    
def test_create_movement_out_updates_stock():
    product_response = client.post(
        "/products",
        json={
            "name": "Produto Movimento OUT",
            "price": 100,
            "stock_quantity": 10,
            "category_id": 1
        }
    )

    product_id = product_response.json()["id"]

    movement_response = client.post(
        "/movements/",
        json={
            "product_id": product_id,
            "type": "OUT",
            "quantity": 4
        }
    )

    assert movement_response.status_code == 200

    product_response = client.get(f"/products/{product_id}")

    assert product_response.status_code == 200
    assert product_response.json()["stock_quantity"] == 6
    
def test_movement_inactive_product():
        product_response = client.post(
            "/products",
            json={
                "name": "Produto Inativo",
                "price" : 100,
                "stock_quantity" : 10,
                "category_id" : 1
            }
        )
        
        product_id = product_response.json()["id"]
        
        delete_response = client.delete(f"/products/{product_id}")
        
        assert delete_response.status_code == 204
        
        movement_response = client.post(
        "/movements/",
        json={
            "product_id": product_id,
            "type": "IN",
            "quantity": 5
        }
    )
        assert movement_response.status_code == 409

   