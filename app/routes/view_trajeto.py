from datetime import datetime
from config import db
from flask import Blueprint, request, jsonify, render_template
from models.trajeto import Trajeto
from models.veiculo import Veiculo

trajeto_bp = Blueprint('view_trajeto', __name__)

@trajeto_bp.route('/create', methods=['POST'])
def cerate_trajeto():
  """
  Rota para cadastrar um trajeto.
  """

  data = request.get_json() # pega todos os dados passados pelo body

  nome = data.get("nome")
  trajeto_planejado = data.get("trajeto_planejado")
  horario_inicio = data.get("horario_inicio")
  horario_final = data.get("horario_final")
  veiculo_id = data.get("veiculo_id")

  inicio = datetime.strptime(horario_inicio, "%H:%M").time()
  final = datetime.strptime(horario_final, "%H:%M").time()

  try:
    trajeto = Trajeto(
      nome = nome,
      trajeto_planejado = trajeto_planejado,
      horario_inicio = inicio,
      horario_final = final,
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

    db.session.add(trajeto)
    db.session.commit()
      
  except Exception as e:
    return jsonify({
      'status':'error',
      'message':f'{str(e)}'
    }), 500
  
  return jsonify({
    "status": "created"
  }), 201