# inventory_service/test_app.py
import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            db.session.commit()
            db.drop_all()
        yield client


def test_get_books_empty(client):
    """Start with a blank database."""
    rv = client.get('/books')
    response_data = rv.data.strip()
    assert b'[]' == response_data


def test_add_book(client):
    """Test adding a book."""
    rv = client.post('/books', json={
        'title': 'Test Book',
        'author': 'Author Name',
        'stock_quantity': 5
    })
    assert b'Book added successfully' in rv.data
    rv = client.get('/books')
    assert b'Test Book' in rv.data
