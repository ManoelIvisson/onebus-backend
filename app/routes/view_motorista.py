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
    # return render_template('todos_motoristas.html', all_motoristas=motoristas), 302

@view_motorista.route('/motorista-especifico', methods=['GET', 'POST'])
def get_especific_motorista():
    """
    Rota para mostrar um motorista especifico pela cnh informada

    Método:
        Get

    Retorno:
        Página listando motorista especifico
    """

    data = request.get_json()
    cnh_desejado = data.get('motorista-cnh')

    try:
        motorista = Motorista.query.filter_by(cnh=cnh_desejado).first()

    except Exception as e:
        return jsonify({
            'status':'error',
            'message':f'{str(e)}'
        }), 500
    
    if motorista:
        resposta_json = {"nome completo":motorista.nome_completo, "cpf":motorista.cpf, "senha":motorista.senha, "tipo usuario":motorista.tipo_usuario, "placa do carro":motorista.carro_placa, "cnh":motorista.cnh}

        return jsonify({
            "status":"success",
            "data":resposta_json
        }), 200
    
    else:
        return jsonify({
            'status':'not found'
        }), 404

@view_motorista.route('/excluir-motorista', methods=['GET', 'DELETE'])
def delete_motorista():
    """
    Rota para deletar um motorista específico com o cpf informado

    Método:
        Get, Post

    Retorno:
        Página indicando motorista deletado
    """
    if request.method == 'DELETE':
        cpf_motorista = request.form.get('motorista-cpf')
        
        try:
            motorista = Motorista.query.filter_by(cpf=cpf_motorista).first()
        
        except Exception as e:
            return jsonify({
                'status':'error',
                'message':f'{str(e)}'
            }), 500
        
        if motorista:
            try:
                Motorista.query.filter_by(cpf=cpf_motorista).delete()
                db.session.commit()
            
            except Exception as e:
                return jsonify({
                    "status":"error",
                    "message":f"{str(e)}"
                }), 500
            
            return jsonify({
                "status":"deleted"
            }), 204
        
        else:
            return jsonify({
                "status":"not found"
            }), 404
        
    # return render_template('motoristas.html'), 302

@view_motorista.route('/alterar-motorista', methods=['GET', 'PATCH'])
def edit_motorista():
    """
    Rota para editar um motorista específico com o cpf informado

    Método:
        Get, Patch

    Retorno:
        Página mostrando motorista editado
    """

    if request.method == 'PATCH':
        data = request.get_json()
        cpf_motorista = data.get('motorista-cpf')
        
        try:
            motorista = Motorista.query.filter_by(cpf=cpf_motorista).first()

        except Exception as e:
            return jsonify({
                'status':'error',
                'message':f'{str(e)}'
            }), 500
        
        if motorista:
            new_nome = data.get('motorista-nome')
            new_placa = data.get('placa-carro')
            # new_cnh = data.get('motorista-cnh')
            # new_tipo_usuario = data.get('tipo-usuario')

            if new_nome != motorista.nome_completo and new_nome != None:
                try:
                    motorista.nome_completo = new_nome
                    db.session.commit()

                except Exception as e:
                    return jsonify({
                        "status":"error",
                        "message":f"{str(e)}"
                    }), 500
            
            if new_placa != motorista.carro_placa and new_placa != None:
                try:
                    carro_desejado = Veiculo.query.filter_by(placa=new_placa).first()

                    if carro_desejado:
                        carro_desejado.motorista_cnh.append(motorista)
                        db.session.commit()

                    else:
                        return jsonify({
                            "status":"not found",
                        }), 404

                except Exception as e:
                    return jsonify({
                        "status":"error",
                        "message":f"{str(e)}"
                    }), 500
            
            # db.session.commit()
            return jsonify({
                "status":"updated",
            }), 204

        else:
            return jsonify({
                "status":"not found",
            }), 404