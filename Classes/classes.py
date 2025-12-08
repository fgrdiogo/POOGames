import json
import unicodedata

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
  
class Relatorio:
  def __init__(self, colecao):
    self.colecao = colecao

class Relatorio_resumido(Relatorio):
  def gerar(self):
    print("======Relatorio resumido=======")
    for jogo in self.colecao.lista_de_jogos:
      print(f"{jogo.titulo} - Status: {jogo.status}")
    print("=============")

class Relatorio_horas(Relatorio): 
    def gerar(self): 
      print("======Relatorio de horas=======")
      ordenado = sorted(self.colecao.lista_de_jogos, key=lambda j: j.horas, reverse=True)
      total_horas = 0
      for jogo in ordenado:
            print(f"{jogo.titulo}: {jogo.horas} horas")
            total_horas += jogo.horas
      print(f"Total de horas jogadas: {total_horas}")
      print("=============")

class Relatorio_media_avaliacao(Relatorio):
    def gerar(self):
        print("======Média de avaliações=======")

        avaliadas = []
        for jogo in self.colecao.lista_de_jogos:
            if jogo.status.upper() == "FINALIZADO" and jogo._avaliacoes:
                media = sum(av.nota for av in jogo._avaliacoes) / len(jogo._avaliacoes)
                avaliadas.append(media)

        if not avaliadas:
            print("Nenhum jogo finalizado com avaliação registrada.")
            return

        media_geral = sum(avaliadas) / len(avaliadas)
        print(f"Média geral das avaliações: {media_geral:.2f}")
        print("=============")

class Relatorio_percentual_status(Relatorio):
    def gerar(self):
        print("===== Percentual por status =====")

        total = len(self.colecao.lista_de_jogos)
        if total == 0:
            print("Nenhum jogo cadastrado.")
            return

        contagem = {}
        for jogo in self.colecao.lista_de_jogos:
            contagem[jogo.status] = contagem.get(jogo.status, 0) + 1

        for status, qtd in contagem.items():
            percentual = (qtd / total) * 100
            print(f"{status}: {percentual:.2f}% ({qtd} jogo(s))")

        print("=============")

class Relatorio_top5(Relatorio):
    def gerar(self):
        print("====== Top 5 mais jogados ======")

        if not self.colecao.lista_de_jogos:
            print("Nenhum jogo cadastrado.")
            return

        top = sorted(self.colecao.lista_de_jogos, key=lambda j: j.horas, reverse=True)[:5]

        for i, jogo in enumerate(top, start=1):
            print(f"{i}. {jogo.titulo} — {jogo.horas} horas")

        print("=============")

        
