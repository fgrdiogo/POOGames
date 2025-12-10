#--------------------------------------------------------------
# IMPORTAÇÕES
#--------------------------------------------------------------
import json
import os
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


#--------------------------------------------------------------
# MENU PRINCIPAL / INICIALIZAÇÃO DO SISTEMA
#--------------------------------------------------------------
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
        print("9 - EDITAR CONFIGURAÇÕES")
        print("10 - VERIFICAR ALERTAS")
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
            atualizar_horas(colecao); salvar(colecao)
        elif x == 8:
            atualizar_status(colecao); salvar(colecao)
        elif x == 9:
            configurar_usuario()
        elif x == 10:
            avisos(colecao)


#--------------------------------------------------------------
# FUNÇÕES - CADASTRO E INFORMAÇÕES DE JOGOS
#--------------------------------------------------------------
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


def mostrar_resumo(colecao):
    nome = input("Nome do jogo: ")
    for jogo in colecao.lista_de_jogos:
        if nome.lower() == jogo.titulo.lower():
            print(jogo); return
    print("Jogo não encontrado.")


#--------------------------------------------------------------
# FUNÇÕES DE AVALIAÇÃO
#--------------------------------------------------------------
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


#--------------------------------------------------------------
# FUNÇÕES DE ATUALIZAÇÃO (HORAS / STATUS)
#--------------------------------------------------------------
def atualizar_horas(colecao):
    """
    Localiza um jogo na coleção pelo título e (opcionalmente) plataforma.
    Se o jogo for encontrado chama a função responsável por atualizar as horas.
    """
    titulo = input("Título: ")
    plataforma = input("Plataforma (opcional): ")

    for jogo in colecao.lista_de_jogos:
        if jogo.titulo.lower() == titulo.lower() and \
           (not plataforma or jogo.plataforma.lower() == plataforma.lower()):
            #Jogo encontrado, então chama a função de atualizar as horas
            atualizar_horas_jogo(jogo)  
            return

    print("Jogo não encontrado.") 


def atualizar_horas_jogo(jogo):
    """
    Atualiza o total de horas jogadas no objeto passado como parâmetro.
    Não busca jogo, apenas modifica o que foi encontrado anteriormente.
    """
    try:
        horas = int(input("Adicionar horas: "))
        if horas < 0:
            print("Não é permitido diminuir horas.")
            return
        jogo.horas += horas
        print("Horas atualizadas com sucesso!")
    except ValueError:
        print("Entrada inválida. Digite um número.")


def atualizar_status(colecao):
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


#--------------------------------------------------------------
# SALVAR E CARREGAR ARQUIVOS JSON
#--------------------------------------------------------------
"""
Uso de caminhos relativos com base_dir e data_path para procurar arquivos .json na máquina do usuário
"""


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "..", "data", "colecao.json")

"""
Caso não seja encontrado um colecao.json, o mesmo é criado
"""

os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
if not os.path.exists(DATA_PATH):
    with open(DATA_PATH, "w") as f:
        json.dump([], f)


def salvar(colecao):
    dados = [jogo.to_dict() for jogo in colecao.lista_de_jogos]
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            lista = json.load(f)
    except FileNotFoundError:
        return []   # caso o json não exista ainda

    return [Jogo.from_dict(jogo) for jogo in lista]

#--------------------------------------------------------------
# EXIBIÇÃO DA COLEÇÃO
#--------------------------------------------------------------
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


#--------------------------------------------------------------
# RELATÓRIOS
#--------------------------------------------------------------
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


#--------------------------------------------------------------
# CONFIGURAÇÕES DO USUÁRIO (SETTINGS.JSON)
#--------------------------------------------------------------
"""
Caminho do arquivo settings.json no mesmo diretório /data/
"""
SETTINGS_PATH = os.path.join(BASE_DIR, "..", "data", "settings.json")

"""
Garante que exista a pasta e o arquivo de settings
"""
os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
if not os.path.exists(SETTINGS_PATH):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "meta_anual": 0,
            "plataforma_principal": None,
            "generos_favoritos": []
        }, f, indent=4, ensure_ascii=False)


def salvar_settings(settings):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)


def carregar_settings():
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "meta_anual": 0,
            "plataforma_principal": None,
            "generos_favoritos": []
        }

def configurar_usuario():
    settings = carregar_settings()

    while True:
        print("\n====== CONFIGURAÇÕES DO SISTEMA ======")
        print(f"1 - Definir meta anual de jogos finalizados (Atual: {settings['meta_anual']})")
        print(f"2 - Definir plataforma principal (Atual: {settings['plataforma_principal']})")
        print(f"3 - Adicionar gênero favorito")
        print(f"4 - Remover gênero favorito")
        print("5 - Ver configurações atuais")
        print("0 - Voltar ao menu principal")
        opc = input("Escolha: ")

        if opc == "0":
            salvar_settings(settings)
            print("Configurações salvas com sucesso.")
            break

        elif opc == "1":
            try:
                nova_meta = int(input("Nova meta anual: "))
                if nova_meta >= 0:
                    settings["meta_anual"] = nova_meta
                    print("Meta anual atualizada!")
                else:
                    print("A meta não pode ser negativa.")
            except:
                print("Digite um número válido.")

        elif opc == "2":
            plataforma = input("Digite a plataforma principal: ")
            settings["plataforma_principal"] = plataforma
            print("Plataforma principal definida!")

        elif opc == "3":
            genero = input("Adicionar gênero favorito: ")
            if genero not in settings["generos_favoritos"]:
                settings["generos_favoritos"].append(genero)
                print("Gênero adicionado!")
            else:
                print("Esse gênero já está na lista.")

        elif opc == "4":
            genero = input("Remover qual gênero? ")
            if genero in settings["generos_favoritos"]:
                settings["generos_favoritos"].remove(genero)
                print("Gênero removido.")
            else:
                print("Esse gênero não está na lista.")

        elif opc == "5":
            print("\nCONFIGURAÇÕES ATUAIS:")
            print(f"Meta anual: {settings['meta_anual']}")
            print(f"Plataforma principal: {settings['plataforma_principal']}")
            print(f"Gêneros favoritos: {', '.join(settings['generos_favoritos']) if settings['generos_favoritos'] else 'Nenhum'}")

        else:
            print("Opção inválida. Tente novamente.")


#--------------------------------------------------------------
# ALERTAS / AVISOS
#--------------------------------------------------------------
def avisos(colecao):
    """
    Nesse módulo o usuário poderá ver seus avisos e alertas, 
    """
    settings = carregar_settings()
    print("AVISOS E ALERTAS:")

    meta_atual = 0
    for jogo in colecao.lista_de_jogos:
        if jogo.status == "FINALIZADO":
            meta_atual += 1

    if meta_atual < settings['meta_anual']:
        print("A META ATUAL DE JOGOS É MENOR QUE A META ANUAL!")

    else:
        print("VOCÊ ULTRAPASSOU A META ANUAL PARABÉNS!")
    
    if not colecao.lista_de_jogos: 
        print("VOCÊ NÃO POSSUI AVISOS NEM JOGOS CADASTRADOS")
