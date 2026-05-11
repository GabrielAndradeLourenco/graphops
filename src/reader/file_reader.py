"""Leitura de grafo a partir de arquivo JSON."""

import json
import sys
import os

# adiciona o diretorio src ao path pra importar o core
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.graph import Graph


def ler_grafo_json(caminho_arquivo):
    """Le um arquivo JSON e devolve um objeto Graph."""
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    grafo = Graph()

    # adiciona os vertices com seus nomes
    for v in dados.get("vertices", []):
        grafo.adicionar_vertice(v["id"], v.get("nome"))

    # adiciona as arestas com pesos
    for a in dados.get("arestas", []):
        grafo.adicionar_aresta(a["origem"], a["destino"], a.get("peso", 1))

    return grafo
