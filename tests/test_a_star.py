from algorithms.a_star import AStar
from algorithms.bfs import BFS
from puzzle.state import State, GOAL_STATE
from tests.helpers import aplicar_acoes, embaralhar

ESTADO_PRINCIPAL = (1, 8, 3, 2, 6, 4, 7, 0, 5)   # solúvel, custo ótimo 19
INSOLUVEL = (2, 1, 3, 4, 5, 6, 7, 8, 0)


# ---------- heuristic() ----------

def test_heuristica_do_objetivo_é_zero():
    assert AStar().heuristic(State(GOAL_STATE)) == 0


def test_heuristica_de_um_movimento_é_um():
    # A peça 8 está no índice 8 e deveria estar no índice 7: distância 1
    assert AStar().heuristic(State((1, 2, 3, 4, 5, 6, 7, 0, 8))) == 1


def test_heuristica_de_duas_pecas_trocadas_é_dois():
    # Peça 2 no índice 0 (deveria estar no 1) e peça 1 no índice 1 (deveria estar no 0)
    assert AStar().heuristic(State((2, 1, 3, 4, 5, 6, 7, 8, 0))) == 2


def test_heuristica_do_estado_principal():
    assert AStar().heuristic(State(ESTADO_PRINCIPAL)) == 9


def test_heuristica_nunca_superestima_o_custo_real():
    # Admissível: heurística <= distância real até o objetivo.
    # Usamos o BFS, que dá a distância real.
    for semente in range(5):
        estado = embaralhar(8, semente)
        custo_real = BFS().search(State(estado.tiles)).path_cost
        assert AStar().heuristic(estado) <= custo_real


def test_heuristica_nunca_superestima_com_embaralhados_de_k_movimentos():
    # Um embaralhado de k movimentos está no máximo a k do objetivo
    for k in range(1, 9):
        estado = embaralhar(k, k)
        assert AStar().heuristic(estado) <= k


# ---------- search() ----------

def test_objetivo_retorna_zero_movimentos():
    resultado = AStar().search(State(GOAL_STATE))
    assert resultado.found
    assert resultado.path_cost == 0
    assert resultado.actions == []
    assert resultado.nodes_expanded == 1


def test_um_movimento_é_encontrado_como_otimo():
    resultado = AStar().search(State((1, 2, 3, 4, 5, 6, 7, 0, 8)))
    assert resultado.found
    assert resultado.path_cost == 1
    assert resultado.actions == ["direita"]


def test_solucao_leva_ao_objetivo_e_custo_bate_com_depth():
    inicial = State(ESTADO_PRINCIPAL)
    resultado = AStar().search(inicial)
    assert resultado.found
    assert resultado.solution.is_goal
    assert resultado.depth == resultado.path_cost == len(resultado.actions)
    assert aplicar_acoes(inicial.tiles, resultado.actions) == GOAL_STATE


def test_estado_principal_tem_custo_otimo_19():
    assert AStar().search(State(ESTADO_PRINCIPAL)).path_cost == 19


def test_custo_igual_ao_bfs_em_embaralhados():
    # A* com heurística admissível deve achar o mesmo custo ótimo que o BFS
    for semente in range(5):
        inicial = embaralhar(10, semente)
        resultado_astar = AStar().search(State(inicial.tiles))
        resultado_bfs = BFS().search(State(inicial.tiles))
        assert resultado_astar.path_cost == resultado_bfs.path_cost


def test_expande_menos_estados_que_o_bfs():
    resultado_astar = AStar().search(State(ESTADO_PRINCIPAL))
    resultado_bfs = BFS().search(State(ESTADO_PRINCIPAL))
    assert resultado_astar.nodes_expanded < resultado_bfs.nodes_expanded


def test_estado_insoluvel_nao_tem_solucao():
    resultado = AStar().search(State(INSOLUVEL))
    assert not resultado.found
    assert resultado.solution is None
    assert resultado.path_cost == -1
    assert resultado.actions == []


def test_contadores_sao_coerentes():
    resultado = AStar().search(State(ESTADO_PRINCIPAL))
    assert resultado.nodes_expanded >= 1
    assert resultado.nodes_generated >= resultado.nodes_expanded
    assert resultado.max_frontier_size >= 1
