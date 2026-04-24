registros = []

def registrar_emocao():
    print("\nQuero te ouvir um pouco...")
    
    nome = input("Como posso te chamar? ").strip()
    if not nome:
        print("Hmm… preciso de um nome pra continuar.")
        return
    
    emocao = input(f"{nome}, como você está se sentindo agora? ").lower().strip()
    if not emocao:
        print("Tá tudo bem se for difícil explicar, mas tenta colocar em palavras.")
        return
    
    try:
        intensidade = int(input("De 1 a 10, quão forte é esse sentimento? "))
        if intensidade < 1 or intensidade > 10:
            print("Vamos manter entre 1 e 10, tá?")
            return
    except ValueError:
        print("Ops… preciso de um número pra entender melhor.")
        return
    
    registros.append({
        "nome": nome,
        "emocao": emocao,
        "intensidade": intensidade
    })
    
    print(f"Obrigado por compartilhar isso comigo, {nome}.")

def mostrar_registros():
    print("\nDeixa eu ver o que você já compartilhou comigo...")
    
    if not registros:
        print("Ainda não tenho registros seus.")
        return
    
    for r in registros:
        print(f"{r['nome']} estava se sentindo {r['emocao']} (nível {r['intensidade']})")

def analisar_humor():
    print("\nVou tentar entender como você tem se sentido no geral...")
    
    if not registros:
        print("Ainda não tenho informações suficientes.")
        return
    
    media = sum(r["intensidade"] for r in registros) / len(registros)
    
    print(f"Pelo que vi, sua média emocional está em {media:.1f}.")
    
    if media <= 3:
        print("Parece que você pode estar passando por um momento mais pesado.")
        print("Talvez descansar um pouco ou conversar com alguém de confiança ajude.")
    elif media <= 6:
        print("Você está em um estado mais equilibrado, com altos e baixos normais.")
        print("Tentar manter uma rotina saudável pode ajudar bastante.")
    else:
        print("Você parece estar em um momento positivo!")
        print("Vale a pena continuar fazendo o que tem te feito bem.")

def emocao_mais_frequente():
    print("\nDeixa eu ver qual sentimento aparece mais...")
    
    if not registros:
        print("Ainda não tenho dados suficientes.")
        return
    
    contagem = {}
    
    for r in registros:
        e = r["emocao"]
        contagem[e] = contagem.get(e, 0) + 1
    
    mais_comum = max(contagem, key=contagem.get)
    
    print(f"Pelo que percebi, você tem se sentido mais: {mais_comum}")

def despedida():
    print("\nAntes de ir...")
    print("Lembre-se: entender o que você sente já é um grande passo.")
    print("Você não precisa carregar tudo sozinho.")
    print("Até a próxima!")

def menu():
    print("Olá... eu tô aqui pra te ajudar a se entender melhor.")
    
    while True:
        print("\nO que você quer fazer agora?")
        print("1 - Registrar como estou me sentindo")
        print("2 - Ver meus registros")
        print("3 - Analisar meu momento")
        print("4 - Ver sentimento mais frequente")
        print("5 - Sair")
        
        op = input("Escolha uma opção: ")
        
        if op == "1":
            registrar_emocao()
        elif op == "2":
            mostrar_registros()
        elif op == "3":
            analisar_humor()
        elif op == "4":
            emocao_mais_frequente()
        elif op == "5":
            despedida()
            break
        else:
            print("Hmm… não entendi essa opção.")

menu()