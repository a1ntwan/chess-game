from import_test_classes import Pawn, Rook, Knight, Bishop, Queen, King, PotentialAttack


def test_pawn():
    """Тест ходов и атак пешки"""
    p = Pawn('e2', 'P', 'p1')
    assert p.move('e2', 'e3') == ('e', 3)
    p = Pawn('e2', 'P', 'p1')
    assert p.move('e2', 'e4') == ('e', 4)
    p = Pawn('e2', 'P', 'p1')
    assert p.move('e2', 'f3') == ('f', 3)
    p = Pawn('e2', 'P', 'p1')
    assert p.move('e2', 'd3') == ('d', 3)
    p = Pawn('e2', 'P', 'p1')
    assert p.move('e2', 'd3') != ('f', 2)
    p = Pawn('e2', 'P', 'p1')
    assert p.move('e2', 'e3') != ('g', 4)


def test_rook():
    """Тесты ходов и атак ладьи"""
    r = Rook('h3', 'R', 'r3')
    assert r.move('h3', 'h5') is True
    r = Rook('h5', 'R', 'r1')
    assert r.move('h5', 'c5') is True


def test_knight():
    """Тесты ходов и атак коня"""
    kn = Knight('d4', 'N', 'n')
    assert kn.move('d4', 'f3') is True
    kn = Knight('d4', 'N', 'n')
    assert kn.move('d4', 'f5') is True
    kn = Knight('d4', 'N', 'n')
    assert kn.move('d4', 'b5') is True
    kn = Knight('d4', 'N', 'n')
    assert kn.move('d4', 'e6') is True
    kn = Knight('d4', 'N', 'n')
    assert kn.move('d4', 'c6') is True
    kn = Knight('d4', 'N', 'n')
    assert kn.move('d4', 'c2') is True
    kn = Knight('d4', 'N', 'n')
    assert kn.move('d4', 'e2') is True


def test_bishop():
    """Тесты ходов и атак слона"""
    bish = Bishop('g2', 'B', 'b1')
    assert bish.move('g2', 'e4') is True
    bish = Bishop('g2', 'B', 'b1')
    assert bish.move('g2', 'h3') is True


def test_queen():
    """Тесты ходов и атак ферзя"""
    q = Queen('d4', 'Q', name='q')
    assert q.move('d4', 'd6') is True
    q = Queen('d4', 'Q', name='q')
    assert q.move('d4', 'd3') is True
    q = Queen('d4', 'Q', name='q')
    assert q.move('d4', 'h4') is True
    q = Queen('d4', 'Q', name='q')
    assert q.move('d4', 'a4') is True
    q = Queen('d4', 'Q', name='q')
    assert q.move('d4', 'f6') is True
    q = Queen('d4', 'Q', name='q')
    assert q.move('d4', 'b6') is True
    q = Queen('e5', 'Q', name='q')
    assert q.move('e5', 'c3') is True
    q = Queen('e5', 'Q', name='q')
    assert q.move('e5', 'g4') is True


def test_king():
    """Тесты ходов и атак короля"""
    k = King('e2', 'K', 'k')
    assert k.move('e2', 'e1') is True
    k = King('e2', 'K', 'k')
    assert k.move('e2', 'd1') is True
    k = King('e2', 'K', 'k')
    assert k.move('e2', 'f1') is True
    k = King('e2', 'K', 'k')
    assert k.move('e2', 'f2') is True
    k = King('e2', 'K', 'k')
    assert k.move('e2', 'd2') is True
    k = King('e2', 'K', 'k')
    assert k.move('e2', 'f3') is True
    k = King('e2', 'K', 'k')
    assert k.move('e2', 'd3') is True
    k = King('e2', 'K', 'k')
    assert k.move('e2', 'e3') is True


def test_moves_pot():
    """Потенциальные атаки каждой фигуры"""
    assert set(PotentialAttack.pawn_pot('c2')) == {'b3', 'd3'}
    assert set(PotentialAttack.knight_pot('b1')) == {'d2', 'c3', 'a1', 'c1', 'a3'}
    assert set(PotentialAttack.rook_pot('h1')) == {'h6', 'h8', 'h3', 'h5', 'f1', 'h7', 'h2', 'e1', 'b1', 'c1', 'h4',
                                                   'g1', 'a1', 'd1'}
    assert set(PotentialAttack.bishop_pot('f5')) == {'d3', 'g6', 'e4', 'h7', 'g4', 'h3', 'e6', 'd7', 'c2', 'b1', 'c8'}
    assert set(PotentialAttack.queen_pot('f4')) == {'f1', 'd2', 'a4', 'e3', 'g5', 'h4', 'f6', 'd6', 'g3', 'f5', 'b4',
                                                    'f2', 'g4', 'f3', 'f7', 'e4', 'c1', 'f8', 'b8', 'e5', 'h2', 'h6',
                                                    'd4', 'c7', 'c4'}
    assert set(PotentialAttack.king_pot('e4')) == {'f5', 'e3', 'e5', 'f4', 'f3', 'd4', 'd5', 'd3'}
