from flask import Flask, jsonify
import os

VERSION = os.environ.get('APP_VERSION', 'UNKNOWN')
COLOR = os.environ.get('APP_COLOR', 'gray')

app = Flask(__name__)

# Main route
@app.route('/', methods=['GET'])
def index():
    response = {
        'message': 'Welcome to the Zero-Downtime Deployment Test!',
        'version': VERSION,
        'color': COLOR,
        'environment': os.environ.get('ENVIRONMENT', 'Local Docker Compose')
    }
    return jsonify(response)

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'version': VERSION}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
