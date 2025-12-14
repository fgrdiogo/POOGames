from Classes.jogo import Jogo
from Classes.colecao import Colecao
import pytest

def test_finalizado():
    """
    Teste para verificar se é possível mudar o status de um  
    jogo com 0 horas para status = finalizado.
    Deve falhar pois a classe exige pelo menos 1 hora.
    """
    
    jogo1 = Jogo("TesteGame", "RPG", "pc", "NÃO INICIADO", horas=0)

    # Garante que horas é 0
    jogo1.horas = 0

    # Tentar mudar para FINALIZADO com 0 horas deve gerar ValueError
    with pytest.raises(ValueError): 
        jogo1.status = "FINALIZADO"

def test_status():
    """
    Teste para verificar se é possível adicionar mais de
    3 jogos na coleção (limite máximo)
    """
    colecao = Colecao()

    jogo1 = Jogo("TesteGame1", "RPG", "pc", "JOGANDO", horas=2)
    jogo2 = Jogo("TesteGame2", "RPG", "pc", "JOGANDO", horas=2)
    jogo3 = Jogo("TesteGame3", "RPG", "pc", "JOGANDO", horas=2)
    
    colecao.adicionar_jogos(jogo1)
    colecao.adicionar_jogos(jogo2)
    colecao.adicionar_jogos(jogo3)

    jogo4 = Jogo("TesteGame4", "RPG", "pc", "JOGANDO", horas=2)
    with pytest.raises(ValueError):
        colecao.adicionar_jogos(jogo4)

def test_duplicados():
    """
    Teste para verificar se não é possível
    adicionar jogos duplicados (mesmo titulo e plataforma)
    """

    colecao = Colecao()

    # Cria o primeiro jogo
    jogo1 = Jogo("TesteGame1", "RPG", "pc", "JOGANDO", horas=2)
    colecao.adicionar_jogos(jogo1)

    # Cria um segundo jogo com mesmo TITULO e PLATAFORMA (o que define igualdade na sua classe)
    jogo2 = Jogo("TesteGame1", "Aventura", "pc", "NÃO INICIADO", horas=0)
    
    with pytest.raises(ValueError):
        colecao.adicionar_jogos(jogo2)

def test_jogo_adicionado_sucesso():
    """
    Teste para verificar se os jogos estão
    sendo adicionados com sucesso a colecao
    """
    colecao = Colecao()

    jogo1 = Jogo("TesteGame1", "RPG", "pc", "JOGANDO", horas=2) 
    
    resultado = colecao.adicionar_jogos(jogo1)
    assert resultado == True
    assert len(colecao.lista_de_jogos) == 1

def test_horas_negativas():
    """
    Teste para verificar se o sistema impede
    a inserção de horas negativas
    """
    # Instancia com horas válidas
    jogo = Jogo("TesteGame", "RPG", "pc", "JOGANDO", horas=10)
    
    # Tenta setar negativo
    with pytest.raises(ValueError):
        jogo.horas = -5

def test_diminuir_horas_erro():
    """
    Teste específico para sua lógica que impede diminuir horas.
    Se o jogo tem 10 horas, não pode mudar para 5.
    """
    jogo = Jogo("TesteGame", "RPG", "pc", "JOGANDO", horas=10)
    
    with pytest.raises(ValueError):
        jogo.horas = 5

def test_status_invalido():
    """
    Teste para verificar se o sistema recusa
    um status que não esteja na lista VALID_STATUSES
    """
    jogo = Jogo("TesteGame", "RPG", "pc", "JOGANDO", horas=2)
    
    with pytest.raises(ValueError):
        jogo.status = "STATUS_QUE_NAO_EXISTE"

def test_atualizar_status_sucesso():
    """
    Teste para verificar a atualização de status
    para FINALIZADO quando as horas são válidas (>= 1)
    """
    # Cria jogo com 10 horas (requisito > 0 atendido)
    jogo = Jogo("TesteGame", "RPG", "pc", "JOGANDO", horas=10)
    
    # Ação permitida pois horas >= 1
    jogo.status = "FINALIZADO"
    
    assert jogo.status == "FINALIZADO"

def test_colecao_inicia_vazia():
    """
    Teste para verificar se uma nova coleção inicia
    sem nenhum jogo cadastrado (lista vazia)
    """
    colecao = Colecao()
    
    assert len(colecao.lista_de_jogos) == 0
    assert colecao.lista_de_jogos == []

def test_atributos_iniciais_jogo():
    """
    Teste simples para verificar se os atributos básicos
    do jogo são salvos corretamente usando os nomes da classe
    (titulo, genero, plataforma)
    """
    titulo_teste = "Zelda"
    genero_teste = "Aventura"
    plat_teste = "Switch"
    
    jogo = Jogo(titulo_teste, genero_teste, plat_teste, "NÃO INICIADO", horas=0)
    
    # Agora acessando .titulo (correto) em vez de .nome (errado)
    assert jogo.titulo == titulo_teste
    assert jogo.genero == genero_teste
    assert jogo.plataforma == plat_teste
    assert jogo.horas == 0