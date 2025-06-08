# Ferramenta de Análise de Dependências para Projetos Go

Este repositório contém o código-fonte de uma ferramenta desenvolvida para analisar, visualizar e determinar a ordem de compilação de pacotes em projetos na linguagem Go, utilizando ordenação topológica.

## Requisitos

Para executar o código deste repositório, você precisa ter instalado em sua máquina:

1.  **Python 3** (versão 3.8 ou superior é recomendada).
2.  **pip** (geralmente já vem instalado com o Python).
3.  **Graphviz**: Esta é uma dependência do sistema e deve ser instalada antes dos pacotes Python. Você pode baixá-la no site oficial:
    * [https://graphviz.org/download/](https://graphviz.org/download/)

## Instalação

Para configurar o ambiente e instalar as dependências do projeto, siga os passos abaixo:

1.  **Clone o repositório** (caso ainda não tenha feito):
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DA_PASTA_DO_PROJETO>
    ```

2.  **Crie um ambiente virtual (virtual environment):**
    Isso isola as dependências do seu projeto do restante do sistema.
    ```bash
    python3 -m venv venv
    ```

3.  **Ative o ambiente virtual:**
    * **No Linux ou macOS:**
        ```bash
        source venv/bin/activate
        ```
    * **No Windows (PowerShell ou CMD):**
        ```bash
        .\venv\Scripts\activate
        ```
    O nome do ambiente virtual `(venv)` deverá aparecer no início do seu terminal.

4.  **Instale os pacotes Python:**
    ```bash
    pip install -r requirements.txt
    ```

## Execução

Com o ambiente virtual ativado, você pode executar a ferramenta da seguinte forma:

1.  **Execute o script principal:**
    ```bash
    python main.py
    ```

2.  **Informe o caminho do projeto Go:**
    O script solicitará que você insira o caminho para o diretório raiz de um projeto Go que você deseja analisar.
    ```
    Enter the root directory of the Go project: /caminho/para/seu/projeto-go
    ```

3.  **Visualize o resultado:**
    Após a análise, a ferramenta gerará um arquivo com o grafo de dependências (por exemplo, `dependency_graph.svg` ou `static_graph.html`) e, dependendo da implementação, poderá abri-lo automaticamente no seu navegador.
