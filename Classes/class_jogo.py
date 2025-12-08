class Jogo:
  def __init__(self, titulo, genero, plataforma, status = "NÃO INICIADO", horas = 0):
    self.titulo = titulo
    self.genero = genero
    self.plataforma = plataforma
    #os atributos status e horas(protegidos) receberão os valores que foram colocados no init
    self._status = status
    self._horas = horas 
    self._avaliacoes = []

  def to_dict(self):
    return {
      "titulo": self.titulo,
      "genero": self.genero,
      "plataforma": self.plataforma,
      "status": self.status,
      "horas": self.horas
    }
  
  #reconstruindo os objetos a partir de um arquivo
  @classmethod
  def from_dict(cls, data):
    jogo = cls(
    data["titulo"],
    data["genero"],
    data["plataforma"],
    data["status"],
    data["horas"]
    )
    return jogo

  
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
      
  #Não é necessário usar o parametro status, pois como já estamos na classe jogo, já podemos chamar self.status
  def avaliar_jogo(self, avaliacao):
    if self.status == "FINALIZADO":
      self._avaliacoes.append(avaliacao)
    else: 
      return "Jogo ainda não foi finalizado!"