import random

from puzzle.state import State, GOAL_STATE
from tests.helpers import DESLOCAMENTO, aplicar_acoes, passo


# ---------- neighbors() ----------

def test_objetivo_tem_dois_vizinhos_cima_e_esquerda():
    # Objetivo: vazio no canto inferior direito (índice 8), só pode subir ou ir para a esquerda
    filhos = State(GOAL_STATE).neighbors()
    assert len(filhos) == 2
    assert sorted(filho.action for filho in filhos) == ["cima", "esquerda"]


def test_vazio_no_canto_superior_esquerdo_tem_dois_vizinhos():
    filhos = State((0, 1, 2, 3, 4, 5, 6, 7, 8)).neighbors()
    assert sorted(filho.action for filho in filhos) == ["baixo", "direita"]


def test_vazio_no_centro_tem_quatro_vizinhos():
    filhos = State((1, 2, 3, 4, 0, 5, 6, 7, 8)).neighbors()
    assert len(filhos) == 4
    assert sorted(filho.action for filho in filhos) == sorted(DESLOCAMENTO)


def test_vizinhos_trocam_o_vazio_com_a_peca_certa():
    filhos = {filho.action: filho for filho in State(GOAL_STATE).neighbors()}
    # vazio (índice 8) sobe: troca com a peça do índice 5, que é 6
    assert filhos["cima"].tiles == (1, 2, 3, 4, 5, 0, 7, 8, 6)
    # vazio (índice 8) vai para a esquerda: troca com a peça do índice 7, que é 8
    assert filhos["esquerda"].tiles == (1, 2, 3, 4, 5, 6, 7, 0, 8)


def test_vizinhos_guardam_pai_acao_e_custo_mais_um():
    raiz = State(GOAL_STATE, cost=3)
    for filho in raiz.neighbors():
        assert filho.parent is raiz
        assert filho.cost == 4
        assert filho.action in DESLOCAMENTO


def test_vizinhos_nao_alteram_o_estado_original():
    raiz = State(GOAL_STATE)
    raiz.neighbors()
    assert raiz.tiles == GOAL_STATE
    assert raiz.parent is None
    assert raiz.action is None


def test_vizinhos_sao_tabuleiros_validos_com_0_a_8():
    gerador = random.Random(0)
    estado = State((2, 8, 3, 1, 6, 4, 7, 0, 5))
    for _ in range(30):
        for filho in estado.neighbors():
            assert sorted(filho.tiles) == list(range(9))
        estado = gerador.choice(estado.neighbors())


# ---------- path() ----------

def test_path_do_inicial_e_somente_ele_mesmo():
    raiz = State(GOAL_STATE)
    caminho = raiz.path()
    assert len(caminho) == 1
    assert caminho[0] is raiz


def test_path_vai_do_inicial_ate_o_atual_nessa_ordem():
    raiz = State(GOAL_STATE)
    filho = passo(raiz, "cima")
    neto = passo(filho, "esquerda")

    caminho = neto.path()
    assert len(caminho) == 3
    assert caminho[0] is raiz
    assert caminho[1] is filho
    assert caminho[2] is neto


# ---------- actions() ----------

def test_actions_do_inicial_é_lista_vazia():
    assert State(GOAL_STATE).actions() == []


def test_actions_registram_os_movimentos_na_ordem():
    raiz = State(GOAL_STATE)
    estado = passo(passo(raiz, "cima"), "esquerda")
    assert estado.actions() == ["cima", "esquerda"]


def test_actions_reproduzem_o_tabuleiro_atual():
    gerador = random.Random(3)
    raiz = State((2, 8, 3, 1, 6, 4, 7, 0, 5))
    estado = raiz
    for _ in range(12):
        estado = gerador.choice(estado.neighbors())
    assert aplicar_acoes(raiz.tiles, estado.actions()) == estado.tiles
    assert len(estado.actions()) == estado.cost
