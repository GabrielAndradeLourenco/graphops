"""Calculo de Betweenness Centrality usando BFS (algoritmo de Brandes)."""

from collections import deque


def calcular_betweenness(grafo):
    """
    Retorna um dicionario {vertice: valor_betweenness}.
    Complexidade: O(V * E) em tempo e O(V + E) em espaco.
    """
    betweenness = {v: 0.0 for v in grafo.vertices()}

    # para cada vertice, faz uma BFS e acumula os valores
    for s in grafo.vertices():
        # estrutura do Brandes
        pilha = []
        predecessores = {v: [] for v in grafo.vertices()}
        sigma = {v: 0 for v in grafo.vertices()}  # quantidade de caminhos minimos
        sigma[s] = 1
        distancia = {v: -1 for v in grafo.vertices()}
        distancia[s] = 0

        fila = deque([s])
        while fila:
            v = fila.popleft()
            pilha.append(v)
            for w in grafo.vizinhos(v):
                # primeira vez visitando w
                if distancia[w] < 0:
                    fila.append(w)
                    distancia[w] = distancia[v] + 1
                # se o caminho minimo passa por v
                if distancia[w] == distancia[v] + 1:
                    sigma[w] += sigma[v]
                    predecessores[w].append(v)

        # acumulo de dependencias
        delta = {v: 0.0 for v in grafo.vertices()}
        while pilha:
            w = pilha.pop()
            for v in predecessores[w]:
                if sigma[w] > 0:
                    delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != s:
                betweenness[w] += delta[w]

    return betweenness


def ranking_spofs(grafo):
    """Retorna lista ordenada de (nome, valor) por betweenness decrescente."""
    valores = calcular_betweenness(grafo)
    ordenado = sorted(valores.items(), key=lambda x: x[1], reverse=True)
    return [(grafo.nome_do(v), valor) for v, valor in ordenado]
