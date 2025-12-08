import json
from Classes.classes import (Avaliacao, Colecao, Jogo, Relatorio_resumido, 
                             Relatorio_horas, Relatorio_media_avaliacao, Relatorio_percentual_status, Relatorio_top5)


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
        print("6-FILTRAR COLECAO")
        print("7-ATUALIZAR HORAS DE UM JOGO")
        print("8-ATUALIZAR STATUS DE UM JOGO")
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
        elif x == 5:
            gerar_relatorio(colecao)
        elif x == 6:
            mostrar_colecao_filtrada(colecao)
        elif x == 7:
            atualizar_horas_cli(colecao)
            salvar(colecao)
        elif x == 8:
            atualizar_status_cli(colecao)
            salvar(colecao)



def cadastrar_jogo(colecao):
    print("====CADASTRO DE JOGOS====")
    titulo = input("Digite o título do jogo: ")
    genero = input("Digite o gênero do jogo: ")
    plataforma = input("Digite a plataforma do jogo: ")
    status = input("Digite o status do jogo: ")
    try:
        horas_input = input("Digite as horas jogadas: ")
        horas = int(horas_input)
    except ValueError:
        print("Horas inválidas. Retornando ao menu.")
        return

    try:
        # normalizar status informado pelo usuário
        try:
            from Classes.classes import Jogo as JogoClass
            status_clean = JogoClass.normalize_status(status)
        except Exception:
            status_clean = status
        jogo = Jogo(titulo, genero, plataforma, status_clean, horas)
    except ValueError as e:
        print(f"Erro ao cadastrar jogo: {e}. Retornando ao menu.")
        return

    resultado = colecao.adicionar_jogos(jogo)
    print(resultado)

def atualizar_horas(jogo):
    try:
        horas = int(input("Digite as horas jogadas: "))
        if horas < 0:
            print("Não é permitido subtrair horas. Retornando ao menu.")
            return
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
            try:
                avaliacao = Avaliacao(nota, jogo, favoritado)
                resultado = jogo.avaliar_jogo(avaliacao)
                if resultado:
                    print(resultado)
            except ValueError as e:
                print(f"Erro na avaliação: {e}. Retornando ao menu.")
            break
    else: 
        print("Jogo não encontrado na coleção!")


def atualizar_horas_cli(colecao):
    print("===Atualizar horas de um jogo===")
    titulo = input("Digite o título do jogo: ")
    plataforma = input("Digite a plataforma do jogo (enter para pular): ")
    for jogo in colecao.lista_de_jogos:
        if jogo.titulo.lower() == titulo.lower() and (not plataforma or jogo.plataforma.lower() == plataforma.lower()):
            atualizar_horas(jogo)
            return
    print("Jogo não encontrado. Retornando ao menu.")


def atualizar_status_cli(colecao):
    print("===Atualizar status de um jogo===")
    titulo = input("Digite o título do jogo: ")
    plataforma = input("Digite a plataforma do jogo (enter para pular): ")
    novo_status = input("Digite o novo status: ")
    for jogo in colecao.lista_de_jogos:
        if jogo.titulo.lower() == titulo.lower() and (not plataforma or jogo.plataforma.lower() == plataforma.lower()):
            try:
                # normalizar usando o método da classe
                from Classes.classes import Jogo as JogoClass
                jogo.status = JogoClass.normalize_status(novo_status)
                print("Status atualizado com sucesso.")
            except ValueError as e:
                print(f"Erro ao atualizar status: {e}. Retornando ao menu.")
            return
    print("Jogo não encontrado. Retornando ao menu.")

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
        # imprimir só os campos principais e a média de avaliações
        print(f"titulo: {dados.get('titulo')}")
        print(f"genero: {dados.get('genero')}")
        print(f"plataforma: {dados.get('plataforma')}")
        print(f"status: {dados.get('status')}")
        print(f"horas: {dados.get('horas')}")
        # calcular media a partir das avaliacoes do objeto
        if hasattr(jogo, '_avaliacoes') and jogo._avaliacoes:
            media = sum(av.nota for av in jogo._avaliacoes) / len(jogo._avaliacoes)
            print(f"media_avaliacoes: {media:.2f}")
        else:
            print("media_avaliacoes: N/A")
        print("---------------")    
    print("==============\n")

def mostrar_colecao_filtrada(colecao):
    print("===Filtro da coleção===")
    genero = input("Gênero (enter para pular): ")
    status = input("Status (enter para pular): ")
    plataforma = input("Plataforma (enter para pular): ")
    # normalizar entradas vazias para None
    genero = genero or None
    status = status or None
    plataforma = plataforma or None
    resultados = colecao.filtrar(genero=genero, status=status, plataforma=plataforma)
    if not resultados:
        print("Nenhum jogo encontrado com esses filtros.")
        return
    for jogo in resultados:
        dados = jogo.to_dict()
        print(f"titulo: {dados.get('titulo')}")
        print(f"genero: {dados.get('genero')}")
        print(f"plataforma: {dados.get('plataforma')}")
        print(f"status: {dados.get('status')}")
        print(f"horas: {dados.get('horas')}")
        if hasattr(jogo, '_avaliacoes') and jogo._avaliacoes:
            media = sum(av.nota for av in jogo._avaliacoes) / len(jogo._avaliacoes)
            print(f"media_avaliacoes: {media:.2f}")
        else:
            print("media_avaliacoes: N/A")
        print("---------------")

def gerar_relatorio(colecao):
    print("QUAL TIPO DE RELATÓRIO VOCÊ DESEJA GERAR?")
    print("1-RELATÓRIO RESUMIDO")
    print("2-RELATORIO DE HORAS")
    print("3-RELATORIO MÉDIA DE AVALIAÇÕES")
    print("4-RELATORIO PERCENTUAL DE JOGOS POR STATUS")
    print("5-TOP 5 JOGOS MAIS JOGADOS")
    x = int(input("Digite a sua opção: "))

    if x == 1: 
       Relatorio_resumido(colecao).gerar()
    elif x == 2:
        Relatorio_horas(colecao).gerar()
    elif x == 3:
        Relatorio_media_avaliacao(colecao).gerar()
    elif x == 4:
        Relatorio_percentual_status(colecao).gerar()
    elif x == 5:
        Relatorio_top5(colecao).gerar()
    else:
        print("Digite uma opção válida!")