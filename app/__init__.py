from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'uma_chave_segura_aqui'

    bcrypt.init_app(app)

    # Registrar blueprints
    from app.catalogo.routes import catalogo_bp
    from app.auth.routes import auth_bp

    app.register_blueprint(catalogo_bp, url_prefix='/catalogo')
    app.register_blueprint(auth_bp, url_prefix='/auth')  # <- aqui é crucial

    # Rota raiz redireciona para home do catálogo
    @app.route('/')
    def index():
        return redirect(url_for('catalogo.home'))

    return app
