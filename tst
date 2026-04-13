conn = sqlite3.connect("jogo_palavras.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS palavras (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    palavra TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS moedas (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    quantidade INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS login (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")


cursor.execute("INSERT OR IGNORE INTO moedas (id, quantidade) VALUES (1, 0)")
conn.commit()


cursor.execute("SELECT quantidade FROM moedas WHERE id = 1")
moedas = cursor.fetchone()[0]