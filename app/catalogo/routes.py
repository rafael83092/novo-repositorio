from flask import Blueprint, render_template, request, redirect, url_for
from config import conectar  # função que retorna a conexão MySQL

catalogo_bp = Blueprint('catalogo', __name__, template_folder='templates')

@catalogo_bp.route('/')
def home():
    return render_template('home.html')

@catalogo_bp.route('/produto', methods=['GET', 'POST'])
def produto():
    # --- BUSCA ---
    termo = request.args.get('termo', '')

    # --- PAGINAÇÃO ---
    page = int(request.args.get('page', 1))
    per_page = 50
    offset = (page - 1) * per_page

    # --- ORDENAÇÃO ---
    order = request.args.get('order', 'sku')

    # Segurança: só aceita colunas existentes
    colunas_validas = ['sku', 'nome_site', 'seller', 'preco']
    if order not in colunas_validas:
        order = 'sku'

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    # --- CONTAR TOTAL ---
    if termo:
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM produto
            WHERE sku LIKE %s OR nome_site LIKE %s
        """, (f"%{termo}%", f"%{termo}%"))
    else:
        cursor.execute("SELECT COUNT(*) AS total FROM produto")

    total = cursor.fetchone()['total']
    total_pages = (total // per_page) + (1 if total % per_page else 0)

    # --- BUSCA COM PAGINAÇÃO + ORDENAÇÃO ---
    if termo:
        cursor.execute(f"""
            SELECT sku, nome_site, seller, preco
            FROM produto
            WHERE sku LIKE %s OR nome_site LIKE %s
            ORDER BY {order}
            LIMIT %s OFFSET %s
        """, (f"%{termo}%", f"%{termo}%", per_page, offset))
    else:
        cursor.execute(f"""
            SELECT sku, nome_site, seller, preco
            FROM produto
            ORDER BY {order}
            LIMIT %s OFFSET %s
        """, (per_page, offset))

    produtos = cursor.fetchall()

    # --- Corrige preço vindo como string ---
    for p in produtos:
        try:
            p['preco'] = float(p['preco'])
        except:
            p['preco'] = 0.0

    cursor.close()
    conn.close()

    # --- RETORNO ---
    return render_template(
        'produto.html',
        produtos=produtos,
        termo=termo,
        page=page,
        total_pages=total_pages,
        per_page=per_page,
        order=order
    )




@catalogo_bp.route('/dashboard')
def dashboard():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total_produtos FROM produto")
    total_produtos = cursor.fetchone()['total_produtos']

    cursor.execute("SELECT COUNT(DISTINCT seller) AS total_sellers FROM produto")
    total_sellers = cursor.fetchone()['total_sellers']

    cursor.execute("""
        SELECT categoria, COUNT(*) AS total
        FROM produto
        GROUP BY categoria
        ORDER BY total DESC
        LIMIT 10
    """)
    categorias = cursor.fetchall()

    cursor.close()
    conn.close()

    labels = [c['categoria'] for c in categorias]
    valores = [c['total'] for c in categorias]

    return render_template(
        'dashboard.html',
        total_produtos=total_produtos,
        total_sellers=total_sellers,
        labels=labels,
        valores=valores
    )


@catalogo_bp.route('/novo', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        sku = request.form['sku']
        nome_site = request.form['nome_site']
        seller = request.form['seller']
        categoria = request.form.get('categoria', '')

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produto (sku, nome_site, seller, categoria) VALUES (%s, %s, %s, %s)",
            (sku, nome_site, seller, categoria)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('catalogo.produto'))

    return render_template('novo_produto.html')


@catalogo_bp.route('/buscar', methods=['GET'])
def buscar_produto():
    q = request.args.get('q', '')
    resultados = []

    if q:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT sku, nome_site, seller, categoria FROM produto WHERE sku LIKE %s OR nome_site LIKE %s OR seller LIKE %s",
            (f"%{q}%", f"%{q}%", f"%{q}%")
        )
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()

    return render_template('buscar_produto.html', resultados=resultados)

