import classes

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

