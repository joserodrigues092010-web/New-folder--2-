import time
import pygame
import sqlite3
from colorama import Fore, Style, init
init(autoreset=True)


pygame.mixer.init()  
som_erro = pygame.mixer.Sound("erro.mp3")
dinheirao_ganhar = pygame.mixer.Sound("para-sesi-efekti_PaUswM1.mp3")


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


pygame.mixer.music.load("Nintendo 3DS Internet Settings Theme (High Quality, 2022 Remastered).mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

logao = True
criar_conta = False

while logao:
    print(Style.BRIGHT + Fore.CYAN + "="*50)
    print(Style.BRIGHT + Fore.MAGENTA + "         BEM-VINDO AO JOGO DAS PALAVRAS!  ")
    print(Style.BRIGHT + Fore.CYAN + "="*50)
    print("Opções de Login")
    print("Se for novo utilizador digite 1")
    print("Se já tiver conta criada digite 2")
    
    try:
        opcaodelogin = int(input("Digite opção: "))
    except ValueError:
        print("Escreve apenas números!")
        continue

    if opcaodelogin == 1:
        criar_conta = True
        logao = False
    elif opcaodelogin == 2:
        criar_conta = False
        logao = False
    else:
        print("Opção inválida!")


if criar_conta:
    while True:
        login = input("Crie o seu nome: ")
        cursor.execute("SELECT * FROM login WHERE nome = ?", (login,))
        if cursor.fetchone():
            print("Esse nome já existe! Tenta outro.")
            som_erro.play()
            som_erro.set_volume(0.1)
            continue

        password = input("Crie sua palavra pass: ")
        try:
            cursor.execute("INSERT INTO login (nome, password) VALUES (?, ?)", (login, password))
            conn.commit()
            print("Conta criada com sucesso!")
            break
        except sqlite3.IntegrityError:
            print("Erro ao criar conta, tenta outro nome.")
            som_erro.play()
            som_erro.set_volume(0.1)


while True:
    login1 = input("Nome da conta: ")
    cursor.execute("SELECT * FROM login WHERE nome = ?", (login1,))
    resultado = cursor.fetchone()
    if not resultado:
        print("Conta não encontrada!")
        som_erro.play()
        som_erro.set_volume(0.1)
        continue

    password1 = input("Password: ")
    if password1 != resultado[2]:  
        print("Password incorreta!")
        som_erro.play()
        som_erro.set_volume(0.1)
        continue

    print("Login feito com sucesso!")
    print("Fazendo Login na conta...")
    time.sleep(2)
    pygame.mixer.music.stop()
    break


pygame.mixer.music.load("Charlie's Here - Pizza Parlor _ Club Penguin OST.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)


perguntar = True
print(Style.BRIGHT + Fore.RED + f"Olá {login1}!" + Style.RESET_ALL)

while perguntar:
    print(Style.BRIGHT + "Conheço a palavra?\n" + Style.RESET_ALL)
    print(Fore.GREEN + "Escreva 'mostrar palavras' para ver as palavras guardadas " + Style.RESET_ALL)
    print(Fore.YELLOW + "Escreva 'mostrar moedas' para ver quantas moedas tens \n" + Style.RESET_ALL)
    
    palavra = input(Fore.CYAN + Style.BRIGHT + "Escreva a palavra que deseja verificar: " + Style.RESET_ALL).strip().lower()

    if palavra == "mostrar palavras":
        cursor.execute("SELECT palavra FROM palavras")
        palavras = cursor.fetchall()
        print(Fore.GREEN + "Palavras guardadas:", [p[0] for p in palavras])

    elif palavra == "mostrar moedas":
        print(Fore.GREEN + "Moedas:", moedas)
        dinheirao_ganhar.play()
        dinheirao_ganhar.set_volume(0.6)

    else:
        cursor.execute("SELECT palavra FROM palavras WHERE palavra = ?", (palavra,))
        resultado = cursor.fetchone()

        if resultado:
            print("Conheço sim a palavra:", palavra)
        else:
            print("Desculpa, mas não conheço.")
            addpala = input("Quer adicionar essa palavra?" + Fore.RED + Style.BRIGHT + " (sim/nao) " + Style.RESET_ALL).strip().lower()
            if addpala == "sim":
                try:
                    cursor.execute("INSERT INTO palavras (palavra) VALUES (?)", (palavra,))
                    moedas += 1
                    cursor.execute("UPDATE moedas SET quantidade = ? WHERE id = 1", (moedas,))
                    conn.commit()
                    print(Fore.YELLOW + "Palavra adicionada! +1 moeda" + Style.RESET_ALL)
                    dinheirao_ganhar.play()
                    dinheirao_ganhar.set_volume(0.6)
                except sqlite3.IntegrityError:
                    print("Essa palavra já existe!")
            elif addpala == "nao":
                perguntar = False
                print(Fore.RED + "Programa terminado." + Style.RESET_ALL)
                print("Moedas ganhas:", Fore.YELLOW + str(moedas) + Style.RESET_ALL)

conn.close()