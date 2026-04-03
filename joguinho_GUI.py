import pygame
import sqlite3
import sys

# =========================
# INICIAR PYGAME
# =========================
pygame.init()
pygame.mixer.init()

LARGURA = 1000
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo das Palavras")

clock = pygame.time.Clock()

# =========================
# CORES (TEMA ANIME)
# =========================
FUNDO = (15, 15, 25)
ROXO = (180, 90, 255)
ROSA = (255, 120, 200)
AZUL = (100, 180, 255)
BRANCO = (240, 240, 240)
CINZA = (60, 60, 80)
PRETO = (0, 0, 0)
VERMELHO = (255, 80, 80)
VERDE = (100, 255, 140)

# =========================
# FONTES
# =========================
fonte_titulo = pygame.font.SysFont("arial", 50, bold=True)
fonte = pygame.font.SysFont("arial", 28)
fonte_pequena = pygame.font.SysFont("arial", 22)

# =========================
# SONS E MÚSICA
# =========================
def carregar_som(caminho, volume=0.5):
    try:
        s = pygame.mixer.Sound(caminho)
        s.set_volume(volume)
        return s
    except:
        print(f"Aviso: {caminho} não encontrado")
        return None

som_erro = carregar_som("erro.mp3", 0.4)
som_ganhar = carregar_som("para-sesi-efekti_PaUswM1.mp3", 0.6)

# =========================
# DATABASE
# =========================
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

# =========================
# FUNÇÕES DB
# =========================
def pegar_moedas():
    cursor.execute("SELECT quantidade FROM moedas WHERE id = 1")
    return cursor.fetchone()[0]

def atualizar_moedas(valor):
    cursor.execute("UPDATE moedas SET quantidade = ? WHERE id = 1", (valor,))
    conn.commit()

def criar_conta(nome, senha):
    cursor.execute("INSERT INTO login (nome, password) VALUES (?, ?)", (nome, senha))
    conn.commit()

def verificar_login(nome, senha):
    cursor.execute("SELECT * FROM login WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()
    if not resultado:
        return False
    return senha == resultado[2]

def palavra_existe(p):
    cursor.execute("SELECT palavra FROM palavras WHERE palavra = ?", (p,))
    return cursor.fetchone() is not None

def adicionar_palavra(p):
    cursor.execute("INSERT INTO palavras (palavra) VALUES (?)", (p,))
    conn.commit()

def pegar_lista_palavras():
    cursor.execute("SELECT palavra FROM palavras ORDER BY palavra ASC")
    return [x[0] for x in cursor.fetchall()]

# =========================
# FUNÇÕES GUI
# =========================
def desenhar_texto(texto, x, y, cor=BRANCO, font=fonte):
    txt = font.render(texto, True, cor)
    TELA.blit(txt, (x, y))

def desenhar_botao(rect, texto, cor_fundo=CINZA, cor_borda=ROXO):
    pygame.draw.rect(TELA, cor_fundo, rect, border_radius=12)
    pygame.draw.rect(TELA, cor_borda, rect, 3, border_radius=12)
    txt = fonte_pequena.render(texto, True, BRANCO)
    TELA.blit(txt, (rect.x + (rect.width - txt.get_width()) // 2,
                    rect.y + (rect.height - txt.get_height()) // 2))

def desenhar_input(rect, texto, ativo):
    cor = ROSA if ativo else BRANCO
    pygame.draw.rect(TELA, (25, 25, 40), rect, border_radius=10)
    pygame.draw.rect(TELA, cor, rect, 2, border_radius=10)
    txt = fonte.render(texto, True, BRANCO)
    TELA.blit(txt, (rect.x + 10, rect.y + 10))

def clicou(rect, pos):
    return rect.collidepoint(pos)

# =========================
# TELAS (ESTADOS)
# =========================
TELA_MENU = "menu"
TELA_LOGIN = "login"
TELA_CRIAR = "criar"
TELA_JOGO = "jogo"
TELA_PALAVRAS = "palavras"

estado = TELA_MENU

# =========================
# VARIÁVEIS
# =========================
mensagem = ""
usuario_logado = ""

login_nome = ""
login_senha = ""
criar_nome = ""
criar_senha = ""

campo_ativo = None

palavra_digitada = ""
moedas = pegar_moedas()
scroll_palavras = 0

musica_atual = None  # controla qual música está tocando

# =========================
# LOOP PRINCIPAL
# =========================
rodando = True
while rodando:
    TELA.fill(FUNDO)

    # ======== FUNDO ANIME (efeito neon)
    pygame.draw.circle(TELA, (90, 40, 120), (200, 120), 160)
    pygame.draw.circle(TELA, (60, 120, 180), (800, 450), 200)
    pygame.draw.circle(TELA, (140, 60, 200), (700, 150), 120)

    # =========================
    # MENU PRINCIPAL
    # =========================
    if estado == TELA_MENU:
        if musica_atual != "menu":
            try:
                pygame.mixer.music.load("Nintendo 3DS Internet Settings Theme (High Quality, 2022 Remastered).mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.2)
                musica_atual = "menu"
            except:
                print("ERRO: música do menu não encontrada!")

        desenhar_texto("Jogo das Palavras", 260, 60, ROXO, fonte_titulo)
        desenhar_texto("Sigma Edition", 380, 130, ROSA, fonte)

        btn_login = pygame.Rect(370, 230, 260, 60)
        btn_criar = pygame.Rect(370, 310, 260, 60)
        btn_sair = pygame.Rect(370, 390, 260, 60)

        desenhar_botao(btn_login, "Fazer Login", cor_borda=AZUL)
        desenhar_botao(btn_criar, "Criar Conta", cor_borda=ROSA)
        desenhar_botao(btn_sair, "Sair", cor_borda=VERMELHO)

        if mensagem:
            desenhar_texto(mensagem, 280, 500, BRANCO, fonte_pequena)

    # =========================
    # LOGIN
    # =========================
    elif estado == TELA_LOGIN:
        if musica_atual != "menu":
            try:
                pygame.mixer.music.load("Nintendo 3DS Internet Settings Theme (High Quality, 2022 Remastered).mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.2)
                musica_atual = "menu"
            except:
                print("ERRO: música do menu não encontrada!")

        desenhar_texto("Login", 450, 60, ROXO, fonte_titulo)
        input_nome = pygame.Rect(300, 200, 400, 55)
        input_senha = pygame.Rect(300, 280, 400, 55)

        btn_entrar = pygame.Rect(300, 370, 190, 55)
        btn_voltar = pygame.Rect(510, 370, 190, 55)

        desenhar_texto("Nome:", 210, 210, BRANCO)
        desenhar_texto("Senha:", 210, 290, BRANCO)

        desenhar_input(input_nome, login_nome, campo_ativo == "login_nome")
        desenhar_input(input_senha, "*" * len(login_senha), campo_ativo == "login_senha")

        desenhar_botao(btn_entrar, "Entrar", cor_borda=VERDE)
        desenhar_botao(btn_voltar, "Voltar", cor_borda=VERMELHO)

        if mensagem:
            desenhar_texto(mensagem, 250, 500, BRANCO, fonte_pequena)

    # =========================
    # CRIAR CONTA
    # =========================
    elif estado == TELA_CRIAR:
        if musica_atual != "menu":
            try:
                pygame.mixer.music.load("Nintendo 3DS Internet Settings Theme (High Quality, 2022 Remastered).mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.2)
                musica_atual = "menu"
            except:
                print("ERRO: música do menu não encontrada!")

        desenhar_texto("Criar Conta", 360, 60, ROXO, fonte_titulo)

        input_nome = pygame.Rect(300, 200, 400, 55)
        input_senha = pygame.Rect(300, 280, 400, 55)

        btn_criar = pygame.Rect(300, 370, 190, 55)
        btn_voltar = pygame.Rect(510, 370, 190, 55)

        desenhar_texto("Nome:", 210, 210, BRANCO)
        desenhar_texto("Senha:", 210, 290, BRANCO)

        desenhar_input(input_nome, criar_nome, campo_ativo == "criar_nome")
        desenhar_input(input_senha, "*" * len(criar_senha), campo_ativo == "criar_senha")

        desenhar_botao(btn_criar, "Criar", cor_borda=ROSA)
        desenhar_botao(btn_voltar, "Voltar", cor_borda=VERMELHO)

        if mensagem:
            desenhar_texto(mensagem, 250, 500, BRANCO, fonte_pequena)

    # =========================
    # JOGO
    # =========================
    elif estado == TELA_JOGO:
        if musica_atual != "jogo":
            try:
                pygame.mixer.music.load("Charlie's Here - Pizza Parlor _ Club Penguin OST.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.2)
                musica_atual = "jogo"
            except:
                print("ERRO: música do jogo não encontrada!")

        desenhar_texto(f"Olá, {usuario_logado}!", 50, 40, ROXO, fonte)
        desenhar_texto(f"Moedas: {moedas}", 780, 40, ROSA, fonte)

        desenhar_texto("Digite uma palavra:", 50, 120, BRANCO, fonte)
        input_palavra = pygame.Rect(50, 170, 500, 55)
        desenhar_input(input_palavra, palavra_digitada, campo_ativo == "palavra")

        btn_verificar = pygame.Rect(580, 170, 160, 55)
        btn_palavras = pygame.Rect(760, 170, 190, 55)
        btn_logout = pygame.Rect(50, 260, 200, 55)
        btn_sair = pygame.Rect(270, 260, 200, 55)

        desenhar_botao(btn_verificar, "Verificar", cor_borda=AZUL)
        desenhar_botao(btn_palavras, "Palavras", cor_borda=ROXO)
        desenhar_botao(btn_logout, "Logout", cor_borda=VERMELHO)
        desenhar_botao(btn_sair, "Sair", cor_borda=VERMELHO)

        if mensagem:
            desenhar_texto(mensagem, 50, 350, BRANCO, fonte)

    # =========================
    # LISTA DE PALAVRAS
    # =========================
    elif estado == TELA_PALAVRAS:
        desenhar_texto("Palavras Guardadas", 300, 40, ROXO, fonte_titulo)
        lista = pegar_lista_palavras()
        area = pygame.Rect(200, 150, 600, 330)
        pygame.draw.rect(TELA, (20, 20, 35), area, border_radius=12)
        pygame.draw.rect(TELA, ROXO, area, 3, border_radius=12)

        TELA.set_clip(area)  # ativa recorte
        y = area.y + 10 - scroll_palavras
        for p in lista:
            desenhar_texto("- " + p, area.x + 20, y, BRANCO, fonte_pequena)
            y += 30
        TELA.set_clip(None)  # desativa recorte

        btn_voltar = pygame.Rect(400, 500, 200, 60)
        desenhar_botao(btn_voltar, "Voltar", cor_borda=VERMELHO)
        desenhar_texto("Use roda do mouse para scroll", 330, 120, ROSA, fonte_pequena)

    # =========================
    # EVENTOS
    # =========================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            # =========================
            # MENU
            # =========================
            if estado == TELA_MENU:
                if clicou(btn_login, pos):
                    mensagem = ""
                    estado = TELA_LOGIN
                elif clicou(btn_criar, pos):
                    mensagem = ""
                    estado = TELA_CRIAR
                elif clicou(btn_sair, pos):
                    rodando = False

            # =========================
            # LOGIN
            # =========================
            elif estado == TELA_LOGIN:
                campo_ativo = "login_nome" if clicou(input_nome, pos) else "login_senha" if clicou(input_senha, pos) else None
                if clicou(btn_voltar, pos):
                    mensagem = ""
                    estado = TELA_MENU
                if clicou(btn_entrar, pos):
                    if verificar_login(login_nome.strip(), login_senha.strip()):
                        usuario_logado = login_nome
                        mensagem = "Login feito com sucesso!"
                        moedas = pegar_moedas()
                        estado = TELA_JOGO
                        campo_ativo = None
                    else:
                        mensagem = "Nome ou senha incorretos!"
                        if som_erro: som_erro.play()

            # =========================
            # CRIAR CONTA
            # =========================
            elif estado == TELA_CRIAR:
                campo_ativo = "criar_nome" if clicou(input_nome, pos) else "criar_senha" if clicou(input_senha, pos) else None
                if clicou(btn_voltar, pos):
                    mensagem = ""
                    estado = TELA_MENU
                if clicou(btn_criar, pos):
                    nome = criar_nome.strip()
                    senha = criar_senha.strip()
                    if nome == "" or senha == "":
                        mensagem = "Preencha tudo!"
                        if som_erro: som_erro.play()
                    else:
                        try:
                            criar_conta(nome, senha)
                            mensagem = "Conta criada com sucesso!"
                            estado = TELA_LOGIN
                            login_nome = nome
                            login_senha = ""
                            criar_nome = ""
                            criar_senha = ""
                        except sqlite3.IntegrityError:
                            mensagem = "Esse nome já existe!"
                            if som_erro: som_erro.play()

            # =========================
            # JOGO
            # =========================
            elif estado == TELA_JOGO:
                campo_ativo = "palavra" if clicou(input_palavra, pos) else None
                if clicou(btn_sair, pos): rodando = False
                if clicou(btn_logout, pos):
                    usuario_logado = ""
                    login_nome = ""
                    login_senha = ""
                    palavra_digitada = ""
                    mensagem = ""
                    estado = TELA_MENU
                if clicou(btn_palavras, pos):
                    scroll_palavras = 0
                    estado = TELA_PALAVRAS
                if clicou(btn_verificar, pos):
                    palavra = palavra_digitada.strip().lower()
                    if palavra == "":
                        mensagem = "Digite uma palavra!"
                        if som_erro: som_erro.play()
                    else:
                        if palavra_existe(palavra):
                            mensagem = f"Conheço sim: {palavra}"
                        else:
                            try:
                                adicionar_palavra(palavra)
                                moedas += 1
                                atualizar_moedas(moedas)
                                mensagem = f"Palavra adicionada! +1 moeda ({palavra})"
                                if som_ganhar: som_ganhar.play()
                            except sqlite3.IntegrityError:
                                mensagem = "Essa palavra já existe!"
                                if som_erro: som_erro.play()
                    palavra_digitada = ""

            # =========================
            # LISTA DE PALAVRAS
            # =========================
            elif estado == TELA_PALAVRAS:
                lista = pegar_lista_palavras()
                altura_total = len(lista) * 30
                limite_scroll = max(0, altura_total - 330)
                if event.button == 4:  # scroll up
                    scroll_palavras = max(0, scroll_palavras - 20)
                if event.button == 5:  # scroll down
                    scroll_palavras = min(limite_scroll, scroll_palavras + 20)
                if clicou(btn_voltar, pos):
                    estado = TELA_JOGO

        # =========================
        # TECLADO
        # =========================
        if event.type == pygame.KEYDOWN:
            if campo_ativo == "login_nome":
                if event.key == pygame.K_BACKSPACE: login_nome = login_nome[:-1]
                else: login_nome += event.unicode
            elif campo_ativo == "login_senha":
                if event.key == pygame.K_BACKSPACE: login_senha = login_senha[:-1]
                else: login_senha += event.unicode
            elif campo_ativo == "criar_nome":
                if event.key == pygame.K_BACKSPACE: criar_nome = criar_nome[:-1]
                else: criar_nome += event.unicode
            elif campo_ativo == "criar_senha":
                if event.key == pygame.K_BACKSPACE: criar_senha = criar_senha[:-1]
                else: criar_senha += event.unicode
            elif campo_ativo == "palavra":
                if event.key == pygame.K_BACKSPACE: palavra_digitada = palavra_digitada[:-1]
                elif event.key == pygame.K_RETURN:
                    # mesmo que botão verificar
                    palavra = palavra_digitada.strip().lower()
                    if palavra != "":
                        if palavra_existe(palavra):
                            mensagem = f"Conheço sim: {palavra}"
                        else:
                            try:
                                adicionar_palavra(palavra)
                                moedas += 1
                                atualizar_moedas(moedas)
                                mensagem = f"Palavra adicionada! +1 moeda ({palavra})"
                                if som_ganhar: som_ganhar.play()
                            except sqlite3.IntegrityError:
                                mensagem = "Essa palavra já existe!"
                                if som_erro: som_erro.play()
                    palavra_digitada = ""
                else:
                    palavra_digitada += event.unicode

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()