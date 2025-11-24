import classes

def inicializar():
    while True:
        print("====POOGAMES====")
        print("Qual ação deseja realizar?")
        print("0-SAIR DO PROGRAMA")
        print("1-CADASTRAR JOGOS")
        print("2-RESUMO DE UM JOGO")
        x = int(input())
        if x == 0: 
            break
        elif x == 1:
            cadastrar_jogo()
        elif x == 2:
            ...
        elif x == 3: 
            atualizar_horas()


def cadastrar_jogo():
    print("==CADASTRO DE JOGOS==")
    titulo = input("Digite o título do jogo: ")
    genero = input("Digite o gênero do jogo: ")
    plataforma = input("Digite a plataforma do jogo: ")

    Jogo = Jogo(titulo, genero, plataforma)

    print("Jogo cadastrado com sucesso!")
    return Jogo

def atualizar_horas(jogo):
    try:
        horas = int(input("Digite as horas jogadas: "))
        jogo.horas += horas 
    except ValueError:
        print("Digite um número como horas jogadas! ")

def mostrar_resumo():
    print("Qual jogo vc deseja verificar o resumo?")
    nome = input()
    if self.titulo == nome:
        print(jogo)
    else:
        print("O jogo não existe na coleção")