import json
import os
from Classes.jogo import Jogo

# ---------------------------------------------------------
# CONFIGURAÇÃO DE CAMINHOS
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

COLECAO_PATH = os.path.join(DATA_DIR, "colecao.json")
SETTINGS_PATH = os.path.join(DATA_DIR, "settings.json")

# ---------------------------------------------------------
# PERSISTÊNCIA DE JOGOS
# ---------------------------------------------------------
def salvar_jogos(lista_jogos):
    """Salva a lista de objetos Jogo em JSON."""
    dados = [jogo.to_dict() for jogo in lista_jogos]
    try:
        with open(COLECAO_PATH, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Erro ao salvar jogos: {e}")

def carregar_jogos():
    """Carrega o JSON e retorna lista de objetos Jogo."""
    if not os.path.exists(COLECAO_PATH):
        return []
    try:
        with open(COLECAO_PATH, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return [Jogo.from_dict(item) for item in dados]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# ---------------------------------------------------------
# PERSISTÊNCIA DE CONFIGURAÇÕES (CORRIGIDA)
# ---------------------------------------------------------
def salvar_settings(settings):
    """Salva o dicionário de configurações."""
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Erro ao salvar settings: {e}")

def carregar_settings():
    """
    Carrega as configurações. 
    Se o arquivo não existir ou estiver vazio, CRIA um novo com o padrão.
    """
    padrao = {
        "meta_anual": 0,
        "plataforma_principal": None,
        "generos_favoritos": []
    }
    
    # Se o arquivo não existe, cria-o imediatamente com o padrão
    if not os.path.exists(SETTINGS_PATH):
        salvar_settings(padrao)
        return padrao
        
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # Se o arquivo existe mas está vazio ou corrompido (o seu caso atual)
        print("Aviso: settings.json estava corrompido ou vazio. Restaurando padrão.")
        salvar_settings(padrao)
        return padrao