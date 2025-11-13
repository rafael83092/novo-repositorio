from flask import Flask
import mysql.connector
from flask_bcrypt import Bcrypt
from flask import session

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'uma_chave_segura_aqui'  # troque depois por algo forte

    bcrypt.init_app(app)

    # Conexão com banco MySQL
    def get_db_connection():
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='SENHA_DO_MYSQL',
            database='NOME_DA_SUA_BASE'
        )

    app.config['get_db_connection'] = get_db_connection

    # Registrar blueprint
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
