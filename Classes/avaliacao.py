import json
import unicodedata

class Avaliacao:
  def __init__(self, nota, jogo, favoritado = False):
    if nota < 0 or nota > 10:
      raise ValueError("A nota precisa ser de 0 a 10!")
    self.nota = nota
    self.favoritado = favoritado
    self.jogo = jogo
  
  def to_dict(self):
    return {
      "nota": self.nota,
      "favoritado": bool(self.favoritado),
      "jogo_titulo": getattr(self.jogo, 'titulo', None),
      "jogo_plataforma": getattr(self.jogo, 'plataforma', None)
    }

  @classmethod
  def from_dict(cls, data, jogo_obj=None):
    nota = data.get('nota')
    favoritado = data.get('favoritado', False)
    return cls(nota, jogo_obj, favoritado)