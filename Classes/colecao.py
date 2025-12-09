import json
import unicodedata

class Colecao:
  def __init__(self):
    self.lista_de_jogos = []

  def adicionar_jogos(self, jogo_recebido):
    for jogo_existente in self.lista_de_jogos:
      if jogo_recebido == jogo_existente:
        return "Esse jogo já está na coleção!"
    self.lista_de_jogos.append(jogo_recebido)
    return "Jogo adicionado com sucesso!"
  
  def filtrar(self, genero=None, status=None, plataforma=None):
    resultado = self.lista_de_jogos
    if genero:
      resultado = [j for j in resultado if j.genero.lower() == genero.lower()]
    if status:
      s = status.strip().upper()
      resultado = [j for j in resultado if j.status.upper() == s]
    if plataforma:
      resultado = [j for j in resultado if j.plataforma.lower() == plataforma.lower()]
    return resultado

  def ordenar(self, key='horas', reverse=False):
    key = key.lower()
    if key == 'horas':
      return sorted(self.lista_de_jogos, key=lambda j: j.horas, reverse=reverse)
    if key == 'titulo':
      return sorted(self.lista_de_jogos, key=lambda j: j.titulo.lower(), reverse=reverse)
    if key == 'media_avaliacao':
      def media(j):
        if hasattr(j, '_avaliacoes') and j._avaliacoes:
          return sum(av.nota for av in j._avaliacoes) / len(j._avaliacoes)
        return 0
      return sorted(self.lista_de_jogos, key=media, reverse=reverse)
    if key == 'plataforma':
      return sorted(self.lista_de_jogos, key=lambda j: j.plataforma.lower(), reverse=reverse)
    if key == 'genero':
      return sorted(self.lista_de_jogos, key=lambda j: j.genero.lower(), reverse=reverse)
    if key == 'status':
      return sorted(self.lista_de_jogos, key=lambda j: j.status.lower(), reverse=reverse)
    return list(self.lista_de_jogos)