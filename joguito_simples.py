import sqlite3
from colorama import Fore, Style, init, Back
init(autoreset=True)

conn = sqlite3.connect("jogo_palavras.db")
cursor = conn.cursor()

# serve para criar tabelas
cursor.execute("""
CREATE TABLE IF NOT EXISTS palavras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    palavra TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS moedas (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    quantidade INTEGER NOT NULL
)
""")

# Garantir que existe a linha das moedas
cursor.execute("INSERT OR IGNORE INTO moedas (id, quantidade) VALUES (1, 0)")
conn.commit()

# Carregar moedas
cursor.execute("SELECT quantidade FROM moedas WHERE id = 1")
moedas = cursor.fetchone()[0]

perguntar = True
print(Style.BRIGHT + Fore.RED + "Olá user!" + Style.RESET_ALL)
while perguntar:
    print(Style.BRIGHT + "Conheço a palavra?\n" + Style.RESET_ALL)
    print(Fore.GREEN + "escreva 'mostrar palavras' para ver as palavras guardadas "+ Style.RESET_ALL)
    print(Fore.YELLOW + "escreva 'mostrar moedas' para ver quantas moedas tens \n" + Style.RESET_ALL)
    palavra = input(Fore.CYAN + Style.BRIGHT + "Escreva a palavra que deseja verificar:" + Style.RESET_ALL).strip().lower()

    if palavra == "mostrar palavras":
        cursor.execute("SELECT palavra FROM palavras")
        palavras = cursor.fetchall()
        print(Fore.GREEN + "Palavras guardadas:", [p[0] for p in palavras])

    elif palavra == "mostrar moedas":
        print(Fore.GREEN + "Moedas:", moedas)

    else:
        cursor.execute("SELECT palavra FROM palavras WHERE palavra = ?", (palavra,))
        resultado = cursor.fetchone()

        if resultado:
            print("Conheço sim a palavra:", palavra)

        else:
            print("Desculpa, mas não conheço.")
            addpala = input("Quer adicionar uma palavra?" + Fore.RED + Style.BRIGHT + " (sim/nao) " + Style.RESET_ALL).strip().lower()

            if addpala == "sim":
                try:
                    cursor.execute("INSERT INTO palavras (palavra) VALUES (?)", (palavra,))
                    moedas += 1
                    cursor.execute("UPDATE moedas SET quantidade = ? WHERE id = 1", (moedas,))
                    conn.commit()
                    print(Fore.YELLOW + "Palavra adicionada! +1 moeda" + Style.RESET_ALL)

                except sqlite3.IntegrityError:
                    print("Essa palavra já existe!")

            elif addpala == "nao":
                perguntar = False
                print(Fore.RED + "Programa terminado." + Style.RESET_ALL)
                print("Moedas ganhas:", Fore.YELLOW + str(moedas) + Style.RESET_ALL)

conn.close()