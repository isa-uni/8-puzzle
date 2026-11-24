from algorithms.dfs import DFS, DEFAULT_DEPTH_LIMIT
from puzzle.state import State, GOAL_STATE
from tests.helpers import aplicar_acoes, embaralhar

ESTADO_PRINCIPAL = (1, 8, 3, 2, 6, 4, 7, 0, 5)   # solúvel, a solução ótima tem 19 movimentos
INSOLUVEL = (2, 1, 3, 4, 5, 6, 7, 8, 0)
DOIS_MOVIMENTOS = (1, 2, 3, 4, 0, 5, 7, 8, 6)    # solução ótima tem 2 movimentos


def test_limite_padrao_é_50():
    assert DFS().depth_limit == DEFAULT_DEPTH_LIMIT == 50


def test_objetivo_retorna_zero_movimentos():
    resultado = DFS().search(State(GOAL_STATE))
    assert resultado.found
    assert resultado.path_cost == 0
    assert resultado.actions == []
    assert resultado.nodes_expanded == 1


def test_solucao_leva_ao_objetivo_e_custo_bate_com_depth():
    inicial = State(ESTADO_PRINCIPAL)
    resultado = DFS().search(inicial)
    assert resultado.found
    assert resultado.solution.is_goal
    assert resultado.depth == resultado.path_cost == len(resultado.actions)
    assert aplicar_acoes(inicial.tiles, resultado.actions) == GOAL_STATE


def test_solucao_respeita_o_limite_de_profundidade():
    resultado = DFS().search(State(ESTADO_PRINCIPAL))
    assert resultado.path_cost <= DEFAULT_DEPTH_LIMIT


def test_embaralhados_sao_resolvidos_com_acoes_validas():
    # Limite pequeno (6): o embaralhado tem no máximo 3 movimentos, então a solução cabe no limite.
    # Sem limite pequeno, o DFS pode demorar bastante em alguns embaralhados.
    for semente in range(3):
        inicial = embaralhar(3, semente)
        resultado = DFS(depth_limit=6).search(inicial)
        assert resultado.found
        assert aplicar_acoes(inicial.tiles, resultado.actions) == GOAL_STATE


def test_limite_baixo_demais_nao_encontra_a_solucao():
    # Precisa de 2 movimentos: com limite 1 não pode achar
    resultado = DFS(depth_limit=1).search(State(DOIS_MOVIMENTOS))
    assert not resultado.found
    assert resultado.solution is None


def test_limite_suficiente_encontra_a_solucao_otima_do_caso():
    # Com limite 2, a única solução possível tem exatamente 2 movimentos
    resultado = DFS(depth_limit=2).search(State(DOIS_MOVIMENTOS))
    assert resultado.found
    assert resultado.path_cost == 2
    assert aplicar_acoes(DOIS_MOVIMENTOS, resultado.actions) == GOAL_STATE


def test_estado_insoluvel_nao_tem_solucao_dentro_do_limite():
    # Limite pequeno para o teste ser rápido
    resultado = DFS(depth_limit=12).search(State(INSOLUVEL))
    assert not resultado.found
    assert resultado.solution is None
    assert resultado.path_cost == -1
