from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado."""
        pos_vazio = self.blank_index          # posição do espaço vazio (0 a 8)
        linha, coluna = divmod(pos_vazio, 3)  # linha e coluna dessa posição no tabuleiro 3x3

        # Cada movimento: (nome da ação, posição da peça que troca com o vazio, se cabe no tabuleiro)
        movimentos = [
            ("cima",     pos_vazio - 3, linha > 0),
            ("baixo",    pos_vazio + 3, linha < 2),
            ("esquerda", pos_vazio - 1, coluna > 0),
            ("direita",  pos_vazio + 1, coluna < 2),
        ]

        filhos = []
        for acao, destino, valido in movimentos:
            if not valido:
                continue
            novas_pecas = list(self.tiles)                    # tupla não pode ser alterada, então copiamos para lista
            novas_pecas[pos_vazio], novas_pecas[destino] = novas_pecas[destino], novas_pecas[pos_vazio]
            filhos.append(
                State(tuple(novas_pecas), parent=self, action=acao, cost=self.cost + 1)
            )
        return filhos

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este."""
        estados = []
        atual = self
        while atual is not None:      # sobe pelos pais até chegar ao inicial (parent é None)
            estados.append(atual)
            atual = atual.parent
        estados.reverse()             # estava do atual para o inicial; inverte para o inicial vir primeiro
        return estados

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este."""
        # o primeiro estado do caminho é o inicial, que não tem ação (action=None), então pulamos ele
        return [estado.action for estado in self.path()[1:]]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
