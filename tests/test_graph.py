"""Testes unitarios da classe Graph."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from core.graph import Graph


class TestGraph(unittest.TestCase):

    def test_adicionar_vertice(self):
        grafo = Graph()
        grafo.adicionar_vertice(0, "Gateway")
        self.assertIn(0, grafo.vertices())
        self.assertEqual(grafo.nome_do(0), "Gateway")

    def test_adicionar_aresta_cria_vertices(self):
        # se adicionar aresta com vertice que nao existe, ele cria
        grafo = Graph()
        grafo.adicionar_aresta(0, 1, peso=5)
        self.assertEqual(grafo.numero_vertices(), 2)
        self.assertEqual(grafo.numero_arestas(), 1)

    def test_vizinhos(self):
        grafo = Graph()
        grafo.adicionar_aresta(0, 1)
        grafo.adicionar_aresta(0, 2)
        vizinhos = grafo.vizinhos(0)
        self.assertIn(1, vizinhos)
        self.assertIn(2, vizinhos)


if __name__ == "__main__":
    unittest.main()
