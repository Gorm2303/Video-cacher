from flask import Flask

app = Flask(__name__)

# Define API endpoints
@app.route('/')
def index():
    return 'Welcome to the Video API!'

if __name__ == '__main__':
    app.run(debug=True)