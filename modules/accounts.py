from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from data.dummy_data import accounts

accounts_bp = Blueprint('accounts', __name__)

# Retrieve the account details
@accounts_bp.route('/accounts', methods=['GET'])
@jwt_required()
def get_accounts():
    user_id = int(get_jwt_identity())
    user_accounts = [acc for acc in accounts if acc["user_id"] == user_id]

    if not user_accounts:
        return jsonify({"msg": "No accounts found"}), 404

    return jsonify(user_accounts)
