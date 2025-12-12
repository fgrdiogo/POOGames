import unicodedata

class Colecao:
    def __init__(self):
        self.lista_de_jogos = []

    def adicionar_jogos(self, jogo_recebido):
        # Verifica se já existe usando o __eq__ do Jogo
        if jogo_recebido in self.lista_de_jogos:
            raise ValueError("Esse jogo já está na coleção!")
        
        self.lista_de_jogos.append(jogo_recebido)
        return True

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
        elif key == 'titulo':
            return sorted(self.lista_de_jogos, key=lambda j: j.titulo.lower(), reverse=reverse)
        elif key == 'media_avaliacao':
            def media(j):
                # Proteção caso _avaliacoes não exista ou esteja vazio
                if hasattr(j, '_avaliacoes') and j._avaliacoes:
                    return sum(av.nota for av in j._avaliacoes) / len(j._avaliacoes)
                return 0
            return sorted(self.lista_de_jogos, key=media, reverse=reverse)
        elif key == 'plataforma':
            return sorted(self.lista_de_jogos, key=lambda j: j.plataforma.lower(), reverse=reverse)
        elif key == 'genero':
            return sorted(self.lista_de_jogos, key=lambda j: j.genero.lower(), reverse=reverse)
        elif key == 'status':
            return sorted(self.lista_de_jogos, key=lambda j: j.status.lower(), reverse=reverse)
        return list(self.lista_de_jogos)