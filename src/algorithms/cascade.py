"""Simulacao de falha em cascata usando BFS."""

from collections import deque


def bfs_a_partir_de(grafo, origem, removido=None):
    """
    Faz uma BFS a partir da origem ignorando o vertice removido.
    Retorna o conjunto de vertices alcancaveis.
    Complexidade: O(V + E).
    """
    if origem == removido or origem not in grafo.vertices():
        return set()

    visitados = {origem}
    fila = deque([origem])

    while fila:
        atual = fila.popleft()
        for vizinho in grafo.vizinhos(atual):
            if vizinho == removido:
                continue
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)

    return visitados


def simular_falha(grafo, origem, vertice_removido):
    """
    Simula a queda de um servico e retorna os impactos.
    Retorna dict com: alcancaveis, afetados, percentual.
    """
    todos = set(grafo.vertices()) - {vertice_removido}
    alcancaveis = bfs_a_partir_de(grafo, origem, vertice_removido)
    afetados = todos - alcancaveis

    total = len(todos) if len(todos) > 0 else 1
    percentual = (len(afetados) / total) * 100

    return {
        "removido": grafo.nome_do(vertice_removido),
        "alcancaveis": [grafo.nome_do(v) for v in alcancaveis],
        "afetados": [grafo.nome_do(v) for v in afetados],
        "percentual_impacto": round(percentual, 2),
    }
