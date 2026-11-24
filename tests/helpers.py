"""Funções auxiliares compartilhadas pelos testes."""

import random

from puzzle.state import State, GOAL_STATE

# Nome da ação -> quanto o índice do espaço vazio muda
DESLOCAMENTO = {"cima": -3, "baixo": 3, "esquerda": -1, "direita": 1}


def aplicar_acoes(tiles, acoes):
    """Aplica uma lista de ações sobre um tabuleiro e devolve a tupla resultante."""
    tabuleiro = list(tiles)
    vazio = tabuleiro.index(0)
    for acao in acoes:
        destino = vazio + DESLOCAMENTO[acao]
        tabuleiro[vazio], tabuleiro[destino] = tabuleiro[destino], tabuleiro[vazio]
        vazio = destino
    return tuple(tabuleiro)


def embaralhar(k, semente):
    """Embaralha o objetivo com k movimentos aleatórios.

    Devolve um State novo, sem histórico de parent/cost, para ser usado
    como estado inicial de uma busca. A distância até o objetivo é no máximo k.
    """
    gerador = random.Random(semente)
    estado = State(GOAL_STATE)
    for _ in range(k):
        estado = gerador.choice(estado.neighbors())
    return State(estado.tiles)


def passo(estado, acao):
    """Devolve o vizinho de `estado` obtido com a ação `acao`."""
    return next(filho for filho in estado.neighbors() if filho.action == acao)
