from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
import mysql.connector

auth_bp = Blueprint('auth', __name__, template_folder='templates')
bcrypt = Bcrypt()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    return render_template('cadastro.html')
