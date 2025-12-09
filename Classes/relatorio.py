import json
import unicodedata

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