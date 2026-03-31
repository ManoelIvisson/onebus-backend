import os
from config import app, db
from routes.view_index import view_index
from routes.view_motorista import motorista_bp
from routes.view_ponto_trajeto import ponto_trajeto_bp
from routes.view_coordenada_viagem import coordenada_viagem_bp
from routes.view_openroute import openroute_bp
# from routes.viewCidadao import view_cidadao
from routes.view_veiculo import veiculo_bp
from routes.view_trajeto import trajeto_bp
from routes.view_viagem import viagem_bp
# from routes.viewViagem import view_viagem
# from routes.viewAnalise import view_analise
from flask import request, jsonify
from services.openroute import get_route

app.register_blueprint(view_index, url_prefix='/')
app.register_blueprint(motorista_bp, url_prefix='/api/v1/motorista')
# app.register_blueprint(view_cidadao, url_prefix='/cidadao')
app.register_blueprint(trajeto_bp, url_prefix='/api/v1/trajeto')
app.register_blueprint(viagem_bp, url_prefix='/api/v1/viagem')
app.register_blueprint(ponto_trajeto_bp, url_prefix='/api/v1/ponto-trajeto')
app.register_blueprint(coordenada_viagem_bp, url_prefix='/api/v1/coordenada-viagem')
app.register_blueprint(veiculo_bp, url_prefix='/api/v1/veiculo')

app.register_blueprint(openroute_bp, url_prefix='/api/v1')
import models

@app.route("/route", methods=["POST"])
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', debug=True)