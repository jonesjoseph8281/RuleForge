from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from pydantic import BaseModel, ValidationError

blp = Blueprint("auth", "auth", url_prefix="/api/v1/auth")

class LoginRequest(BaseModel):
    email: str
    password: str

@blp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        req = LoginRequest.model_validate(data)
    except ValidationError as e:
        return jsonify(e.errors()), 400
        
    if req.email == "test@example.com" and req.password == "password":
        access_token = create_access_token(identity={"id": "u1", "client_id": "client_A", "role": "engineer"})
        refresh_token = create_refresh_token(identity={"id": "u1"})
        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
        
    return jsonify({"message": "Invalid credentials"}), 401
