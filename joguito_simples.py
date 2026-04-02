palavras = []
moedas = 0

perguntar = True
while perguntar:
    print("\nOlá user!")
    palavra = input("Conheço a palavra? ").strip().lower()

    if palavra in palavras:
        print("Conheço sim a palavra:", palavra)

    elif palavra == "mostrar palavras":
        print("Palavras guardadas:", palavras)

    else:
        print("Desculpa, mas não conheço.")
        addpala = input("Quer adicionar uma palavra? (sim/nao) ").strip().lower()

        if addpala == "sim":
            palavras.append(palavra)
            moedas += 1
            print("Palavra adicionada!")

        elif addpala == "nao":
            perguntar = False
            print("Programa terminado.")
            print("Moedas ganhas:", moedas)