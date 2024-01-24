# order_service/test_app.py
import pytest
import requests_mock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_order_creation(client):
    with requests_mock.Mocker() as m:
        m.get('http://localhost:5000/books/1', json={'stock_quantity': 10})
        rv = client.post('/orders', json={'book_id': 1})
        assert b'Order created successfully' in rv.data
