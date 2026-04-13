import time

import pygame
import sqlite3
import os
import sys
import getpass
from colorama import Fore, Style, init
init(autoreset=True)

import db

pygame.mixer.init()
  
som_erro = pygame.mixer.Sound("erro.mp3")
dinheirao_ganhar = pygame.mixer.Sound("para-sesi-efekti_PaUswM1.mp3")

pygame.mixer.music.load("Nintendo 3DS Internet Settings Theme (High Quality, 2022 Remastered).mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
logindef = True
admin = True
logado = True
criar_conta = False
adminpass = True
admin_power = False
conn = sqlite3.connect("jogo_palavras.db")
cursor = conn.cursor()

# --- INICIALIZAR MOEDAS ---
cursor.execute("SELECT quantidade FROM moedas WHERE id = 1")
resultado_moedas = cursor.fetchone()
if resultado_moedas:
    moedas = resultado_moedas[0]
else:
    moedas = 0
    cursor.execute("INSERT OR IGNORE INTO moedas (id, quantidade) VALUES (1, ?)", (moedas,))
    conn.commit()
# --------------------------

while logado:
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
        som_erro.play()
        som_erro.set_volume(0.1)
        continue

    if opcaodelogin == 1:
        criar_conta = True
        logado = False
        
    elif opcaodelogin == 2:
        criar_conta = False
        logado = False
    elif opcaodelogin == 3:
        while admin:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("Gran Turismo 6 Soundtrack - annayamada - 4 CHORDS [sT8x_MIgCOE].mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.1)
            print("ADMIN MODE")
            logadm = input("Nome Do Adm: ")
            if logadm == "Admin123":
                print("Nome Correspondido")
            
            else:
                print("Nome Não Correspondido")
                som_erro.play()
                som_erro.set_volume(0.1)
                continue
            
            while adminpass:
                passadm = getpass.getpass("Pass do Adm ")
                if passadm == "123123adm":
                    admin = False
                    logado = False
                    adminpass = False
                    logindef = False
                    admin_power = True
                    break
                    
                    
                else:
                    print("Palavra Pass Não Correspondida")
                    continue
            
        
    else:
        print("Opção inválida!")
        som_erro.play()
        som_erro.set_volume(0.1)
        
        

if admin_power:
    while True:
        print("MODO ADMIN ATIVADO!")
        print("Digite '1' para eliminar uma conta")
        print("Digite '2' para sair do modo admin")
        print("Digite '3' para mostrar contas criadas")
        print("Digite '4' para apagar todas as moedas")
        print("Digite '5' para apagar todas as contas")
        print("Digite '6' para apagar todas as palavras")
        palavra = input("Digite aqui: ")
        
        if palavra == "1":
            nome = input("Digite o nome da conta a apagar: ")
            password = input("Digite a password: ")

            cursor.execute("SELECT * FROM login WHERE nome = ?", (nome,))
            resultado = cursor.fetchone()

            if not resultado:
                print("Conta não encontrada!")
                som_erro.play()
                som_erro.set_volume(0.1)

            elif password != resultado[2]:
                print("Password incorreta!")
                som_erro.play()
                som_erro.set_volume(0.1)

            else:
                cursor.execute("DELETE FROM login WHERE nome = ?", (nome,))
                conn.commit()
                print("Conta apagada com sucesso!")

        elif palavra == "2":
            admin_power = False
            logindef = True
            break
         
            
        elif palavra == "3":
            cursor.execute("SELECT nome, password FROM login")
            contas = cursor.fetchall()

            print("\nContas registadas:")
            for conta in contas:
                print("Nome:", conta[0], "| Password:", conta[1])
        
        elif palavra == "4":
          
            moedas = 0
            cursor.execute("UPDATE moedas SET quantidade = 0 WHERE id = 1")
            conn.commit()
            print("Moedas resetadas com sucesso!")
        
        elif palavra == "5":
        
            cursor.execute("DELETE FROM login")
            conn.commit()
            print("Todas as contas foram apagadas!")
        
        elif palavra == "6":
            
            cursor.execute("DELETE FROM palavras")
            conn.commit()
            print("Todas as palavras foram apagadas!")
   
            


        else:
            print("opção invalida!")
            som_erro.play()
            som_erro.set_volume(0.1)
            continue
        

if criar_conta:
    while True:
        login = input("Crie o seu nome: ")
        cursor.execute("SELECT * FROM login WHERE nome = ?", (login,))
        if cursor.fetchone():
            print("Esse nome já existe! Tenta outro.")
            som_erro.play()
            som_erro.set_volume(0.1)
            continue
        

        password = getpass.getpass("Crie sua palavra pass: ")
        try:
            cursor.execute("INSERT INTO login (nome, password) VALUES (?, ?)", (login, password))
            conn.commit()
            print("Conta criada com sucesso!")
            break
        except sqlite3.IntegrityError:
            print("Erro ao criar conta, tenta outro nome.")
            som_erro.play()
            som_erro.set_volume(0.1)


while logindef:
    login1 = input("Nome da conta: ")

   

    cursor.execute("SELECT * FROM login WHERE nome = ?", (login1,))
    resultado = cursor.fetchone()

    if not resultado:
        print("Conta não encontrada!")
        som_erro.play()
        som_erro.set_volume(0.1)
        continue

    password1 = getpass.getpass("Password: ")
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
    elif palavra == "sair":
        perguntar = False
        print(Fore.RED + "Programa terminado." + Style.RESET_ALL)
        print("Moedas ganhas:", Fore.YELLOW + str(moedas) + Style.RESET_ALL)

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
                continue
            

conn.close()