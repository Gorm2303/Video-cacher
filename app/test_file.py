from initial import app

def test_index():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert response.data == b'Welcome to the Video API!'