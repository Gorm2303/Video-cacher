from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB database
client = MongoClient()
db = client['video_db']
videos = db['videos']

# Define API endpoints
@app.route('/')
def index():
    return 'Welcome to the Video API!'

@app.route('/videos')
def get_videos():
    results = []
    for video in videos.find():
        results.append({
            'id': str(video['_id']),
            'title': video['title'],
            'description': video['description'],
            'genres': video['genres'],
            'length': video['length'],
            'release_date': video['release_date'],
            'image': video['image']
        })
    return jsonify(results)

@app.route('/videos/<string:video_id>')
def get_video(video_id):
    video = videos.find_one({ '_id': ObjectId(video_id) })
    if video is None:
        return jsonify({ 'error': 'Video not found' }), 404
    else:
        result = {
            'id': str(video['_id']),
            'title': video['title'],
            'description': video['description'],
            'genres': video['genres'],
            'length': video['length'],
            'release_date': video['release_date'],
            'image': video['image']
        }
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)