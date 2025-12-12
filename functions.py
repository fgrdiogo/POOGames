#--------------------------------------------------------------
# IMPORTAÇÕES
#--------------------------------------------------------------
import dados
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
    
    colecao.lista_de_jogos = dados.carregar_jogos()

    while True:
        print("\n==== POOGAMES ====")
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
        
        try:
            # valida que o que será digitado pelo usuário é um inteiro
            x = int(input("ESCOLHA: "))
        except ValueError:
            print("Opção inválida. Digite um número.")
            continue

        if x == 0: 
            break
        elif x == 1:
            cadastrar_jogo(colecao)
            dados.salvar_jogos(colecao.lista_de_jogos)
        elif x == 2:
            mostrar_resumo(colecao)
        elif x == 3:
            avaliacao(colecao)
            dados.salvar_jogos(colecao.lista_de_jogos)
        elif x == 4:
            mostrar_colecao(colecao)
        elif x == 5:
            gerar_relatorio(colecao)
        elif x == 6:
            mostrar_colecao_filtrada(colecao)
        elif x == 7:
            atualizar_horas(colecao)
            dados.salvar_jogos(colecao.lista_de_jogos)
        elif x == 8:
            atualizar_status(colecao)
            dados.salvar_jogos(colecao.lista_de_jogos)
        elif x == 9:
            configurar_usuario()
        elif x == 10:
            avisos(colecao)
        else:
            print("Opção inexistente.")

#--------------------------------------------------------------
# FUNÇÕES - CADASTRO E INFORMAÇÕES DE JOGOS
#--------------------------------------------------------------
def cadastrar_jogo(colecao):
    print("==== Cadastro ====")
    titulo = input("Título: ").strip()
    if not titulo:
        print("Erro: O título é obrigatório.")
        return

    plataforma = input("Plataforma: ").strip()
    
    # verifica duplicidade usando o __eq__ da classe Jogo
    temp_jogo = Jogo(titulo, "Genérico", plataforma)
    if temp_jogo in colecao.lista_de_jogos:
        print("ERRO: Já existe um jogo com esse título e plataforma.")
        return

    genero = input("Gênero: ")
    status = input("Status (JOGANDO, FINALIZADO...): ")

    # validar a regra de mais de 3 jogos com status "jogando"
    if status.upper() == "JOGANDO":
        jogando_atuais = sum(1 for j in colecao.lista_de_jogos if j.status == "JOGANDO")
        if jogando_atuais >= 3:
            print("ERRO: Você já tem 3 jogos 'JOGANDO'. Finalize ou pause um antes.")
            return

    try:
        horas_input = input("Horas jogadas: ")
        horas = int(horas_input) if horas_input else 0
    except ValueError:
        print("Valor de horas inválido.")
        return

    try:
        # tenta criar o jogo (a classe jogo pelo encapsulamento que vai avaliar as regras)
        jogo = Jogo(titulo, genero, plataforma, status, horas)
        
        # adiciona na coleção
        colecao.adicionar_jogos(jogo)
        print("Jogo cadastrado com sucesso!")
        
    except ValueError as e:
        print(f"Erro ao cadastrar: {e}")


def mostrar_resumo(colecao):
    nome = input("Nome do jogo: ")
    encontrado = False
    for jogo in colecao.lista_de_jogos:
        if nome.lower() in jogo.titulo.lower():
            print(jogo)
            encontrado = True
    if not encontrado:
        print("Jogo não encontrado.")


#--------------------------------------------------------------
# FUNÇÕES DE AVALIAÇÃO
#--------------------------------------------------------------
def avaliacao(colecao): 
    if not colecao.lista_de_jogos:
        print("Nenhum jogo cadastrado.")
        return
    
    jogos_finalizados = False
    for jogo in colecao.lista_de_jogos:
        if jogo.status.upper() == "FINALIZADO":
            jogos_finalizados = True
    
    if jogos_finalizados == False:
        print("Não há jogos disponíveis para avaliação")
        return

    for jogo in colecao.lista_de_jogos:
        if jogo.status.upper() == "FINALIZADO":
            print(f"Jogo disponível para avaliação: {jogo.titulo}")

    titulo = input("Avaliar qual jogo? ")
    for jogo in colecao.lista_de_jogos:
        if jogo.titulo.lower() == titulo.lower():
            
            # validação rápida de status
            if jogo.status != "FINALIZADO":
                print("ERRO: O jogo precisa estar FINALIZADO para ser avaliado.")
                return

            try:
                nota = int(input("Nota (de 0 a 10): "))
                fav = input("Favorito? S/N ").upper() == "S"
                avali = Avaliacao(nota, jogo, fav)
                
                msg = jogo.avaliar_jogo(avali)
                if msg: print(msg)
                
            except ValueError as e:
                print(f"Erro: {e}")
            return
            
    print("Jogo não encontrado.")


#--------------------------------------------------------------
# FUNÇÕES DE ATUALIZAÇÃO (HORAS / STATUS)
#--------------------------------------------------------------
def atualizar_horas(colecao):
    titulo = input("Título: ")
    
    #procura o jogo na coleção para fazer a avaliação
    for jogo in colecao.lista_de_jogos:
        if jogo.titulo.lower() == titulo.lower():
            #se o jogo existir chama a função de atualizar as horas
            atualizar_horas_jogo(jogo)  
            return

    print("Jogo não encontrado.") 


def atualizar_horas_jogo(jogo):
    try:
        horas = int(input(f"Quantas horas adicionar ao jogo {jogo.titulo}? "))
        # a propriedade setter .horas na classe Jogo valida se é negativo/menor
        jogo.horas += horas
        print(f"Horas atualizadas! Total: {jogo.horas}h")
    except ValueError as e:
        print(f"Erro: {e}")


def atualizar_status(colecao):
    titulo = input("Título: ")
    novo_status = input("Novo status: ")

    for jogo in colecao.lista_de_jogos:
        if jogo.titulo.lower() == titulo.lower():
            try:
                # o setter .status na classe Jogo valida se o status existe
                jogo.status = novo_status
                print(f"Status atualizado para {jogo.status}.")
            except ValueError as e:
                print(f"Erro: {e}")
            return

    print("Jogo não encontrado.")


#--------------------------------------------------------------
# EXIBIÇÃO DA COLEÇÃO
#--------------------------------------------------------------
def mostrar_colecao(colecao):
    if not colecao.lista_de_jogos:
        print("Coleção vazia.")
        return
    
    print("-" * 30)
    for jogo in colecao.lista_de_jogos:
        print(f"Titulo: {jogo.titulo}")
        print(f"Gênero: {jogo.genero}")
        print(f"Plataforma: {jogo.plataforma}")
        print(f"Status: {jogo.status}")
        print(f"Horas: {jogo.horas}")
        
        # verifica se tem avaliações de forma segura
        if hasattr(jogo, '_avaliacoes') and jogo._avaliacoes:
            media = sum(a.nota for a in jogo._avaliacoes) / len(jogo._avaliacoes)
            print(f"Média Avaliações: {media:.2f}")
        else:
            print(f"Média Avaliações: N/A")
        print("-" * 30)


def mostrar_colecao_filtrada(colecao):
    print("Deixe em branco para ignorar o filtro.")
    genero = input("Gênero: ") or None
    status = input("Status: ") or None
    plataforma = input("Plataforma: ") or None

    resultados = colecao.filtrar(genero=genero, status=status, plataforma=plataforma)
    if not resultados:
        print("Nenhum jogo encontrado com esses filtros.")
        return

    print(f"\nEncontrados {len(resultados)} jogo(s):")
    for jogo in resultados:
        print(f"{jogo.titulo} | {jogo.plataforma} | {jogo.status} | {jogo.horas}h")


#--------------------------------------------------------------
# RELATÓRIOS
#--------------------------------------------------------------
def gerar_relatorio(colecao):
    print("\nQUAL TIPO DE RELATÓRIO VOCÊ DESEJA GERAR?")
    print("1-RELATÓRIO RESUMIDO")
    print("2-RELATORIO DE HORAS")
    print("3-RELATORIO MÉDIA DE AVALIAÇÕES")
    print("4-RELATORIO PERCENTUAL DE JOGOS POR STATUS")
    print("5-TOP 5 JOGOS MAIS JOGADOS")
    
    try:
        x = int(input("Digite a sua opção: "))
    except ValueError:
        print("Opção inválida.")
        return

    #opções de relatório filtrados
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
# CONFIGURAÇÕES DE USUÁRIO
#--------------------------------------------------------------
def configurar_usuario():
    # Usa o módulo dados para carregar
    settings = dados.carregar_settings()

    while True:
        print("\n====== CONFIGURAÇÕES DO SISTEMA ======")
        print(f"1 - Definir meta anual de jogos finalizados (Atual: {settings['meta_anual']})")
        print(f"2 - Definir plataforma principal (Atual: {settings['plataforma_principal']})")
        print(f"3 - Adicionar gênero favorito")
        print(f"4 - Remover gênero favorito")
        print("5 - Ver configurações atuais")
        print("0 - Voltar e Salvar")
        opc = input("Escolha: ")

        if opc == "0":
            # Usa o módulo dados para salvar
            dados.salvar_settings(settings)
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
            except ValueError:
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
            print("Opção inválida.")


#--------------------------------------------------------------
# ALERTAS / AVISOS
#--------------------------------------------------------------
def avisos(colecao):
    settings = dados.carregar_settings()
    meta_anual = settings.get('meta_anual', 0)

    print("\n==== AVISOS E ALERTAS ====")

    #Se a meta anual não tiver definida ou não houver jogos
    if meta_anual == 0:
        print("Nenhuma meta anual definida. Vá em 'Configurações' para definir uma.")
    else:
        meta_atual = 0
        for jogo in colecao.lista_de_jogos:
            if jogo.status == "FINALIZADO":
                meta_atual += 1

        if meta_atual < meta_anual:
            falta = meta_anual - meta_atual
            print(f"Você finalizou {meta_atual} jogos. Faltam {falta} para a meta de {meta_anual}!")
        else:
            print(f"✅ PARABÉNS! Você atingiu a meta anual ({meta_atual}/{meta_anual})!")
    #if not averigua se a lista_de_jogos é vazia, se ela for avisa que não há jogos
    if not colecao.lista_de_jogos: 
        print("DICA: Sua coleção está vazia. Cadastre alguns jogos!")