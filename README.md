# POOGames 🎮  ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

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

## 🧠 Decisões de Design (Arquitetura)

O projeto foi estruturado seguindo princípios de **Desacoplamento** e **Coesão**:

1.  **Separação de Responsabilidades:**
    * **Domínio (`Classes/`):** As classes `Jogo`, `Colecao` e `Avaliacao` contêm apenas regras de negócio (ex: não permitir finalizar com < 1h). Elas não sabem como salvar arquivos.
    * **Persistência (`dados.py`):** Módulo dedicado exclusivamente a ler/escrever JSON. Este módulo foi criado com o intuito de dar ao projeto maior escalabilidade para futuras mudanças para um banco de dados mais sofisticado como SQL.
    * **Interface (`functions.py`):** Gerencia a interação com o usuário (CLI) e validações de entrada.

2.  **Uso de Herança:** Aplicada no sistema de Relatórios, onde uma classe base `Relatorio` define o contrato, e subclasses especializadas implementam a lógica específica de exibição.

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

```mermaid
classDiagram
    class Jogo {
        +str titulo
        +str status
        +int horas
        +avaliar_jogo()
    }
    class Colecao {
        +list lista_de_jogos
        +adicionar_jogos()
        +filtrar()
    }
    class Avaliacao {
        +int nota
        +bool favorito
    }
    class Relatorio {
        <<Abstract>>
        +gerar()
    }

    Colecao "1" o-- "*" Jogo : contem
    Jogo "1" *-- "*" Avaliacao : possui
    Relatorio <|-- Relatorio_resumido
    Relatorio <|-- Relatorio_top5
    Relatorio ..> Colecao : usa
   ```

---

## 🛠️ Como usar o projeto localmente

### Pré-requisitos

- Python 3 instalado  

## ​💻​ Como Executar

1. Clone este repositório:

   ```bash
   git clone https://github.com/fgrdiogo/POOGames.git
   ```

2. Entre na pasta do projeto

   ```bash
   cd POOGames
   ```
 
3. Execute o aplicativo
    ```bash
     python app.py
    ```

---

### 🧪 Testes Automatizados

Para garantir a confiabilidade do código e a integridade das regras de negócio (como a proibição de horas negativas ou mudanças de status inválidas), o projeto utiliza testes unitários com o framework pytest.

Atualmente, o sistema cobre 10 cenários críticos da classe Jogo, incluindo:

    ✅ Validação de status: Apenas status permitidos são aceitos.

    ✅ Regras de finalização: O jogo não pode ser "FINALIZADO" com 0 horas.

    ✅ Integridade de dados: Impedimento de inserção de horas negativas ou redução do tempo jogado.

    ✅ Unicidade: Prevenção de duplicidade de jogos na coleção.

    ✅ Limites: Verificação do comportamento da coleção ao atingir limites.

---

## ​💻​ Como rodar os testes

1. Instale o pytest (caso não tenha):

   ```bash
   pip install pytest
   ```

2. Na raiz do projeto execute: 

   ```bash
   pytest
   ```
 
O terminal exibirá o resultado dos testes (espera-se 10 passed)

---


## 📁 Estrutura do Projeto

```text
POOGames/
│  README.md
│  app.py           ← ponto de entrada principal
│  functions.py     ← lógica de interface e controle
|  dados.py         ← camada de persistência (JSON)
│
├─ Classes/
│    jogo.py
│    avaliacao.py
│    colecao.py
│    relatorio.py
│
└─ data/
|     colecao.json   ← arquivo de persistência (gerado automaticamente)
|     settings.json  ← criado no primeiro uso
│
└─ testes/           ← Testes Unitários
     __init__.py     ← define o pacote de testes
     test_jogo.py    ← bateria de testes da classe Jogo
```