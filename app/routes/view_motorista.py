from config import db
from flask import Blueprint, request, jsonify, render_template
from models.motorista import Motorista
from models.veiculo import Veiculo

view_motorista = Blueprint('view_motorista', __name__)

@view_motorista.route('/create', methods=['POST'])
def cerate_motorista():
    """
    Rota para cadastrar um motorista no banco de dados.
    """

    data = request.get_json() # pega todos os dados passados pelo body

    cnh = data.get('cnh') 
    cpf= data.get('cpf') 
    nome = data.get('nome') 
    senha = data.get('senha') 
    role = data.get('role') 
    veiculo_id = data.get('veiculo-id')

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
    

@view_motorista.route('/get-all', methods=['GET'])
def get_motoristas():
    """
    Rota para mostrar todos os motoristas

    Método:
        Get

    Retorno:
        JSON listando todos os motoristas
    """
    try:
        motoristas = Motorista.query.all()

    except Exception as e:
        return jsonify({
            'status':'error',
            'message':f'{str(e)}'
        }), 500
    
    resposta_json = {}

    for motorista in motoristas:
        resposta_json[motorista.id] = {"nome completo":motorista.nome_completo, "cpf":motorista.cpf, "senha":motorista.senha, "role":motorista.role, "Veiculos":motorista.veiculos, "cnh":motorista.cnh}

    return jsonify({
        "status":"success",
        "data":resposta_json
        }), 200

@view_motorista.route('/get/<int:id>', methods=['GET'])
def get_motorista(id):
    """
    Rota para mostrar um motorista pelo id passado pela URL

    Método:
        Get

    Retorno:
        JSON do motorista buscado
    """

    try:
        motorista = Motorista.query.filter_by(id=id).first()

    except Exception as e:
        return jsonify({
            'status':'error',
            'message':f'{str(e)}'
        }), 500
    
    if motorista:
        resposta_json = {
            "id": motorista.id,
            "nome completo": motorista.nome_completo, 
            "cpf":motorista.cpf, 
            "senha":motorista.senha, 
            "role":motorista.role, 
            "veiculos":motorista.veiculos, 
            "cnh":motorista.cnh
        }

        return jsonify({
            "status":"success",
            "data":resposta_json
        }), 200
    
    else:
        return jsonify({
            'status':'not found'
        }), 404

@view_motorista.route('/delete/<int:id>', methods=['DELETE'])
def delete_motorista(id):
    """
    Rota para deletar um motorista com o id informado

    Método:
        DELETE

    Retorno:
        JSON indicando que o motorista foi deletado
    """
    
    try:
        motorista = Motorista.query.filter_by(id=id).first()
    
    except Exception as e:
        return jsonify({
            'status':'error',
            'message':f'{str(e)}'
        }), 500
    
    if motorista:
        try:
            Motorista.query.filter_by(id=motorista.id).delete()
            db.session.commit()
        
        except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            }), 500
        
        return jsonify({
            "status":"deleted"
        }), 200
    else: 
        return jsonify({
            "status": "not found"
        }), 404


@view_motorista.route('/put/<int:id>', methods=['PUT'])
def edit_motorista(id):
    """
    Rota para editar um motorista com o id informado

    Método:
        PUT

    Retorno:
        JSON mostrando motorista editado
    """

    data = request.get_json()
    
    try:
        motorista = Motorista.query.filter_by(id=id).first()

    except Exception as e:
        return jsonify({
            'status':'error',
            'message':f'{str(e)}'
        }), 500
    
    if motorista:
        nome = data.get('nome')
        cnh = data.get('cnh')
        cpf = data.get('cpf')
        senha = data.get('senha')
        role = data.get('role')

        try:
            motorista.nome_completo = nome
            motorista.cnh = cnh
            motorista.cpf = cpf
            motorista.senha = senha
            motorista.role = role
            db.session.commit()

        except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            }), 500

        return jsonify({
            "status":"updated",
        }), 200
    else:
        return jsonify({
            "status":"not found",
        }), 404