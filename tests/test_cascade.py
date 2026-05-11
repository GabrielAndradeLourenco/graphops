"""Testes unitarios da simulacao de falha em cascata."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from core.graph import Graph
from algorithms.cascade import simular_falha, bfs_a_partir_de


class TestCascade(unittest.TestCase):

    def test_caso_base(self):
        # 0 -> 1 -> 2, se tirar o 1 o 2 fica inalcancavel
        grafo = Graph()
        grafo.adicionar_aresta(0, 1)
        grafo.adicionar_aresta(1, 2)

        resultado = simular_falha(grafo, origem=0, vertice_removido=1)

        # o vertice 2 tem que estar na lista de afetados
        self.assertIn("2", resultado["afetados"])
        # impacto deve ser maior que 0
        self.assertGreater(resultado["percentual_impacto"], 0)

    def test_grafo_vazio(self):
        # grafo sem vertices - nao deve dar erro
        grafo = Graph()
        alcancaveis = bfs_a_partir_de(grafo, origem=0)

        # conjunto vazio
        self.assertEqual(alcancaveis, set())

    def test_grafo_completo(self):
        # grafo completo: mesmo tirando um vertice, os outros se alcancam
        grafo = Graph()
        for i in range(4):
            grafo.adicionar_vertice(i)
        for i in range(4):
            for j in range(4):
                if i != j:
                    grafo.adicionar_aresta(i, j)

        resultado = simular_falha(grafo, origem=0, vertice_removido=2)

        # ninguem fica inalcancavel porque todos tem ligacao direta
        self.assertEqual(len(resultado["afetados"]), 0)


if __name__ == "__main__":
    unittest.main()
