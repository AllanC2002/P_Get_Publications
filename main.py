from flask import Flask, request, jsonify
import jwt
import os
from dotenv import load_dotenv
from services.functions import user_publications
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

CORS(app)
SECRET_KEY = os.getenv("SECRET_KEY")

@app.route("/my-publications", methods=["GET"])
def get_Userpublications():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token missing or invalid"}), 401

    token = auth_header.replace("Bearer ", "")

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded.get("user_id")
        if user_id is None:
            return jsonify({"error": "Invalid token data"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    try:
        publications = user_publications(user_id)
        return jsonify(publications), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
