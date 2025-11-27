from sqlalchemy import null
from config import db
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template
from models.coordenada_viagem import CoordenadaViagem
from models.veiculo import Veiculo
from models.viagem import Viagem

coordenada_viagem_bp = Blueprint('view_coordenada_viagem', __name__)

@coordenada_viagem_bp.route('/create', methods=['POST'])
def cerate_coordenada_viagem():
  """
  Rota para cadastrar uma coordenada de viagem
  """

  data = request.get_json() # pega todos os dados passados pelo body

  latitude = data.get('latitude') 
  longitude = data.get('longitude') 
  criado_em = data.get('criado_em')
  mac = data.get('mac')

  criado_em = datetime.strptime(criado_em, "%Y-%m-%d %H:%M:%S")
  try:
    veiculo = Veiculo.query.filter_by(mac_embarcado=mac).first()
    if not veiculo:
      return jsonify({
        'status': 'error',
        'message': 'Veículo não encontrado para esse MAC.'
      }), 404
    
    viagem = Viagem.query.filter_by(veiculo_id=veiculo.id, status="ativa").first()
    if not viagem:
      return jsonify({
        'status': 'error',
        'message': 'Veículo não encontrado para esse MAC.'
      }), 404
  except Exception as e:
    return jsonify({
      'status':'error',
      'message':f'{str(e)}'
    }), 500

  try:
    ponto_trajeto = CoordenadaViagem(
      latitude=latitude,
      longitude=longitude,
      criado_em=criado_em,
      viagem_id=viagem.id,
      mac=mac
    )
    
    veiculo.status = "ativo"

    db.session.add(ponto_trajeto)
    db.session.add(veiculo)
    db.session.commit()
      
  except Exception as e:
    db.session.rollback()
    return jsonify({
      'status':'error',
      'message':f'{str(e)}'
    }), 500
  
  return jsonify({
    "status": "created"
  }), 201
  
@coordenada_viagem_bp.route('/get-all', methods=['GET'])
def get_Coordenadas():
  """
  Rota para mostrar todos os pontos

  Método:
    Get

  Retorno:
    JSON listando todos os pontos
  """
  try:
    coordenadas = CoordenadaViagem.query.all()

  except Exception as e:
    return jsonify({
      'status':'error',
      'message':f'{str(e)}'
    }), 500
  
  resposta_json = {}

  for ponto in coordenadas:
    resposta_json[ponto.id] = {
      "latitude": ponto.latitude, 
      "longitude": ponto.longitude, 
      "criado_em": ponto.criado_em, 
      "viagem_id": ponto.viagem_id,
      "mac": ponto.mac
    }

  return jsonify({
    "status":"success",
    "data":resposta_json
  }), 200
