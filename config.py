import mysql.connector

def conectar():
    conexao = mysql.connector.connect(
        host="catalogo.cnkocea2idc6.us-east-1.rds.amazonaws.com",
        port=3306,
        database="catalogo",
        user="fivetran",
        password="5SZYV5aBW4N3taDUiZ0zgvEWJj4"
    )
    return conexao