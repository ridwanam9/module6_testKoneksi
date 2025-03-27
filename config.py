from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_secret_key"  # Ubah dengan secret key yang kuat
jwt = JWTManager(app)
