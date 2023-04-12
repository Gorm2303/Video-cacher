import pytest
import json
import requests
from unittest.mock import Mock, patch
from app import app, redis_conn

@pytest.fixture
def client():
    return app.test_client()

# Mock video metadata for testing
video_metadata = [
    {
        "id": "1",
        "title": "Sample Video 1",
        "description": "This is a sample video."
    },
    {
        "id": "2",
        "title": "Sample Video 2",
        "description": "This is another sample video."
    }
]

# Test the index route
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Welcome to the Video cacher API!'

# Test get_videos_metadata_endpoint
@patch('app.get_videos_metadata_from_mongodb', return_value=video_metadata)
def test_get_videos_metadata_endpoint(mock_get_videos_metadata_from_mongodb, client):
    response = client.get('/api/v1/videometadata')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == video_metadata

    # Test if the data is cached in Redis
    redis_data = redis_conn.get('data')
    assert redis_data is not None
    redis_data = json.loads(redis_data)
    assert redis_data == video_metadata

# Test get_video_metadata
@patch('app.get_video_metadata_from_mongodb', return_value=video_metadata[0])
def test_get_video_metadata(mock_get_video_metadata_from_mongodb, client):
    response = client.get('/api/v1/videometadata/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == video_metadata[0]

    # Test if the data is cached in Redis
    redis_data = redis_conn.get('data:1')
    assert redis_data is not None
    redis_data = json.loads(redis_data)
    assert redis_data == video_metadata[0]

# Test search_videos
@patch('app.get_videos_metadata_from_mongodb', return_value=video_metadata)
def test_search_videos(mock_get_videos_metadata_from_mongodb, client):
    response = client.get('/api/v1/videometadata/search?q=sample')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == video_metadata

    response = client.get('/api/v1/videometadata/search?q=1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == [video_metadata[0]]

    response = client.get('/api/v1/videometadata/search?q=nonexistent')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == []
