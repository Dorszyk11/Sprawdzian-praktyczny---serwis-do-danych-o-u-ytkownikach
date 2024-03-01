from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

users = {}
current_id = 1

class UserService:
    @staticmethod
    def get_all_users():
        return [user for user in users.values()]

    @staticmethod
    def get_user(user_id):
        return users.get(user_id)

    @staticmethod
    def add_user(user_data):
        global current_id
        users[current_id] = {**user_data, "id": current_id}
        current_id += 1
        return users[current_id - 1]

    @staticmethod
    def update_user(user_id, user_data):
        if user_id in users:
            for key, value in user_data.items():
                if key in users[user_id]:
                    users[user_id][key] = value
            return users[user_id]
        return None

    @staticmethod
    def delete_user(user_id):
        return users.pop(user_id, None)

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(UserService.get_all_users()), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user(user_id)
    if user:
        return jsonify(user), 200
    else:
        abort(404)

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    if not user_data or 'firstName' not in user_data or 'lastName' not in user_data or 'birthYear' not in user_data or 'group' not in user_data:
        abort(400)
    if user_data['group'] not in ['user', 'premium', 'admin']:
        abort(400)
    new_user = UserService.add_user(user_data)
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user_data = request.json
    updated_user = UserService.update_user(user_id, user_data)
    if updated_user:
        return jsonify(updated_user), 200
    else:
        abort(404)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if UserService.delete_user(user_id):
        return jsonify({}), 204
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
