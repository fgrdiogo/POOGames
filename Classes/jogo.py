import json
import unicodedata
from Classes.avaliacao import Avaliacao

class Jogo:
  VALID_STATUSES = {"NAO INICIADO", "NÃO INICIADO", "JOGANDO", "PAUSADO", "FINALIZADO", "ABANDONADO"}

  @classmethod
  def normalize_status(cls, s: str) -> str:
    if not isinstance(s, str):
      return s
    nf = unicodedata.normalize('NFKD', s)
    no_accent = ''.join(c for c in nf if not unicodedata.combining(c))
    cleaned = no_accent.replace('-', ' ').strip()
    cleaned = ' '.join(cleaned.split())
    return cleaned.upper()

  def __init__(self, titulo, genero, plataforma, status = "NAO INICIADO", horas = 0):
    self.titulo = titulo
    self.genero = genero
    self.plataforma = plataforma
    self._avaliacoes = []
    self.meta_anual = None
    self._allow_set_horas_direct = False
    self._horas = 0
    self.horas = horas
    self._status = "NAO INICIADO"
    self.status = status

  def to_dict(self):
    return {
      "titulo": self.titulo,
      "genero": self.genero,
      "plataforma": self.plataforma,
      "status": self.status,
      "horas": self.horas,
      "avaliacoes": [av.to_dict() for av in self._avaliacoes],
      "meta_anual": self.meta_anual
    }
  
  @classmethod
  def from_dict(cls, data):
    status = data.get("status", "NAO INICIADO")
    try:
      jogo = cls(
        data["titulo"],
        data["genero"],
        data["plataforma"],
        cls.normalize_status(status),
        data.get("horas", 0)
      )
    except KeyError:
      raise
    avals = data.get('avaliacoes') or []
    jogo._avaliacoes = [Avaliacao.from_dict(a, jogo_obj=jogo) for a in avals]
    jogo.meta_anual = data.get('meta_anual')
    return jogo

  @property
  def horas(self):
    return self._horas

  @horas.setter
  def horas(self, valor):
    if valor < 0:
      raise ValueError("As horas não podem ser negativas!")
    if not getattr(self, '_allow_set_horas_direct', False):
      if valor < getattr(self, '_horas', 0):
        raise ValueError("Não é permitido diminuir as horas jogadas!")
    self._horas = valor

  def _set_horas_internal(self, valor):
    self._allow_set_horas_direct = True
    try:
      self.horas = valor
    finally:
      self._allow_set_horas_direct = False

  @property
  def status(self):
    return self._status
  
  @status.setter
  def status(self, novo_status):
    if not isinstance(novo_status, str):
      raise ValueError("Status precisa ser uma string")
    ns = self.normalize_status(novo_status)
    if ns not in {self.normalize_status(s) for s in self.VALID_STATUSES}:
      raise ValueError(f"Status inválido: {novo_status}. Status válidos: {', '.join(sorted(self.VALID_STATUSES))}")
    if ns == "FINALIZADO" and self.horas < 1:
      raise ValueError("O status não pode ser alterado para FINALIZADO com menos de 1 hora!")
    self._status = ns
    
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
      
  def avaliar_jogo(self, avaliacao):
    if self.status == "FINALIZADO":
      self._avaliacoes.append(avaliacao)
      return "Avaliação registrada"
    else:
      raise ValueError("Jogo ainda não foi finalizado!")