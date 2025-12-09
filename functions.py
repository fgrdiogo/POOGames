import json
from Classes.jogo import Jogo
from Classes.avaliacao import Avaliacao
from Classes.colecao import Colecao
from Classes.relatorio import (
    Relatorio_resumido,
    Relatorio_horas,
    Relatorio_media_avaliacao,
    Relatorio_percentual_status,
    Relatorio_top5
)

def inicializar():
    colecao = Colecao()
    colecao.lista_de_jogos = carregar()

    while True:
        print("==== POOGAMES ====")
        print("0 - SAIR")
        print("1 - CADASTRAR JOGO")
        print("2 - MOSTRAR RESUMO DE UM JOGO")
        print("3 - AVALIAR JOGO")
        print("4 - MOSTRAR COLEÇÃO COMPLETA")
        print("5 - GERAR RELATÓRIOS")
        print("6 - FILTRAR COLEÇÃO")
        print("7 - ATUALIZAR HORAS JOGADAS")
        print("8 - ATUALIZAR STATUS")
        x = int(input("ESCOLHA: "))

        if x == 0: 
            break
        elif x == 1:
            cadastrar_jogo(colecao); salvar(colecao)
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
            atualizar_horas_cli(colecao); salvar(colecao)
        elif x == 8:
            atualizar_status_cli(colecao); salvar(colecao)

def cadastrar_jogo(colecao):
    print("==== Cadastro ====")
    titulo = input("Título: ")
    genero = input("Gênero: ")
    plataforma = input("Plataforma: ")
    status = input("Status: ")

    if status == "JOGANDO":
        jogando_atuais = 0
        for jogo in colecao.lista_de_jogos:
            if jogo.status == "JOGANDO":
                jogando_atuais += 1
        if jogando_atuais >= 3:
            raise ValueError("NÃO É POSSÍVEL CADASTRAR MAIS DE 3 JOGOS COM STATUS JOGANDO")

    try:
        horas = int(input("Horas jogadas: "))
    except ValueError:
        print("Valor inválido.")
        return

    try:
        jogo = Jogo(titulo, genero, plataforma, status, horas)
    except ValueError as e:
        print(f"Erro: {e}")
        return

    print(colecao.adicionar_jogos(jogo))

def atualizar_horas(jogo):
    try:
        horas = int(input("Adicionar horas: "))
        if horas < 0:
            print("Não pode subtrair horas.")
            return
        jogo.horas += horas
    except:
        print("Entrada inválida.")

def mostrar_resumo(colecao):
    nome = input("Nome do jogo: ")
    for jogo in colecao.lista_de_jogos:
        if nome.lower() == jogo.titulo.lower():
            print(jogo); return
    print("Jogo não encontrado.")

def avaliacao(colecao): 
    if not colecao.lista_de_jogos:
        print("Nenhum jogo cadastrado.")
        return
    
    titulo = input("Avaliar qual jogo? ")

    for jogo in colecao.lista_de_jogos:
        if jogo.titulo.lower() == titulo.lower():
            if jogo.status != "FINALIZADO":
                raise ValueError("PARA AVALIAR UM JOGO É NECESSÁRIO QUE ELE ESTEJA FINALIZADO")
            else:
                try:
                    nota = int(input("Nota (de 0 a 10): "))
                    fav = input("Favorito? S/N ").upper() == "S"
                    avali = Avaliacao(nota, jogo, fav)
                    resultado = jogo.avaliar_jogo(avali)
                    if resultado: print(resultado)
                except ValueError as e:
                    print(f"Erro: {e}")
                return
    print("Jogo não encontrado.")

def atualizar_horas_cli(colecao):
    titulo = input("Título: ")
    plataforma = input("Plataforma (opcional): ")

    for jogo in colecao.lista_de_jogos:
        if jogo.titulo.lower() == titulo.lower() and (not plataforma or jogo.plataforma.lower() == plataforma.lower()):
            atualizar_horas(jogo); return
            
    print("Jogo não encontrado.")

def atualizar_status_cli(colecao):
    titulo = input("Título: ")
    plataforma = input("Plataforma (opcional): ")
    novo_status = input("Novo status: ")

    for jogo in colecao.lista_de_jogos:
        if jogo.titulo.lower() == titulo.lower() and (not plataforma or jogo.plataforma.lower() == plataforma.lower()):
            try:
                jogo.status = novo_status
                print("Status atualizado.")
            except ValueError as e:
                print(f"Erro: {e}")
            return

    print("Jogo não encontrado.")

def salvar(colecao):
    dados = [jogo.to_dict() for jogo in colecao.lista_de_jogos]
    with open("/home/diogo/POO/data/colecao.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar():
    try:
        with open("/home/diogo/POO/data/colecao.json", "r") as f:
            return [Jogo.from_dict(j) for j in json.load(f)]
    except:
        return []

def mostrar_colecao(colecao):
    if not colecao.lista_de_jogos:
        print("Coleção vazia."); return
    
    for jogo in colecao.lista_de_jogos:
        print(f"Titulo: {jogo.titulo}")
        print(f"Gênero: {jogo.genero}")
        print(f"Plataforma: {jogo.plataforma}")
        print(f"Status: {jogo.status}")
        print(f"Horas: {jogo.horas}")
        if jogo._avaliacoes:
            media = sum(a.nota for a in jogo._avaliacoes) / len(jogo._avaliacoes)
            print(f"Média Avaliações: {media:.2f}")
        else:
            print(f"Média Avaliações: N/A")
        print("---------------")

def mostrar_colecao_filtrada(colecao):
    genero = input("Gênero: ") or None
    status = input("Status: ") or None
    plataforma = input("Plataforma: ") or None

    resultados = colecao.filtrar(genero=genero, status=status, plataforma=plataforma)
    if not resultados:
        print("Nenhum jogo encontrado."); return

    for jogo in resultados:
        print(f"{jogo.titulo} | {jogo.plataforma} | {jogo.status} | {jogo.horas}h")

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
