from config import conectar

try:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    print("✅ Conectado com sucesso ao banco:", cursor.fetchone()[0])
    cursor.close()
    conn.close()
except Exception as e:
    print("❌ Erro ao conectar ao MySQL:", e)
