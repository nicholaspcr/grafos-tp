# TP

Reference links
- https://networkx.org/
    - To check if the implementation is valid.

## Requirements

To run the code in this repository you need to have installed in your machine the following:

1. Python3
2. pip

## Install

You should have [graphviz](https://graphviz.org/download/) installed in your system.

Additionally you should do the following:

1. `python3 -m venv venv`
2. `source venv/bin/activate`
    - Ensure that the python version of pip is the same as the python being used.
3. `pip install -r requirements.txt`


# Remove later
## TODO

Até dia 30 fazer:
- [ ] Implementar Kahn algorithm
- [ ] Implementar visualização com graphiz
- [ ] Template de relatório Latex no repositório

## Etapa 1

- [x] Escolha do tema
- [x] definição do problema
- [x] levantamento de dados 
- [ ] modelagem do grafo.
    - A utiização de diagramas UML será avaliado na modelagem!
    - Professor é de Engenharia de Software, foco nos diagramas

## Etapa 2

- [ ] Implementação da estrutura de grafos
- [ ] Aplicação dos algoritmos e construção de uma interface mínima de uso. 
- [ ] Apresente uma interface gráfica com os resultados.
    - Visualização das dependências.
    - Talvez colorir dependências externas em uma cor distinta das dependências dentro do repositório.

## Etapa 3

- [ ] Contextualização, modelagem, análise dos resultados obtidos 
- [ ] avaliação do desempenho,
- [ ] conclusões e apresentação da solução.

Entregáveis: Relatório técnico em LATEX usando o template oficial da SBC (obrigatório);
apresentação oral com demonstração da ferramenta; repositório Git contendo o histórico
de desenvolvimento (commits individuais serão avaliados)


## Ideia

A ideia é utilizar do tema 9:

> Gestão de Conflitos em Sistemas de Dependência: modelagem de dependências entre tarefas ou pacotes com detecção de
> ciclos, visualização de dependências e execução segura baseada em ordenação topológica.

Onde o objetivo é analisar as dependências internas e externas de repositórios escritos em golang, tais como:
- https://github.com/nicholaspcr/gode
- https://github.com/cli/cli
- https://github.com/TheThingsNetwork/lorawan-stack

Deve-se conferir se existe ciclo e caso não exista, precisamos gerar a ordem topológica das dependências.
