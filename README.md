# Caatinga.AI — Sprint 1

Projeto da disciplina de Inteligência Artificial.

## Estado atual

Este é o primeiro estágio do projeto. Nesta etapa foram criadas a estrutura inicial do repositório, o gerador determinístico do pomar e a base da implementação das buscas.

As demais estratégias de busca e os outros módulos da atividade serão implementados nos próximos commits.

## Execução

```bash
python src/main.py 24114049
```

## Estrutura inicial

```text
src/
├── gerador_pomar.py
├── buscas.py
└── main.py
```


## Estado deste segundo commit

Nesta etapa foi adicionada a busca em profundidade (DFS), utilizando uma pilha
para controlar a fronteira. A BFS do commit anterior foi mantida para permitir
a comparação entre as duas estratégias. Ainda não foram implementadas UCS,
A* ou as métricas completas exigidas pela atividade.
