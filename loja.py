import pygame

# =========================
# LOJA
# =========================
def abrir_loja(tela, usuario, moedas, som_erro=None):
    rodando = True
    fonte = pygame.font.SysFont("arial", 28)
    fonte_pequena = pygame.font.SysFont("arial", 22)
    FUNDO = (15, 15, 25)
    BRANCO = (240, 240, 240)
    ROXO = (180, 90, 255)
    CINZA = (60, 60, 80)
    VERDE = (100, 255, 140)
    VERMELHO = (255, 80, 80)

    # Produtos da loja
    produtos = [
        {"nome": "Potion", "preco": 2},
        {"nome": "Mega Tocha", "preco": 5},
        {"nome": "Boost XP", "preco": 3}
    ]

    while rodando:
        tela.fill(FUNDO)
        pygame.draw.rect(tela, (30,30,50), (100, 100, 800, 400), border_radius=12)
        pygame.draw.rect(tela, ROXO, (100, 100, 800, 400), 3, border_radius=12)

        # Título
        txt = fonte.render("Loja", True, ROXO)
        tela.blit(txt, (460, 110))
        txt_user = fonte_pequena.render(f"Usuário: {usuario}  Moedas: {moedas}", True, BRANCO)
        tela.blit(txt_user, (350, 150))

        # Desenhar produtos
        for i, prod in enumerate(produtos):
            rect = pygame.Rect(150, 200 + i*70, 600, 50)
            pygame.draw.rect(tela, CINZA, rect, border_radius=10)
            pygame.draw.rect(tela, ROXO, rect, 2, border_radius=10)
            txt_nome = fonte_pequena.render(f"{prod['nome']} - {prod['preco']} moedas", True, BRANCO)
            tela.blit(txt_nome, (rect.x + 20, rect.y + 10))

        # Botão voltar
        btn_voltar = pygame.Rect(400, 500, 200, 50)
        pygame.draw.rect(tela, VERMELHO, btn_voltar, border_radius=10)
        pygame.draw.rect(tela, ROXO, btn_voltar, 2, border_radius=10)
        txt_voltar = fonte_pequena.render("Voltar", True, BRANCO)
        tela.blit(txt_voltar, (btn_voltar.x + 70, btn_voltar.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if btn_voltar.collidepoint(pos):
                    rodando = False
                # Comprar produtos
                for prod in produtos:
                    rect = pygame.Rect(150, 200 + produtos.index(prod)*70, 600, 50)
                    if rect.collidepoint(pos):
                        if moedas >= prod['preco']:
                            moedas -= prod['preco']
                            # aqui você pode adicionar item ao inventário
                        else:
                            if som_erro: som_erro.play()

        pygame.display.flip()