from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        # 1. Fronteira: fila onde ficam os estados esperando para serem explorados.
        #    FIFO (primeiro a entrar, primeiro a sair) é o que faz a busca ir nível por nível.
        fronteira = deque([initial])

        # 2. Visitados: guarda os estados que já entraram na fronteira,
        #    para não explorar o mesmo tabuleiro duas vezes.
        visitados = {initial}

        # 3. Contadores para o relatório final.
        nos_expandidos = 0
        nos_gerados = 1          # o estado inicial também foi "gerado"
        maior_fronteira = 1

        while fronteira:
            # 4. Tira o estado mais antigo da fila: ele será expandido agora.
            atual = fronteira.popleft()
            nos_expandidos += 1

            # 5. Achou o objetivo? Então a busca terminou.
            if atual.is_goal:
                return SearchResult(
                    solution=atual,
                    nodes_expanded=nos_expandidos,
                    nodes_generated=nos_gerados,
                    max_frontier_size=maior_fronteira,
                    depth=atual.cost,   # cost = número de movimentos até aqui
                )

            # 6. Gera os filhos e enfileira só os que ainda não foram vistos.
            for filho in atual.neighbors():
                nos_gerados += 1
                if filho not in visitados:
                    visitados.add(filho)        # marca como visto
                    fronteira.append(filho)     # e coloca na fila

            # 7. Atualiza o maior tamanho que a fronteira já teve.
            maior_fronteira = max(maior_fronteira, len(fronteira))

        # 8. A fila esvaziou sem achar o objetivo: não há solução.
        return SearchResult(
            solution=None,
            nodes_expanded=nos_expandidos,
            nodes_generated=nos_gerados,
            max_frontier_size=maior_fronteira,
            depth=0,
        )
