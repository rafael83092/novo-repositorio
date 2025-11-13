from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_bcrypt import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__)

# 🔹 Cadastro
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        conn = current_app.config['get_db_connection']()
        cursor = conn.cursor(dictionary=True)

        # Verifica se o e-mail já existe
        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash('E-mail já cadastrado!')
            cursor.close()
            conn.close()
            return redirect(url_for('auth.register'))

        # Criptografa a senha antes de salvar
        hash_senha = generate_password_hash(senha).decode('utf-8')

        cursor.execute(
            "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)",
            (nome, email, hash_senha)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Usuário cadastrado com sucesso! Faça login.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# 🔹 Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = current_app.config['get_db_connection']()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['senha'], senha):
            session['usuario_id'] = user['id']
            session['usuario_nome'] = user['nome']
            flash('Login realizado com sucesso!')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('E-mail ou senha incorretos!')
            return redirect(url_for('auth.login'))

    return render_template('login.html')


# 🔹 Dashboard (área interna)
@auth_bp.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        flash('Você precisa fazer login primeiro.')
        return redirect(url_for('auth.login'))

    return f"Bem-vindo, {session['usuario_nome']}!"
