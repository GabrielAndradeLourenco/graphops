"""Ponto de entrada do GraphOps - interface CLI."""

import argparse
import sys
import os

# garantindo que o python ache os modulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reader.file_reader import ler_grafo_json
from algorithms.betweenness import ranking_spofs
from algorithms.cascade import simular_falha


def executar_centralidade(grafo):
    print("\n=== Analise de Centralidade (SPOFs) ===\n")
    print(f"Grafo carregado: {grafo.numero_vertices()} vertices, "
          f"{grafo.numero_arestas()} arestas\n")

    ranking = ranking_spofs(grafo)
    print(f"{'Servico':<20} {'Betweenness':>12}")
    print("-" * 34)
    for nome, valor in ranking:
        marcador = "  <-- SPOF" if valor == ranking[0][1] and valor > 0 else ""
        print(f"{nome:<20} {valor:>12.2f}{marcador}")
    print()


def executar_cascata(grafo, origem, removido):
    print("\n=== Simulacao de Falha em Cascata ===\n")
    resultado = simular_falha(grafo, origem, removido)

    print(f"Servico removido: {resultado['removido']}")
    print(f"Servicos ainda alcancaveis a partir do Gateway: "
          f"{', '.join(resultado['alcancaveis']) or '(nenhum)'}")
    print(f"Servicos afetados (inalcancaveis): "
          f"{', '.join(resultado['afetados']) or '(nenhum)'}")
    print(f"Percentual de impacto: {resultado['percentual_impacto']}%\n")


def main():
    parser = argparse.ArgumentParser(
        description="GraphOps - analise de dependencias de microsservicos"
    )
    parser.add_argument("--input", required=True,
                        help="caminho do arquivo JSON com o grafo")
    parser.add_argument("--acao", required=True,
                        choices=["centralidade", "cascata"],
                        help="acao a executar")
    parser.add_argument("--origem", type=int, default=0,
                        help="vertice de origem pra cascata (padrao: 0)")
    parser.add_argument("--remover", type=int,
                        help="id do vertice a ser removido na simulacao")

    args = parser.parse_args()

    grafo = ler_grafo_json(args.input)

    if args.acao == "centralidade":
        executar_centralidade(grafo)
    elif args.acao == "cascata":
        if args.remover is None:
            print("Erro: --remover e obrigatorio pra acao cascata")
            sys.exit(1)
        executar_cascata(grafo, args.origem, args.remover)


if __name__ == "__main__":
    main()
