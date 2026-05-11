"""Testes unitarios do Betweenness Centrality."""

import unittest
import sys
import os

# adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from core.graph import Graph
from algorithms.betweenness import calcular_betweenness


class TestBetweenness(unittest.TestCase):

    def test_caso_base(self):
        # grafo simples em linha: 0 -> 1 -> 2
        # o vertice 1 deve ter betweenness maior que 0 (intermedia 0 e 2)
        grafo = Graph()
        grafo.adicionar_aresta(0, 1)
        grafo.adicionar_aresta(1, 2)

        resultado = calcular_betweenness(grafo)

        # o vertice do meio tem que ser o mais central
        self.assertGreater(resultado[1], resultado[0])
        self.assertGreater(resultado[1], resultado[2])

    def test_grafo_vazio(self):
        # grafo sem vertices nem arestas
        grafo = Graph()
        resultado = calcular_betweenness(grafo)

        # tem que devolver dicionario vazio
        self.assertEqual(resultado, {})

    def test_grafo_completo(self):
        # grafo com todos conectados: nenhum vertice intermedia nada
        grafo = Graph()
        for i in range(4):
            grafo.adicionar_vertice(i)
        # liga todo mundo com todo mundo
        for i in range(4):
            for j in range(4):
                if i != j:
                    grafo.adicionar_aresta(i, j)

        resultado = calcular_betweenness(grafo)

        # como todos tem ligacao direta, ninguem precisa de intermediario
        for valor in resultado.values():
            self.assertEqual(valor, 0.0)


if __name__ == "__main__":
    unittest.main()
