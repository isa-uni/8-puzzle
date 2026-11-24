import heapq
import itertools
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan: para cada peça, quantas linhas e colunas ela está do lugar certo.

        Cada movimento anda só uma casa, então a conta nunca passa do número real de movimentos que faltam.
        """
        soma = 0
        for indice, peca in enumerate(state.tiles):
            if peca == 0:
                continue
            indice_objetivo = peca - 1   # a peça 1 deve ficar no índice 0, a 2 no índice 1, e assim por diante
            linha, coluna = divmod(indice, 3)
            linha_objetivo, coluna_objetivo = divmod(indice_objetivo, 3)
            soma += abs(linha - linha_objetivo) + abs(coluna - coluna_objetivo)
        return soma

    def search(self, initial: State) -> SearchResult:
        # A fila de prioridade sempre tira o estado com menor f = g + h.
        # O contador só serve para desempatar (sem ele, o heapq tentaria comparar States).
        contador = itertools.count()
        fila = [(initial.cost + self.heuristic(initial), next(contador), initial)]

        # Menor custo g (movimentos até o estado) encontrado para cada tabuleiro.
        menor_g = {initial: initial.cost}

        nos_expandidos = 0
        nos_gerados = 1
        maior_fronteira = 1

        while fila:
            _, _, atual = heapq.heappop(fila)

            # Entrada antiga: este tabuleiro já foi achado por um caminho mais curto.
            if atual.cost > menor_g[atual]:
                continue
            nos_expandidos += 1

            # A heurística nunca superestima, então o primeiro objetivo que sai da fila é o ótimo.
            if atual.is_goal:
                return SearchResult(
                    solution=atual,
                    nodes_expanded=nos_expandidos,
                    nodes_generated=nos_gerados,
                    max_frontier_size=maior_fronteira,
                    depth=atual.cost,
                )

            for filho in atual.neighbors():
                nos_gerados += 1
                # Guarda o filho se é novo ou se chegou por um caminho mais curto.
                if filho not in menor_g or filho.cost < menor_g[filho]:
                    menor_g[filho] = filho.cost
                    prioridade = filho.cost + self.heuristic(filho)
                    heapq.heappush(fila, (prioridade, next(contador), filho))

            maior_fronteira = max(maior_fronteira, len(fila))

        # A fila esvaziou sem achar o objetivo: não há solução.
        return SearchResult(
            solution=None,
            nodes_expanded=nos_expandidos,
            nodes_generated=nos_gerados,
            max_frontier_size=maior_fronteira,
            depth=0,
        )
