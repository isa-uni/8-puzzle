from algorithms.bfs import BFS
from puzzle.state import State, GOAL_STATE
from tests.helpers import aplicar_acoes, embaralhar

ESTADO_PRINCIPAL = (1, 8, 3, 2, 6, 4, 7, 0, 5)   # solúvel, custo ótimo 19
INSOLUVEL = (2, 1, 3, 4, 5, 6, 7, 8, 0)          # uma troca de 2 peças: sem solução


def test_objetivo_retorna_zero_movimentos():
    resultado = BFS().search(State(GOAL_STATE))
    assert resultado.found
    assert resultado.path_cost == 0
    assert resultado.depth == 0
    assert resultado.actions == []
    assert resultado.nodes_expanded == 1


def test_um_movimento_é_encontrado_como_otimo():
    resultado = BFS().search(State((1, 2, 3, 4, 5, 6, 7, 0, 8)))
    assert resultado.found
    assert resultado.path_cost == 1
    assert resultado.actions == ["direita"]


def test_solucao_leva_ao_objetivo_e_custo_bate_com_depth():
    inicial = State(ESTADO_PRINCIPAL)
    resultado = BFS().search(inicial)
    assert resultado.found
    assert resultado.solution.is_goal
    assert resultado.depth == resultado.path_cost == len(resultado.actions)
    assert aplicar_acoes(inicial.tiles, resultado.actions) == GOAL_STATE


def test_estado_principal_tem_custo_otimo_19():
    resultado = BFS().search(State(ESTADO_PRINCIPAL))
    assert resultado.path_cost == 19


def test_embaralhados_com_k_movimentos_têm_custo_no_maximo_k():
    for semente in range(3):
        inicial = embaralhar(6, semente)
        resultado = BFS().search(inicial)
        assert resultado.found
        assert resultado.path_cost <= 6
        assert aplicar_acoes(inicial.tiles, resultado.actions) == GOAL_STATE


def test_estado_insoluvel_nao_tem_solucao():
    resultado = BFS().search(State(INSOLUVEL))
    assert not resultado.found
    assert resultado.solution is None
    assert resultado.path_cost == -1
    assert resultado.actions == []


def test_contadores_sao_coerentes():
    resultado = BFS().search(State(ESTADO_PRINCIPAL))
    assert resultado.nodes_expanded >= 1
    assert resultado.nodes_generated >= resultado.nodes_expanded
    assert resultado.max_frontier_size >= 1
