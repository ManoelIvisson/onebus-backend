from flask import Blueprint, request, jsonify
from services.openroute import get_route

openroute_bp = Blueprint("openroute", __name__)

@openroute_bp.route("/route", methods=["POST"])
def route():
    try:
        data = request.get_json()

        coordinates = data.get("coordinates")

        if not coordinates or len(coordinates) < 2:
            return jsonify({"error": "Coordenadas inválidas"}), 400

        result = get_route(coordinates)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500