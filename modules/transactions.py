from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from data.dummy_data import accounts, transactions

transactions_bp = Blueprint('transactions', __name__)

# Create a New Transaction to Account
@transactions_bp.route('/transactions', methods=['POST'])
@jwt_required()
def create_transaction():
    data = request.json
    user_id = int(get_jwt_identity())

    account = next((acc for acc in accounts if acc["id"] == data["account_id"] and acc["user_id"] == user_id), None)

    if not account:
        return jsonify({"msg": "Unauthorized or account not found"}), 403

    if data["type"] == "deposit":
        account["balance"] += data["amount"]
    elif data["type"] == "withdrawal":
        if account["balance"] < data["amount"]:
            return jsonify({"msg": "Insufficient balance"}), 400
        account["balance"] -= data["amount"]
    else:
        return jsonify({"msg": "Invalid transaction type"}), 400

    new_transaction = {
        "id": len(transactions) + 1,
        "account_id": data["account_id"],
        "amount": data["amount"],
        "type": data["type"]
    }
    transactions.append(new_transaction)

    return jsonify({"msg": "Transaction successful", "new_balance": account["balance"]})

# Retrieve All Transactions from Account
@transactions_bp.route('/transactions/history', methods=['GET'])
@jwt_required()
def transaction_history():
    
    user_id = int(get_jwt_identity())

    # Ambil query params (optional)
    account_id = request.args.get('account_id', type=int)

    # Cari semua akun milik user ini
    user_accounts = [acc["id"] for acc in accounts if acc["user_id"] == user_id]

    # Jika account_id diberikan, pastikan akun tersebut milik user
    if account_id:
        if account_id not in user_accounts:
            return jsonify({"msg": "Unauthorized to view this account's transactions"}), 403
        transactions_history = [t for t in transactions if t["account_id"] == account_id]
    else:
        # Ambil semua transaksi dari akun-akun milik user ini
        transactions_history = [t for t in transactions if t["account_id"] in user_accounts]

    return jsonify(transactions_history), 200
