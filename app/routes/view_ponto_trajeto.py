from config import db
from flask import Blueprint, request, jsonify, render_template
from models.motorista import Motorista
from models.veiculo import Veiculo

ponto_trajeto_bp = Blueprint('view_ponto_trajeto', __name__)

@ponto_trajeto_bp.route('/create', methods=['POST'])
def cerate_ponto_trajeto():
  """
  Rota para cadastrar um ponto de trajeto.
  """

  data = request.get_json() # pega todos os dados passados pelo body

  cnh = data.get('cnh') 
  cpf= data.get('cpf') 
  nome = data.get('nome') 
  senha = data.get('senha') 
  role = data.get('role') 
  veiculo_id = data.get('veiculo_id')

  try:
    motorista_existente = Motorista.query.filter_by(cpf=cpf).first()
    cnh_existente = Motorista.query.filter_by(cnh=cnh).first()

  except Exception as e:
    return jsonify({
      'status':'error',
      'message':f'{str(e)}'
    }), 500
  
  if motorista_existente or cnh_existente:
    return jsonify({
      "status": "conflict"
    }), 409

  try:
    motorista = Motorista(
      cnh=cnh,
      cpf=cpf,
      nome_completo=nome,
      senha=senha,
      role=role,
    )

    if veiculo_id:
      try:
        veiculo = Veiculo.query.filter_by(id=veiculo_id).first()
      
      except Exception as e:
        return jsonify({
          'status':'error',
          'message':f'{str(e)}'
        }), 500
      
    motorista.veiculos.append(veiculo)

    db.session.add(motorista)
    db.session.commit()
      
  except Exception as e:
    return jsonify({
      'status':'error',
      'message':f'{str(e)}'
    }), 500
  
  return jsonify({
    "status": "created"
  }), 201