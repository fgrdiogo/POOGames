class Jogo:
  def __init__(self, titulo, genero, plataforma, status = "NÃO INICIADO", horas = 0):
    self.titulo = titulo
    self.genero = genero
    self.plataforma = plataforma
    #os atributos status e horas(protegidos) receberão os valores que foram colocados no init
    self._status = status
    self._horas = horas 
  
  @property
  def horas(self):
    return self._horas

  @horas.setter
  def horas(self, valor):
    if valor < 0: 
      raise ValueError("As horas não podem ser negativas!")
    else:
      self._horas = valor

  @property
  def status(self):
    return self._status
  
  @status.setter
  def status(self, novo_status):
    if novo_status == "FINALIZADO" and self.horas < 1: 
      raise ValueError("O status não pode ser alterado com menos de 1 hora!")
    else: 
      self._status = novo_status
    
  def __str__(self):
    return f"O jogo {self.titulo} do gênero {self.genero} na plataforma {self.plataforma}, tem status atual {self.status} e foi jogado por {self.horas} hora(s)"
  
  def __eq__(self, other):
    if isinstance(other, Jogo):
      if self.titulo == other.titulo and self.plataforma == other.plataforma:
        return True
      else:
        return False
    else:
      return False

class Jogo_PC(Jogo):
  pass
class Jogo_Console(Jogo):
  pass
class Jogo_Mobile(Jogo):
  pass


class  Usuario:
  """
  classe que envolve o utilizador do programa, aqui serão as informações principais do usuário
  """
  pass


class Colecao:
  def __init__(self):
    self.lista = []

  def adicionar_jogos(self, jogo_recebido):
    for jogo_existente in self.lista:
      if jogo_recebido == jogo_existente:
        return "Esse jogo já está na coleção!"
    self.lista.append(jogo_recebido)
    return "Jogo adicionado com sucesso!"
  

class Relatorio:
  """
  o relatorio receberá os atributos envolvidos com sua data de geração e qual filtro foi utilizado para criá-lo,
  estará relacionado com o método "gerar_relatorio()" na qual o usuario poderá criar um relatório com filtros personalizados
  """
  pass