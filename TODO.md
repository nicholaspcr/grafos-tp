# TODO

Reference links
- https://networkx.org/
    - To check if the implementation is valid.


## Etapa 1

- [ ] Escolha do tema
- [ ] definição do problema
- [ ] levantamento de dados 
- [ ] modelagem do grafo.
    - A utiização de diagramas UML será avaliado na modelagem
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
