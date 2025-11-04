from sqlalchemy import null
from config import db
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template
from models.ponto_trajeto import PontoTrajeto
from models.veiculo import Veiculo

ponto_trajeto_bp = Blueprint('view_ponto_trajeto', __name__)

@ponto_trajeto_bp.route('/create', methods=['POST'])
def cerate_ponto_trajeto():
  """
  Rota para cadastrar um ponto de trajeto.
  """

  data = request.get_json() # pega todos os dados passados pelo body

  latitude = data.get('latitude') 
  longitude = data.get('longitude') 
  criado_em = data.get('criado_em')
  e_origem = data.get('e_origem')
  e_destino = data.get('e_destino')
  trajeto_id = data.get('trajeto_id')

  criado_em = datetime.strptime(criado_em, "%Y-%m-%d %H:%M:%S")

  try:
    ponto_trajeto = PontoTrajeto(
      latitude=latitude,
      longitude=longitude,
      criado_em=criado_em,
      e_origem=e_origem,
      e_destino=e_destino,
      trajeto_id=trajeto_id
    )

    db.session.add(ponto_trajeto)
    db.session.commit()
      
  except Exception as e:
    return jsonify({
      'status':'error',
      'message':f'{str(e)}'
    }), 500
  
  return jsonify({
    "status": "created"
  }), 201