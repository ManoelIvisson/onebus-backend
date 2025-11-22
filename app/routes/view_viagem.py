from sqlalchemy import null
from config import db
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template
from models.viagem import Viagem
from models.veiculo import Veiculo

viagem_bp = Blueprint('view_viagem', __name__)

@viagem_bp.route('/create', methods=['POST'])
def cerate_viagem():
  """
  Rota para cadastrar uma viagem.
  """

  data = request.get_json()

  horario_inicio = data.get("horario_inicio")
  veiculo_id = data.get("veiculo_id")

  inicio = datetime.strptime(horario_inicio, "%H:%M").time()

  try:
    viagem = Viagem(
      horario_inicio = inicio,
      veiculo_id = veiculo_id
    )

    if veiculo_id:
      try:
        Veiculo.query.filter_by(id=veiculo_id).first()
      
      except Exception as e:
        return jsonify({
          'status':'error',
          'message':f'{str(e)}'
        }), 500

    db.session.add(viagem)
    db.session.commit()
      
  except Exception as e:
    return jsonify({
      'status':'error',
      'message':f'{str(e)}'
    }), 500
  
  return jsonify({
    "status": "created"
  }), 201