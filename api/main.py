import os
import logging
from flask import Flask, request, jsonify
from auth_gateway.config import Config
from auth_gateway.auth import Auth

app = Flask(__name__)
app.config.from_object(Config)

auth = Auth(app.config['AUTH_SERVICE_URL'], app.config['AUTH_SERVICE_PORT'])

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        user_data = auth.login(data['username'], data['password'])
        return jsonify({'token': user_data['token']})
    except Exception as e:
        logging.error(e)
        return jsonify({'error': 'Failed to authenticate'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')
    if token is None:
        return jsonify({'error': 'Missing token'}), 401
    try:
        auth.logout(token)
        return jsonify({'message': 'Logged out successfully'})
    except Exception as e:
        logging.error(e)
        return jsonify({'error': 'Failed to log out'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)