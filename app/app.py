from config import app, db
from routes.view_index import view_index
from routes.view_motorista import motorista_bp
from routes.view_ponto_trajeto import ponto_trajeto_bp
# from routes.viewCidadao import view_cidadao
from routes.view_veiculo import veiculo_bp
from routes.view_trajeto import trajeto_bp
# from routes.viewViagem import view_viagem
# from routes.viewAnalise import view_analise

app.register_blueprint(view_index, url_prefix='/')
app.register_blueprint(motorista_bp, url_prefix='/motorista')
# app.register_blueprint(view_cidadao, url_prefix='/cidadao')
# app.register_blueprint(view_trajeto, url_prefix='/trajeto')
app.register_blueprint(veiculo_bp, url_prefix='/veiculo')

# app.register_blueprint(view_viagem, url_prefix='/viagem')
# app.register_blueprint(view_analise, url_prefix='/analise')

import models

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', debug=True)