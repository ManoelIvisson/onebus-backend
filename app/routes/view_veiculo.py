from config import db
from flask import Blueprint, jsonify, request, render_template
from models.veiculo import Veiculo
from models.motorista import Motorista
#from models.trajeto import Trajeto
#from models.ponto_trajeto import PontoTrajeto

veiculo_bp = Blueprint('veiculo_bp', __name__)

@veiculo_bp.route('/create', methods=['POST'])
def create_veiculo():
  """
  Rota para cadastrar veiculos no banco de dados.

  Método:
    POST

  Retorno:
    veiculos cadastrados no banco de dados
  
  """
  data = request.get_json()
  placa = data.get('placa')
  tipo = data.get('tipo')
  modelo = data.get('modelo')
  mac_embarcado = data.get('mac_embarcado')
  
  try:
    veiculo_existente = Veiculo.query.filter_by(placa=placa).first()

  except Exception as e:
    return jsonify({
      "status":"error",
      "message":f"{str(e)}"
    }), 500
  
  if veiculo_existente:
    return jsonify({
      "status":"conflict"
    }), 409
  
  else:
    veiculo = Veiculo(
      placa=placa,
      tipo=tipo,
      modelo=modelo,
      mac_embarcado=mac_embarcado
    )
      
    try:
      db.session.add(veiculo)
      db.session.commit()

    except Exception as e:
      return jsonify({
      "status":"error here",
      "message":f"{str(e)}"
      }), 500
    
    return jsonify({
      "status":"created"
    }), 201

@veiculo_bp.route('/get-all', methods=['GET'])
def get_veiculos():
  """
  Rota para mostrar todos os veiculos

  Método:
    Get

  Retorno:
    JSON listando todos os veiculos
  """
  try:
    veiculos = Veiculo.query.all()

  except Exception as e:
    return jsonify({
      "status":"error",
      "message":f"{str(e)}"
    }), 500
  
  resposta_json = {}

  for veiculo in veiculos:
    resposta_json[veiculo.id] = {
      "placa": veiculo.placa, 
      "tipo": veiculo.tipo
    }

  return jsonify({
    "status":"success",
    "data":resposta_json
    }), 200
  
  
@veiculo_bp.route('/get-all/coord-atual', methods=['GET'])
def get_veiculos_com_coord_atual():
  """
  Rota para mostrar todos os veiculos com suas coordenadas atuais

  Método:
    Get

  Retorno:
    JSON listando todos os veiculos com suas coordenadas atuais
  """
  try:
    veiculos = Veiculo.query.all()

  except Exception as e:
    return jsonify({
      "status":"error",
      "message":f"{str(e)}"
    }), 500

  return jsonify({
    "status":"success",
    "data": [v.to_dict() for v in veiculos]
    }), 200

@veiculo_bp.route('/get/<int:id>', methods=['GET'])
def get_veiculo(id):
  """
  Rota para mostrar um veiculo especifico pelo id informada

  Método:
    Get

  Retorno:
    JSON do veiculo buscado
  """

  try:
    veiculo = Veiculo.query.filter_by(id=id).first()
  
  except Exception as e:
    return jsonify({
      'status':'error',
      'message':f'{str(e)}'
    }), 500
  
  if veiculo:
    resposta_json = {
      "id": veiculo.id,
      "placa": veiculo.placa, 
      "tipo veiculo": veiculo.tipo
    }
    
    return jsonify({
      "data": resposta_json,
      "status": "success"
    }), 200
  else:
    return jsonify({
      'status':'not found'
    }), 404

@veiculo_bp.route('/edit/<int:id>', methods=['PUT'])
def edit_veiculo(id):
  """
  Rota para editar um veiculo com o id informado

  Método:
    PUT

  Retorno:
    JSON mostrando veiculo editado
  """

  data = request.get_json()

  try:
    veiculo = Veiculo.query.filter_by(id=id).first()

  except Exception as e:
    return  jsonify({
      "status":"error",
      "message":f"{str(e)}"
    }), 500
  
  if veiculo:
    placa = data.get('placa')
    tipo = data.get('tipo')

    try:
      veiculo.placa = placa
      veiculo.tipo = tipo
      db.session.commit()
        
    except Exception as e:
      return jsonify({
        "status":"error",
        "message":f"{str(e)}"
      }), 500
        
    return jsonify({
      "status":"updated"
    }), 200
  else:
    return jsonify({
      "status":"not found"
    }), 404

@veiculo_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_veiculo(id):

  data = request.get_json()

  try:
    veiculo = Veiculo.query.filter_by(id=id).first()
  
  except Exception as e:
    return jsonify({
      "status":"error",
      "message":f"{str(e)}"
    }), 500

  if veiculo:
    try:
      Veiculo.query.filter_by(id=id).delete()
    
    except Exception as e:
      return jsonify({
      "status":"error",
      "message":f"{str(e)}"
    }), 500

    db.session.commit()

    return jsonify({
      "status":"deleted"
    }), 200
  else:
    return jsonify({
      "status":"not found"
    }), 404
