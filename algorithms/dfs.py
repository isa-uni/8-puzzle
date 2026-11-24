from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        # Pilha: o último a entrar é o primeiro a sair.
        pilha = [initial]

        # Para cada tabuleiro, guarda a menor profundidade em que ele foi achado.
        menor_profundidade = {initial: initial.cost}

        nos_expandidos = 0
        nos_gerados = 1
        maior_fronteira = 1

        while pilha:
            atual = pilha.pop()

            # Entrada antiga: este tabuleiro já foi achado por um caminho mais curto.
            if atual.cost > menor_profundidade[atual]:
                continue
            nos_expandidos += 1

            if atual.is_goal:
                return SearchResult(
                    solution=atual,
                    nodes_expanded=nos_expandidos,
                    nodes_generated=nos_gerados,
                    max_frontier_size=maior_fronteira,
                    depth=atual.cost,
                )

            # Chegou no limite de profundidade: não cria filhos.
            if atual.cost >= self.depth_limit:
                continue

            for filho in atual.neighbors():
                nos_gerados += 1
                # Guarda o filho se é novo ou se chegou por um caminho mais curto.
                if filho not in menor_profundidade or filho.cost < menor_profundidade[filho]:
                    menor_profundidade[filho] = filho.cost
                    pilha.append(filho)

            maior_fronteira = max(maior_fronteira, len(pilha))

        # A pilha esvaziou sem achar o objetivo dentro do limite.
        return SearchResult(
            solution=None,
            nodes_expanded=nos_expandidos,
            nodes_generated=nos_gerados,
            max_frontier_size=maior_fronteira,
            depth=0,
        )
