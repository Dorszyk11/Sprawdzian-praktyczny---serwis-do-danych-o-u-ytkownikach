from flask import Flask, jsonify, request, abort
from users_service import UserService

app = Flask(__name__)

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
