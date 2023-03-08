from flask import Flask, jsonify
import redis
import requests

app = Flask(__name__)
redis_conn = redis.Redis(host='localhost', port=6379, db=0, password='redis')


def get_video_metadata_from_mongodb():
    # Make a request to MongoDB API
    response = requests.get('https://your-mongodb-api.com/data')
    # Convert the response to JSON
    video_metadata = response.json()
    return video_metadata

def get_video_metadata_from_mongodb(id):
    # Make a request to MongoDB API
    response = requests.get(f'https://your-mongodb-api.com/data/{id}')
    # Convert the response to JSON
    video_metadata = response.json()
    return video_metadata

# Endpoint to get video metadata for all videos
@app.route('/videometadata')
def get_video_metadata():
    # Try to get the video metadata from Redis
    data = redis_conn.get('data')
    if data is not None:
        return data.decode('utf-8')
    else:
        # If the data is not in Redis, get it from MongoDB
        data = get_video_metadata_from_mongodb()
        # Cache the data in Redis for 1 hour (3600 seconds)
        redis_conn.setex('data', 3600, jsonify(data))
        return jsonify(data)
    
# Endpoint using id to get video metadata for one video
@app.route('/videometadata/<id>')
def get_video_metadata(id):
    # Try to get the video metadata from Redis
    data = redis_conn.get(f'data:{id}')
    if data is not None:
        return data.decode('utf-8')
    else:
        # If the data is not in Redis, get it from MongoDB
        data = get_video_metadata_from_mongodb(id)
        # Cache the data in Redis for 1 hour (3600 seconds)
        redis_conn.setex(f'data:{id}', 3600, jsonify(data))
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)