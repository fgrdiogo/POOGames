# POOGames 🎮  
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📄 Sobre o Projeto

POOGames é um sistema em Python para organizar sua coleção de jogos, permitir cadastro, marcação de horas jogadas, avaliação, e gerar relatórios personalizados. O objetivo é aplicar conceitos de Programação Orientada a Objetos (POO), persistência de dados com JSON e uso de herança/composição para manter o código modular, educacional e organizado.

Você pode usar o programa direto pelo terminal (CLI), registrar seus jogos, adicionar horas, avaliar, consultar resumos, filtrar sua coleção e exportar dados em JSON para manter os registros persistentes.

---

## 🚀 Funcionalidades principais

- 📥 Cadastro de jogos (título, gênero, plataforma, status, horas)  
- 📝 Avaliação dos jogos (nota de 0 a 10, marcar como favorito) — apenas se o jogo estiver finalizado  
- 🧮 Métodos de POO: encapsulamento, getters/setters, `__eq__`, `__str__`  
- 💾 Persistência de dados com JSON — carregamento e salvamento automáticos da coleção  
- 📊 Relatórios com herança:  
  - Relatório resumido (título + status)  
  - Relatório de horas jogadas (ranking + total)  
  - Média de avaliação dos jogos finalizados  
  - Percentual de jogos por status  
  - Top 5 jogos mais jogados  
- 🔍 Filtragem da coleção por gênero, plataforma ou status  
- 📂 Modularização: cada classe em seu próprio módulo, separando lógica e trazendo organização  

---

## 🏗️ Estrutura de Classes e Relações  

| Classe / Módulo           | Responsabilidade / Relação                             |
|--------------------------|--------------------------------------------------------|
| **Jogo**                 | Representa um jogo — atributos: título, gênero, plataforma, status, horas, avaliações; métodos de negócio (`horas`, `status`, `avaliar_jogo()`, `__eq__`, `__str__`) |
| **Avaliacao**            | Representa uma avaliação de um jogo — nota, favorito, referência ao jogo |
| **Colecao**              | Agrega objetos `Jogo`; serve como “biblioteca” do usuário, armazenamento da lista de jogos |
| **Relatorio (base)**     | Classe abstrata que recebe uma `Colecao` e define interface para gerar relatórios |
| **Relatorio_resumido / Relatorio_horas / Relatorio_media_avaliacao / Relatorio_percentual_status / Relatorio_top5** | Subclasses de `Relatorio`, cada uma implementando um tipo de relatório específico |
| **functions.py (controle)** | Interface de linha de comando — lê entradas do usuário, interage com `Colecao`, salva e carrega JSON, invoca relatórios, etc. |

---

## 🛠️ Como usar o projeto localmente

### Pré-requisitos

- Python 3 instalado  
- (Opcional) Criar um diretório `data/` na raiz para armazenar o JSON  

---

## 🚀 Passos para execução:
  #1. Clone o repositório
  git clone https://github.com/fgrdiogo/POOGames.git

  #2. Entre na pasta do projeto
  cd POOGames

  #3. Execute o aplicativo
  python app.py


## 📁 Estrutura do Projeto

```text
POOGames/
│  README.md
│  app.py
│  functions.py
│
├─ Classes/
│    jogo.py
│    avaliacao.py
│    colecao.py
│    relatorio.py
│
└─ data/
     colecao.json   ← arquivo de persistência (gerado automaticamente)
     settings.json  ← criado no primeiro uso



