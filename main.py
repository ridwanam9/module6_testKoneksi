from flask import Flask
from config import app
from modules.users import users_bp
from modules.accounts import accounts_bp
from modules.transactions import transactions_bp

# Register blueprints
app.register_blueprint(users_bp)
app.register_blueprint(accounts_bp)
app.register_blueprint(transactions_bp)

if __name__ == '__main__':
    app.run(debug=True)
