import json
from Classes.classes import (Avaliacao, Colecao, Jogo, Relatorio_resumido, 
                             Relatorio_horas, Relatorio_plataforma)


def inicializar():
    colecao = Colecao()
    #carregando a lista de jogos a partir da função carregar q le o json
    colecao.lista_de_jogos = carregar()
    while True:
        print("====POOGAMES====")
        print("Qual ação deseja realizar?")
        print("0-SAIR DO PROGRAMA")
        print("1-CADASTRAR JOGOS")
        print("2-MOSTRAR RESUMO DE UM JOGO")
        print("3-AVALIAR UM JOGO")
        print("4-MOSTRAR A COLEÇÃO")
        print("5-GERAR RELATÓRIO")
        x = int(input())
        print("===============")
        if x == 0: 
            break
        elif x == 1:
            cadastrar_jogo(colecao)
            salvar(colecao)
        elif x == 2:
            mostrar_resumo(colecao)
        elif x == 3:
            avaliacao(colecao)
        elif x == 4:
            mostrar_colecao(colecao)
        elif x ==5:
            gerar_relatorio(colecao)



def cadastrar_jogo(colecao):
    print("====CADASTRO DE JOGOS====")
    titulo = input("Digite o título do jogo: ")
    genero = input("Digite o gênero do jogo: ")
    plataforma = input("Digite a plataforma do jogo: ")
    status = input("Digite o status do jogo: ")
    horas = int(input("Digite as horas jogadas: "))

    jogo = Jogo(titulo, genero, plataforma, status, horas)

    print("Jogo cadastrado com sucesso!")
    colecao.adicionar_jogos(jogo)

def atualizar_horas(jogo):
    try:
        horas = int(input("Digite as horas jogadas: "))
        jogo.horas += horas 
    except ValueError:
        print("Digite um número como horas jogadas! ")


def mostrar_resumo(colecao):
    print("Qual jogo vc deseja verificar o resumo?")
    nome = input()
    for jogo in colecao.lista_de_jogos:
        if nome.lower() == jogo.titulo.lower():
            print(jogo)
            break
    else: 
        print("Jogo não encontrado")


def avaliacao(colecao): 
    #conferir se a colecao está vazia
    if not colecao.lista_de_jogos: 
        print("A lista de jogos está vazia!")
        #return usado para encerrar o fluxo caso não haja jogos na coleção ainda
        return
    #necessário passar os parametros necessários da avaliação (nota, jogo...)
    titulo = input("Qual jogo você deseja avaliar?")
    for jogo in colecao.lista_de_jogos:
        if jogo.titulo.lower() == titulo.lower():
            nota = int(input(f"Qual nota você dá para {titulo}?"))
            favoritado = input("Deseja favoritar o jogo? S/N")
            if favoritado.upper() == "S":
                favoritado = True
            else:
                favoritado = False
            avaliacao = Avaliacao(nota, jogo, favoritado)
            resultado = jogo.avaliar_jogo(avaliacao)
            if resultado:
                print(resultado)
            break
    else: 
        print("Jogo não encontrado na coleção!")

def salvar(colecao):
    dados = [jogo.to_dict() for jogo in colecao.lista_de_jogos]
    with open("/home/diogo/POO/data/colecao.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar():
    try:
        with open("/home/diogo/POO/data/colecao.json", "r") as f:
            lista = json.load(f)
    except:
        return []
    
    jogos = [Jogo.from_dict(jogo) for jogo in lista]
    return jogos
    
def mostrar_colecao(colecao):
    if not colecao.lista_de_jogos:
        print("Coleção vazia!")
        return
    for jogo in colecao.lista_de_jogos:
        dados = jogo.to_dict()
        for chave, valor in dados.items():
            print(f"{chave}: {valor}")
        print("---------------")    
    print("==============\n")

def gerar_relatorio(colecao):
    print("QUAL TIPO DE RELATÓRIO VOCÊ DESEJA GERAR?")
    print("1-RELATÓRIO RESUMIDO")
    print("2-RELATORIO DE HORAS")
    print("3-RELATORIO POR PLATAFORMA")
    x = int(input("Digite a sua opção: "))

    if x == 1: 
       Relatorio_resumido(colecao).gerar()
    elif x == 2:
        Relatorio_horas(colecao).gerar()
    elif x == 3:
        Relatorio_plataforma(colecao).gerar()
    else:
        print("Digite uma opção válida!")