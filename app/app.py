from flask import Flask, jsonify
import redis
import requests
import os
import json

app = Flask(__name__)
redis_url = os.environ.get('REDIS_URL')
# Endpoint for getting all videos' metadata from video reader
videos_url = os.environ.get('VIDEOS_URL')
# Endpoint for getting one video's metadata from video reader
video_url = os.environ.get('VIDEO_URL')
redis_conn = redis.from_url(redis_url)


def get_videos_metadata_from_mongodb():
    # Make a request to MongoDB API
    response = requests.get(videos_url)
    # Convert the response to JSON
    video_metadata = response.json()
    return video_metadata

def get_video_metadata_from_mongodb(id):
    # Make a request to MongoDB API
    url = video_url.format(id=id)
    response = requests.get(url)
    # Convert the response to JSON
    video_metadata = response.json()
    return video_metadata

@app.route('/')
def index():
    return 'Welcome to the Video cacher API!'

# Endpoint to get video metadata for all videos
@app.route('/videometadata')
def get_videos_metadata():
    # Try to get the video metadata from Redis
    data = redis_conn.get('data')
    if data is not None:
        # Convert string to JSON
        data = json.loads(data)
        return jsonify(data) 
    else:
        # If the data is not in Redis, get it from MongoDB
        data = get_videos_metadata_from_mongodb()
        # Convert JSON to string to cache it in Redis 
        json_str = json.dumps(data)
        # Cache the data in Redis for 1 hour (3600 seconds)
        redis_conn.setex('data', 3600, json_str)    
        return jsonify(data)
    
# Endpoint using id to get video metadata for one video
@app.route('/videometadata/<id>')
def get_video_metadata(id):
    # Try to get the video metadata from Redis
    data = redis_conn.get(f'data:{id}')
    if data is not None:
        # Convert string to JSON
        data = json.loads(data)
        return jsonify(data)
    else:
        # If the data is not in Redis, get it from MongoDB
        data = get_video_metadata_from_mongodb(id)
        # Convert JSON to string to cache it in Redis 
        json_str = json.dumps(data)
        # Cache the data in Redis for 1 hour (3600 seconds)
        redis_conn.setex(f'data:{id}', 3600, json_str)
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)