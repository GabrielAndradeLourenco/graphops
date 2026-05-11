"""Estrutura do grafo dirigido e ponderado usando lista de adjacencia."""


class Graph:
    def __init__(self):
        # dicionario {vertice: [(destino, peso), ...]}
        self.adj = {}
        # guarda os nomes dos servicos {id: nome}
        self.nomes = {}

    def adicionar_vertice(self, id_vertice, nome=None):
        if id_vertice not in self.adj:
            self.adj[id_vertice] = []
            self.nomes[id_vertice] = nome if nome else str(id_vertice)

    def adicionar_aresta(self, origem, destino, peso=1):
        # se algum dos vertices nao existe ainda, cria
        if origem not in self.adj:
            self.adicionar_vertice(origem)
        if destino not in self.adj:
            self.adicionar_vertice(destino)
        self.adj[origem].append((destino, peso))

    def vizinhos(self, vertice):
        # devolve so os ids dos destinos, sem os pesos
        if vertice not in self.adj:
            return []
        return [destino for destino, _ in self.adj[vertice]]

    def vertices(self):
        return list(self.adj.keys())

    def numero_vertices(self):
        return len(self.adj)

    def numero_arestas(self):
        return sum(len(vizinhos) for vizinhos in self.adj.values())

    def nome_do(self, id_vertice):
        return self.nomes.get(id_vertice, str(id_vertice))
