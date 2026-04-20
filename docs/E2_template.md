# E2 — Design Técnico, Arquitetura e Backlog

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 13 de abril de 2026  
> **Peso:** 20% da nota final  

---

## Identificação do Grupo

| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | GraphOps |
| Repositório GitHub | https://github.com/GabrielAndradeLourenco/graphops |
| Integrante 1 | Fernando Januário — RA 38772752 |
| Integrante 2 | Gabriel Andrade — RA 38332167 |

---

## 1. Algoritmos Escolhidos

### 1.1 Algoritmo Principal

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | Betweenness Centrality (Centralidade de Intermediação) |
| Categoria | Busca (baseado em caminhos mínimos via BFS) |
| Complexidade de tempo | O(V · E) |
| Complexidade de espaço | O(V + E) |
| Problema que resolve | Identificar quais microsserviços são pontos críticos (SPOFs) na malha, medindo quantos caminhos mínimos entre pares de serviços passam por cada vértice |

**Por que este algoritmo foi escolhido?**

A gente pensou primeiro em usar PageRank ou degree centrality pra achar os serviços mais importantes, mas percebemos que ter muitas conexões não significa necessariamente ser crítico. Um serviço de logging, por exemplo, recebe chamadas de todo mundo mas se ele cair não derruba nenhum fluxo de negócio. O que realmente importa é se o serviço fica "no meio do caminho" entre outros — e é isso que o Betweenness Centrality mede. Ele calcula quantos caminhos mínimos passam por cada vértice, então um Auth Service que aparece no meio de vários fluxos vai ter um valor alto, indicando que é um SPOF de verdade.

**Alternativa descartada e motivo:**

| Algoritmo alternativo | Motivo da exclusão |
|----------------------|-------------------|
| PageRank | Foi a primeira opção que consideramos, mas ele mede importância por quantidade de links de entrada, o que funciona bem pra páginas web mas não tanto pra microsserviços. Um serviço de logging tem in-degree altíssimo (todo mundo manda log pra ele) mas se cair não quebra nenhum fluxo. Não faz sentido classificar ele como crítico. |

**Limitações no contexto do problema:**

- O algoritmo parte do princípio que a comunicação entre serviços segue caminhos mínimos, o que nem sempre é verdade — em ambientes com load balancers ou circuit breakers o tráfego pode ir por rotas diferentes. Além disso, se o grafo ficar muito grande (tipo milhares de serviços), O(V·E) pode ficar pesado e talvez precise de alguma estratégia de amostragem.

**Referência bibliográfica:**

> CORMEN, T. H. et al. Algoritmos: teoria e prática. 3. ed. Rio de Janeiro: Elsevier, 2012. Cap. 22-24 (BFS e caminhos mínimos).

---

### 1.2 Algoritmo Adicional

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | BFS (Busca em Largura) para Simulação de Falha em Cascata |
| Categoria | Busca |
| Complexidade de tempo | O(V + E) |
| Complexidade de espaço | O(V) |

**Justificativa:**

A BFS serve pra gente simular o que acontece quando um serviço cai. A ideia é: removemos um vértice do grafo (ex: o Auth) e rodamos uma BFS a partir do Gateway pra ver quais serviços ainda são alcançáveis. Os que ficarem fora da busca são os serviços que seriam afetados pela falha. A métrica que usamos é simples: quantidade de vértices que ficam inalcançáveis dividido pelo total de vértices, dando um percentual de impacto. Assim conseguimos responder "se tal serviço cair, X% da malha é afetada".

**Referência bibliográfica:**

> SEDGEWICK, R.; WAYNE, K. Algorithms. 4. ed. Boston: Addison-Wesley, 2011. Cap. 4.1 (Grafos não-dirigidos e BFS).

---

## 2. Arquitetura em Camadas

> Diagrama em texto (a versão visual vai em `./docs/arquitetura_e2.png`):

```
┌─────────────────────────────────────────────────┐
│              APRESENTAÇÃO (CLI)                  │
│  main.py — interface de linha de comando         │
│  Exibe resultados, recebe parâmetros do usuário  │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│            APLICAÇÃO (Service)                   │
│  analysis_service.py — orquestra os fluxos:      │
│  carregar grafo → executar algoritmo → formatar  │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│              DOMÍNIO (Core)                      │
│  graph.py — estrutura do grafo (lista adjacência)│
│  betweenness.py — Betweenness Centrality         │
│  cascade.py — simulação de falha via BFS         │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│          INFRAESTRUTURA (I/O)                    │
│  file_reader.py — leitura de JSON                │
│  file_writer.py — exportação de resultados       │
│  graph_generator.py — geração aleatória          │
└─────────────────────────────────────────────────┘
```

![Diagrama de arquitetura](./docs/arquitetura_e2.png)

### Descrição das camadas

| Camada | Responsabilidade | Artefatos principais |
|--------|-----------------|----------------------|
| Apresentação (CLI) | Recebe os comandos do usuário (qual arquivo carregar, qual algoritmo rodar, qual vértice remover) e mostra os resultados no terminal | `main.py` |
| Aplicação (Service) | Faz a ponte entre as camadas: pega o grafo do I/O, manda pro Core processar e devolve o resultado formatado pra CLI | `analysis_service.py` |
| Domínio (Core) | Onde fica a estrutura do grafo (lista de adjacência dirigida e ponderada) e os algoritmos (Betweenness e BFS de cascata) | `graph.py`, `betweenness.py`, `cascade.py` |
| Infraestrutura (I/O) | Leitura do JSON de entrada, gravação dos resultados e geração de grafos aleatórios pra teste | `file_reader.py`, `file_writer.py`, `graph_generator.py` |

---

## 3. Estrutura de Diretórios

```
graphops/
├── docs/
│   ├── E1_template.md
│   ├── E2_template.md
│   └── arquitetura_e2.png
├── src/
│   ├── core/
│   │   ├── graph.py              # Estrutura do grafo dirigido ponderado (lista de adjacência)
│   │   ├── betweenness.py        # Betweenness Centrality
│   │   └── cascade.py            # Simulação de falha em cascata (BFS)
│   ├── services/
│   │   └── analysis_service.py   # Orquestração dos fluxos de análise
│   ├── io/
│   │   ├── file_reader.py        # Parser de JSON de entrada
│   │   ├── file_writer.py        # Exportação de resultados
│   │   └── graph_generator.py    # Geração aleatória de grafos
│   └── main.py                   # Ponto de entrada CLI
├── tests/
│   ├── test_graph.py
│   ├── test_betweenness.py
│   └── test_cascade.py
├── data/
│   └── exemplo_microsservicos.json
└── requirements.txt
```

> **Justificativa de desvios**: a gente adicionou a pasta `services/` pra separar melhor a camada de aplicação da camada de domínio. O template sugere tudo direto em `src/`, mas achamos que separar em `core/`, `services/` e `io/` deixa mais claro onde cada coisa fica e bate com a arquitetura em camadas.

---

## 4. Definição do Dataset

**Formato de entrada aceito:**

JSON — a gente escolheu JSON porque é fácil de ler e de parsear em Python (já tem o módulo `json` nativo). Dá pra representar o grafo dirigido ponderado sem problema. No E1 tínhamos mencionado usar logs de rastreamento e manifestos de infraestrutura como entrada, mas pensando melhor decidimos simplificar e usar só arquivo JSON com a topologia já definida. Tentar parsear duas fontes diferentes ia dar muito trabalho de implementação sem agregar muito pro lado dos algoritmos de grafos.

**Exemplo de estrutura do arquivo de entrada:**

```json
{
  "vertices": [
    { "id": 0, "nome": "Gateway" },
    { "id": 1, "nome": "Auth" },
    { "id": 2, "nome": "Payment" },
    { "id": 3, "nome": "Inventory" },
    { "id": 4, "nome": "Notification" },
    { "id": 5, "nome": "Logging" }
  ],
  "arestas": [
    { "origem": 0, "destino": 1, "peso": 12 },
    { "origem": 0, "destino": 2, "peso": 8 },
    { "origem": 2, "destino": 1, "peso": 15 },
    { "origem": 1, "destino": 3, "peso": 20 },
    { "origem": 3, "destino": 4, "peso": 5 },
    { "origem": 2, "destino": 4, "peso": 10 },
    { "origem": 0, "destino": 5, "peso": 3 },
    { "origem": 1, "destino": 5, "peso": 2 },
    { "origem": 2, "destino": 5, "peso": 4 }
  ]
}
```

> Os pesos representam latência média em milissegundos entre os serviços (ex: Gateway → Auth: 12ms). No E1 o diagrama não mostrava pesos apesar de termos declarado grafo ponderado, então aqui já deixamos os valores definidos.

**Estratégia de geração aleatória:**

| Parâmetro | Descrição |
|-----------|-----------|
| Número de vértices | Configurável via argumento CLI (padrão: 10) |
| Densidade | Configurável de 0.0 a 1.0 (padrão: 0.3, que é mais ou menos a esparsidade que a gente espera numa malha de microsserviços) |
| Faixa de pesos | Mín: 1ms, Máx: 100ms (configuráveis) |

---

## 5. Backlog do Projeto

### 5.1 In-Scope — O que será implementado

| # | Funcionalidade | Prioridade | Critério de aceite |
|---|---------------|------------|-------------------|
| 1 | Leitura e construção do grafo a partir de JSON | Alta | Dado um arquivo JSON com 6 vértices e 9 arestas ponderadas, quando o sistema carregar o arquivo, então o grafo em memória contém exatamente 6 vértices e 9 arestas com os pesos corretos |
| 2 | Cálculo de Betweenness Centrality | Alta | Dado um grafo com 10 vértices e 15 arestas, quando o usuário executar o cálculo de centralidade, então o sistema exibe o ranking de vértices ordenado por betweenness decrescente, identificando o(s) SPOF(s) |
| 3 | Simulação de falha em cascata via BFS | Alta | Dado um grafo com 10 vértices e vértice de origem 0 (Gateway), quando o usuário remover o vértice 1 (Auth), então o sistema exibe a lista de vértices inalcançáveis a partir do Gateway e o percentual de serviços afetados |
| 4 | Geração de grafos aleatórios | Média | Dado os parâmetros V=20, densidade=0.3 e pesos entre 1 e 100, quando o usuário executar a geração, então o sistema cria um arquivo JSON válido com um grafo dirigido ponderado respeitando os parâmetros |
| 5 | Exportação de resultados em JSON | Média | Dado a execução de qualquer análise, quando o usuário solicitar exportação, então o sistema grava um arquivo JSON com os resultados (ranking de centralidade ou lista de impacto) |
| 6 | Exibição formatada dos resultados no terminal | Baixa | Dado a execução de uma análise, quando o resultado for exibido, então o terminal mostra uma tabela legível com nomes dos serviços, valores de centralidade e indicadores de SPOF |

### 5.2 Out-of-Scope — O que NÃO será feito

| Funcionalidade excluída | Motivo |
|------------------------|--------|
| Interface gráfica (GUI/Web) | Não vai dar tempo e também foge do escopo da disciplina. A CLI já resolve pra mostrar os resultados |
| Coleta automática de dados de infraestrutura real (logs, Kubernetes, AWS) | Ia precisar de parsers diferentes pra cada fonte e não agrega valor pro lado de grafos. Melhor focar nos algoritmos e usar JSON estático como entrada |
| Atuação automática na infraestrutura (reiniciar serviços, redirecionar tráfego) | O GraphOps é ferramenta de análise, não de orquestração. Mexer em infra real ia precisar de integração com APIs de cloud e foge completamente do escopo |

---

## Checklist de Entrega

- [x] Big-O de tempo e espaço declarados para cada algoritmo
- [x] Ao menos 1 alternativa descartada com justificativa
- [x] Diagrama de arquitetura com 4 camadas identificadas
- [x] Referência bibliográfica para cada algoritmo (ABNT ou IEEE)
- [x] Backlog com ≥ 5 itens In-Scope e ≥ 3 Out-of-Scope
- [x] Ao menos 3 critérios de aceite no formato "dado / quando / então"
- [x] Exemplo de estrutura de arquivo de entrada presente

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*
