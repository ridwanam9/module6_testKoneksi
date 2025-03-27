from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from data.dummy_data import users

users_bp = Blueprint('users', __name__)

# Retrieve the all users (Admin Only)
@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    
    user_id = int(get_jwt_identity())
    current_user = next((u for u in users if u["id"] == user_id), None)

    if not current_user or current_user["role"] != "admin":
        return jsonify({"msg": "Unauthorized"}), 403

    return jsonify(users), 200

# Create a new user
@users_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user account"""
    data = request.json
    if not data.get("username") or not data.get("password"):
        return jsonify({"msg": "Username and password are required"}), 400

    # Check if username already exists
    if any(user["username"] == data["username"] for user in users):
        return jsonify({"msg": "Username already exists"}), 400

    new_user = {
        "id": len(users) + 1,
        "username": data["username"],
        "password": data["password"]
    }
    users.append(new_user)

    return jsonify({"msg": "User created successfully", "user_id": new_user["id"]}), 201

# Login
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = next((u for u in users if u["username"] == data["username"] and u["password"] == data["password"]), None)

    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user["id"]))
    return jsonify({"access_token": token})


# Retrieve the profile of the currently logged-in user
@users_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())
    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify(user)


# Update the profile of the currently logged-in user
@users_bp.route('/users/me', methods=['PUT'])
@jwt_required()
def update_user():
    """Update the profile of the currently logged-in user"""
    user_id = int(get_jwt_identity())
    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.json
    if "username" in data:
        user["username"] = data["username"]
    if "password" in data:
        user["password"] = data["password"]

    return jsonify({"msg": "User profile updated successfully"})