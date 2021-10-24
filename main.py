from itertools import product, chain
from functools import wraps
from contextlib import redirect_stdout
from more_itertools import filter_except


product = sorted(product('abcdefgh', '12345678'), key=lambda x: x[1], reverse=True)
save = {str(z + j): '-' for _, _ in enumerate(range(1, 65), 1) for z, j in product}
turn = [0, 1]


class Chessboard:

    @staticmethod
    def chessboard(func):
        """Chessboard decorator"""

        @wraps(func)
        def wrapper(one, two):
            if len(one) == len(two) == 2 and one[0]:
                if one[0] == two[0] and one[1] == two[1]:
                    print("You have not moved!")
                    raise BaseException
                if (ord(one[0]) in range(ord('a'), ord('i')) and ord(two[0]) in range(ord('a'), ord('i'))) \
                        and (int(one[1]) in range(1, 9) and int(two[1]) in range(1, 9)):
                    return func(one, two)
                else:
                    print('Wrong input (the letter is following "H" or the integer is more than 8)')
                    raise BaseException
            else:
                print('Wrong input')
                raise BaseException

        return wrapper

    @staticmethod
    def self_checker(func):
        """Starting with your piece"""

        @wraps(func)
        def wrapper(one, two):
            if turn[1] % 2 != 0:
                if str(save[one][0]).islower() or save[one] == '-':
                    print('Choose your piece!')
                    raise BaseException
                return func(one, two)
            else:
                if str(save[one][0]).isupper() or save[one] == '-':
                    print('Choose your piece!')
                    raise BaseException
                return func(one, two)

        return wrapper

    @staticmethod
    def show_chessboard(num):
        """Chessboard output"""
        ind = 1
        nums = 8
        for i, (index, value) in enumerate(save.items(), 1):
            if i == ind:
                print(f'[{nums}]  ', sep='', end='')
                nums -= 1
                ind += 8
            if i % 8 == 0:
                print(f' {value[0]} ', sep='', end='\n')
            else:
                print(f' {value[0]} ', sep='', end='')
        print(f' {str(num).zfill(2)}', ' [A][B][C][D][E][F][G][H]')


class Move:
    """This class is responsible for piece movement"""

    def __init__(self, ini, logo, name):
        self.x, self.y = ini[0], int(ini[1])
        self.logo = logo
        self.name = name

    @property
    def location(self):
        """Location getter"""
        return self.x, int(self.y)

    @location.setter
    def location(self, value):
        """Location setter"""
        one, two, obj = value[0], value[1], value[2]
        if obj.color == 'white':
            if w.__dict__[save[one][1]].move(one=one, two=two):
                self.x, self.y = two[0], two[1]
                # During the attack on blacks delete black piece and move
                if str(save[two][0]).islower():
                    save[two], save[one] = save[one], '-'
                    del b.__dict__[save[two][1]]
                # During the ordinary move or castling just switch the chessboard squares
                else:
                    save[one], save[two] = save[two], save[one]
        else:
            if b.__dict__[save[one][1]].move(one=one, two=two):
                self.x, self.y = two[0], two[1]
                # During the attack on whites delete white piece and move
                if str(save[two][0]).isupper():
                    save[two], save[one] = save[one], '-'
                    del w.__dict__[save[two][1]]
                # During the ordinary move or castling just switch the chessboard squares
                else:
                    save[one], save[two] = save[two], save[one]


class Pawn(Move):
    """This is a pawn, it has:
            1) simple move +
            2) two-square move on it's first move +
            3) attack +
            4) it becomes any type of piece if it reaches the end of the board +
    """

    def __init__(self, ini, logo, name):
        """Piece initialization"""
        super().__init__(ini, logo, name)
        save[ini] = (self.logo, self.name)

    def move(self, one, two):
        """Simple and two-square moves. Piece transformation."""
        # First move
        if (one[1] == '2' or one[1] == '7') and (one[0] == two[0] and abs(int(two[1]) - int(one[1])) == 2):
            self.x, self.y = two[0], int(two[1])
            return self.x, self.y
        # Piece transformation during a move or attack
        elif (one[0] == two[0] and ((two[1] == '8' or two[1] == '1') and abs(int(two[1]) - int(one[1])) == 1)) or \
                (two[1] == '8' and str(self.logo).isupper() and abs(ord(two[0]) - ord(one[0])) == 1 and
                 ord(two[1]) - ord(one[1]) == 1) or \
                (two[1] == '1' and str(self.logo).islower() and abs(ord(two[0]) - ord(one[0])) == 1 and
                 ord(one[1]) - ord(two[1]) == 1):
            transform = input("""You've reached the end of the board, choose the piece you'd like to have:
            any key -> queen
            b -> bishop
            r -> rook
            n -> knight
            """).strip().lower()
            if transform == 'b':
                if str(self.logo).isupper():
                    name, ini, logo = self.name, two[0] + str(two[1]), 'B'
                    w.delete(name)
                    w.append(ini, logo, name, Bishop, name)
                else:
                    name, ini, logo = self.name, two[0] + str(two[1]), 'b'
                    b.delete(name)
                    b.append(ini, logo, name, Bishop, name)
                save[one], save[two] = '-', (logo, name)
            elif transform == 'r':
                if str(self.logo).isupper():
                    name, ini, logo = self.name, two[0] + str(two[1]), 'R'
                    w.delete(name)
                    w.append(ini, logo, name, Rook, name)
                else:
                    name, ini, logo = self.name, two[0] + str(two[1]), 'r'
                    b.delete(name)
                    b.append(ini, logo, name, Rook, name)
                save[one], save[two] = '-', (logo, name)
            elif transform == 'n':
                if str(self.logo).isupper():
                    name, ini, logo = self.name, two[0] + str(two[1]), 'N'
                    w.delete(name)
                    w.append(ini, logo, name, Knight, name)
                else:
                    name, ini, logo = self.name, two[0] + str(two[1]), 'n'
                    b.delete(name)
                    b.append(ini, logo, name, Knight, name)
                save[one], save[two] = '-', (logo, name)
            else:
                if str(self.logo).isupper():
                    name, ini, logo = self.name, two[0] + str(two[1]), 'Q'
                    w.delete(name)
                    w.append(ini, logo, name, Queen, name)
                else:
                    name, ini, logo = self.name, two[0] + str(two[1]), 'q'
                    b.delete(name)
                    b.append(ini, logo, name, Queen, name)
                save[one], save[two] = '-', (logo, name)

        # Simple move
        elif str(self.logo).islower() and one[0] == two[0] and ord(one[1]) - ord(two[1]) == 1:
            self.x, self.y = two[0], int(two[1])
            return self.x, self.y
        elif str(self.logo).isupper() and one[0] == two[0] and ord(two[1]) - ord(one[1]) == 1:
            self.x, self.y = two[0], int(two[1])
            return self.x, self.y
        # Attack
        elif str(self.logo).isupper() and abs(ord(two[0]) - ord(one[0])) == 1 and ord(two[1]) - ord(one[1]) == 1:
            self.x, self.y = two[0], int(two[1])
            return self.x, self.y
        elif str(self.logo).islower() and abs(ord(two[0]) - ord(one[0])) == 1 and ord(one[1]) - ord(two[1]) == 1:
            self.x, self.y = two[0], int(two[1])
            return self.x, self.y
        else:
            print("It's not a pawn's move!")
            raise BaseException

    def attack(self, one, two):
        """Extra attack method for attack vectors"""
        if str(self.logo).isupper() and abs(ord(two[0]) - ord(one[0])) == 1 and ord(two[1]) - ord(one[1]) == 1:
            return True
        elif str(self.logo).islower() and abs(ord(two[0]) - ord(one[0])) == 1 and ord(one[1]) - ord(two[1]) == 1:
            return True


class Knight(Move):
    """This is a knight, is has:
                1) simple move +
                2) jumps over other pieces
                3) attack +
    """

    def __init__(self, ini, logo, name):
        """Piece initialization"""
        super().__init__(ini, logo, name)
        save[ini] = (self.logo, self.name)

    @staticmethod
    def move(one, two):
        """Move with ability to jump over other pieces"""
        if (abs(ord(two[0]) - ord(one[0])) == 1 and abs(ord(two[1]) - ord(one[1])) == 2) \
                or (abs(ord(two[0]) - ord(one[0])) == 2 and abs(ord(two[1]) - ord(one[1])) == 1):
            return True
        print("It's not a knight's move!")
        raise BaseException


class Rook(Move):
    """This is a rook, it has:
                1) simple move +
                2) castling with a king if both have never moved +
                3) attack +
    """

    def __init__(self, ini, logo, name, static=True):
        """Piece initialization"""
        super().__init__(ini, logo, name)
        self.static = static
        save[ini] = (self.logo, self.name)

    def move(self, one, two):
        """Simple move"""
        if one[0] == two[0] and one[1] == two[1]:
            return True
        elif save[one] != '-' and save[one][1] != self.name:
            print("Rook can't jump over other pieces!")
            raise BaseException
        else:
            if one[0] == two[0] and one[1] < two[1]:
                return self.move((one[0] + str(int(one[1]) + 1)), two)
            elif one[0] < two[0] and one[1] == two[1]:
                return self.move((chr(ord(one[0]) + 1) + str(one[1])), two)
            elif one[0] == two[0] and one[1] > two[1]:
                return self.move((one[0] + str(int(one[1]) - 1)), two)
            elif one[0] > two[0] and one[1] == two[1]:
                return self.move((chr(ord(one[0]) - 1) + str(one[1])), two)
            else:
                print("It's not a rook's move!")
                raise BaseException


class Bishop(Move):
    """This is a bishop, it has:
                1) simple move+
    """

    def __init__(self, ini, logo, name):
        """Piece initialization"""
        super().__init__(ini, logo, name)
        save[ini] = (self.logo, self.name)

    def move(self, one, two):
        """Simple move"""
        if one[0] == two[0] and one[1] == two[1]:
            return True
        elif save[one] != '-' and save[one][1] != self.name:
            print("Bishop can't jump over other pieces!")
            raise BaseException

        else:
            if one[0] < two[0] and one[1] < two[1]:
                return self.move((chr(ord(one[0]) + 1) + str(int(one[1]) + 1)), two)
            elif one[0] > two[0] and one[1] > two[1]:
                return self.move((chr(ord(one[0]) - 1) + str(int(one[1]) - 1)), two)
            elif one[0] < two[0] and one[1] > two[1]:
                return self.move((chr(ord(one[0]) + 1) + str(int(one[1]) - 1)), two)
            elif one[0] > two[0] and one[1] < two[1]:
                return self.move((chr(ord(one[0]) - 1) + str(int(one[1]) + 1)), two)
            else:
                print("It's not a bishop's move!")
                raise BaseException


class Queen(Move):
    """This is a queen, it has:
                1) simple move +
                2) attack +
    """

    def __init__(self, ini, logo, name):
        """Piece initialization"""
        super().__init__(ini, logo, name)
        save[ini] = (self.logo, self.name)

    def move(self, one, two):
        """Simple move"""
        if one[0] == two[0] and one[1] == two[1]:
            return True
        elif save[one] != '-' and save[one][1] != self.name:
            print("Queen can't jump over other pieces!")
            raise BaseException
        else:
            if one[0] == two[0] and one[1] < two[1]:
                return self.move((one[0] + str(int(one[1]) + 1)), two)
            elif one[0] < two[0] and one[1] == two[1]:
                return self.move((chr(ord(one[0]) + 1) + str(one[1])), two)
            elif one[0] == two[0] and one[1] > two[1]:
                return self.move((one[0] + str(int(one[1]) - 1)), two)
            elif one[0] > two[0] and one[1] == two[1]:
                return self.move((chr(ord(one[0]) - 1) + str(one[1])), two)
            elif one[0] < two[0] and one[1] < two[1]:
                return self.move((chr(ord(one[0]) + 1) + str(int(one[1]) + 1)), two)
            elif one[0] > two[0] and one[1] > two[1]:
                return self.move((chr(ord(one[0]) - 1) + str(int(one[1]) - 1)), two)
            elif one[0] < two[0] and one[1] > two[1]:
                return self.move((chr(ord(one[0]) + 1) + str(int(one[1]) - 1)), two)
            elif one[0] > two[0] and one[1] < two[1]:
                return self.move((chr(ord(one[0]) - 1) + str(int(one[1]) + 1)), two)
            else:
                print("It's not a queen's move!")
                raise BaseException


class King(Move):
    """This is a king, it has:
                1) simple move +
                2) castling with rook, if both never moved
                3) attack +
                4) it can't move or attack a square if it's under attack +
    """

    def __init__(self, ini, logo, name, static=True):
        """Piece initialization"""
        super().__init__(ini, logo, name)
        self.static = static
        save[ini] = (self.logo, self.name)

    @staticmethod
    def move(one, two):
        """Simple move"""
        if (ord(two[0]) == ord(one[0]) and abs(ord(two[1]) - ord(one[1])) == 1) \
                or (abs(ord(two[0]) - ord(one[0])) == 1 and abs(ord(two[1]) - ord(one[1])) <= 1):
            return True
        print("It's not a king's move!")
        raise BaseException


class WhitePieces:
    """Whites class"""

    def __init__(self):
        """Whites initialization"""
        self.color = 'white'
        self.p1 = Pawn('a2', 'P', name='p1')
        self.p2 = Pawn('b2', 'P', name='p2')
        self.p3 = Pawn('c2', 'P', name='p3')
        self.p4 = Pawn('d2', 'P', name='p4')
        self.p5 = Pawn('e2', 'P', name='p5')
        self.p6 = Pawn('f2', 'P', name='p6')
        self.p7 = Pawn('g2', 'P', name='p7')
        self.p8 = Pawn('h2', 'P', name='p8')
        self.r1 = Rook('a1', 'R', name='r1')
        self.r2 = Rook('h1', 'R', name='r2')
        self.kn1 = Knight('b1', 'N', name='kn1')
        self.kn2 = Knight('g1', 'N', name='kn2')
        self.b1 = Bishop('c1', 'B', name='b1')
        self.b2 = Bishop('f1', 'B', name='b2')
        self.q = Queen('d1', 'Q', name='q')
        self.k = King('e1', 'K', name='k')

    def delete(self, obj):
        """Delete piece from class"""
        del self.__dict__[obj]

    def append(self, ini, logo, name, cls, obj):
        """Append piece to class if it has reached the opposite side of the board"""
        if cls is Queen:
            self.__dict__[obj] = Queen(ini, logo, name)
        elif cls is Bishop:
            self.__dict__[obj] = Bishop(ini, logo, name)
        elif cls is Rook:
            self.__dict__[obj] = Rook(ini, logo, name)
        elif cls is Knight:
            self.__dict__[obj] = Knight(ini, logo, name)


class BlackPieces:
    """Blacks class"""

    def __init__(self):
        """Blacks initialization"""
        self.color = 'black'
        self.p1 = Pawn('a7', 'p', name='p1')
        self.p2 = Pawn('b7', 'p', name='p2')
        self.p3 = Pawn('c7', 'p', name='p3')
        self.p4 = Pawn('d7', 'p', name='p4')
        self.p5 = Pawn('e7', 'p', name='p5')
        self.p6 = Pawn('f7', 'p', name='p6')
        self.p7 = Pawn('g7', 'p', name='p7')
        self.p8 = Pawn('h7', 'p', name='p8')
        self.r1 = Rook('a8', 'r', name='r1')
        self.r2 = Rook('h8', 'r', name='r2')
        self.kn1 = Knight('b8', 'n', name='kn1')
        self.kn2 = Knight('g8', 'n', name='kn2')
        self.b1 = Bishop('c8', 'b', name='b1')
        self.b2 = Bishop('f8', 'b', name='b2')
        self.q = Queen('d8', 'q', name='q')
        self.k = King('e8', 'k', name='k')

    def delete(self, obj):
        """Delete piece from class"""
        del self.__dict__[obj]

    def append(self, ini, logo, name, cls, obj):
        """Append piece to class if it has reached the opposite side of the board"""
        if cls is Queen:
            self.__dict__[obj] = Queen(ini, logo, name)
        elif cls is Bishop:
            self.__dict__[obj] = Bishop(ini, logo, name)
        elif cls is Rook:
            self.__dict__[obj] = Rook(ini, logo, name)
        elif cls is Knight:
            self.__dict__[obj] = Knight(ini, logo, name)


class PotentialAttack:
    """Calculating all attack vectors"""

    @staticmethod
    def pawn_pot(location):
        """Pawn attacks"""
        location = list(location)
        if turn[1] % 2 != 0:
            right = chr(ord(location[0]) + 1) + str(int(location[1]) + 1)
            left = chr(ord(location[0]) - 1) + str(int(location[1]) + 1)
            return [x for x in (right, left) if ord(chr(96)) < ord(x[0]) < ord('i') and 0 < int(x[1]) < 9]
        right = chr(ord(location[0]) + 1) + str(int(location[1]) - 1)
        left = chr(ord(location[0]) - 1) + str(int(location[1]) - 1)
        return [x for x in (right, left) if ord(chr(96)) < ord(x[0]) < ord('i') and 0 < int(x[1]) < 9]

    @staticmethod
    def knight_pot(location):
        """Knight attacks"""
        location = list(location)
        up_right = chr(ord(location[0]) + 1) + str(int(location[1]) + 2)
        up_left = chr(ord(location[0]) - 1) + str(int(location[1]) + 2)
        down_right = chr(ord(location[0]) + 1) + str(abs(int(location[1]) - 2))
        down_left = chr(ord(location[0]) - 1) + str(abs(int(location[1]) - 2))
        right_up = chr(ord(location[0]) + 2) + str(int(location[1]) + 1)
        left_up = chr(ord(location[0]) - 2) + str(int(location[1]) + 1)
        right_down = chr(ord(location[0]) + 2) + str(int(location[1]) - 1)
        left_down = chr(ord(location[0]) - 2) + str(int(location[1]) - 1)

        return [x for x in (up_right, up_left, down_right, down_left, right_up, left_up, right_down, left_down)
                if ord(chr(96)) < ord(x[0]) < ord('i') and 0 < int(x[1]) < 9]

    @staticmethod
    def rook_pot(location):
        """Rook attacks"""
        location = list(location)
        right = [chr(x) + str(location[1]) for x in range(ord(location[0]) + 1, ord('i'))]
        left = [chr(x) + str(location[1]) for x in range(ord(location[0]) - 1, ord(chr(96)), -1)]
        up = [location[0] + str(x) for x in range(int(location[1]) + 1, 9)]
        down = [location[0] + str(x) for x in range(int(location[1]) - 1, 0, -1)]
        return right + left + down + up

    @staticmethod
    def bishop_pot(location):
        """Bishop attacks"""
        location = list(location)
        right_up = [chr(y) + str(int(location[1]) + x) for x, y in enumerate(range(ord(location[0]) + 1, ord('i')), 1)
                    if 0 < int(location[1]) + x < 9]
        left_down = [chr(y) + str(int(location[1]) - x) for x, y in
                     enumerate(range(ord(location[0]) - 1, ord(chr(96)), -1), 1)
                     if 0 < int(location[1]) - x < 9]
        left_up = [chr(y) + str(int(location[1]) + x) for x, y in
                   enumerate(range(ord(location[0]) - 1, ord(chr(96)), -1), 1)
                   if 0 < int(location[1]) + x < 9]
        right_down = [chr(y) + str(int(location[1]) - x) for x, y in enumerate(range(ord(location[0]) + 1, ord('i')), 1)
                      if 0 < int(location[1]) - x < 9]
        return right_up + left_down + left_up + left_down + right_down

    @staticmethod
    def queen_pot(location):
        """Queen attacks"""
        location = list(location)
        right = [chr(x) + str(location[1]) for x in range(ord(location[0]) + 1, ord('i'))]
        left = [chr(x) + str(location[1]) for x in range(ord(location[0]) - 1, ord(chr(96)), -1)]
        up = [location[0] + str(x) for x in range(int(location[1]) + 1, 9)]
        down = [location[0] + str(x) for x in range(int(location[1]) - 1, 0, -1)]
        right_up = [chr(y) + str(int(location[1]) + x) for x, y in enumerate(range(ord(location[0]) + 1, ord('i')), 1)
                    if 0 < int(location[1]) + x < 9]
        left_down = [chr(y) + str(int(location[1]) - x) for x, y in
                     enumerate(range(ord(location[0]) - 1, ord(chr(96)), -1), 1)
                     if 0 < int(location[1]) - x < 9]
        left_up = [chr(y) + str(int(location[1]) + x) for x, y in
                   enumerate(range(ord(location[0]) - 1, ord(chr(96)), -1), 1)
                   if 0 < int(location[1]) + x < 9]
        right_down = [chr(y) + str(int(location[1]) - x) for x, y in enumerate(range(ord(location[0]) + 1, ord('i')), 1)
                      if 0 < int(location[1]) - x < 9]
        return right + left + down + up + right_up + left_down + left_up + left_down + right_down

    @staticmethod
    def king_pot(location):
        """King attacks"""
        location = list(location)
        up = location[0] + str(int(location[1]) + 1)
        down = location[0] + str(int(location[1]) - 1)
        right = chr(ord(location[0]) + 1) + str(location[1])
        left = chr(ord(location[0]) - 1) + str(location[1])
        left_up = chr(ord(location[0]) - 1) + str(int(location[1]) + 1)
        right_up = chr(ord(location[0]) + 1) + str(int(location[1]) + 1)
        left_down = chr(ord(location[0]) - 1) + str(int(location[1]) - 1)
        right_down = chr(ord(location[0]) + 1) + str(int(location[1]) - 1)

        return [x for x in (up, down, right, left, left_up, right_up, left_down, right_down)
                if ord(chr(96)) < ord(x[0]) < ord('i') and 0 < int(x[1]) < 9]

    @staticmethod
    def real_attacks(piece):
        """All attack vectors, taking in concern location of other pieces"""
        with redirect_stdout(None):
            if isinstance(piece, Pawn):
                pawn = list(filter_except(lambda z: piece.attack(piece.x + str(piece.y), z),
                                          PotentialAttack.pawn_pot(piece.location), BaseException))
                return pawn
            elif isinstance(piece, Knight):
                knight = list(filter_except(lambda z: piece.move(piece.x + str(piece.y), z),
                                            PotentialAttack.knight_pot(piece.location), BaseException))
                return knight
            elif isinstance(piece, Bishop):
                bishop = list(filter_except(lambda z: piece.move(piece.x + str(piece.y), z),
                                            PotentialAttack.bishop_pot(piece.location), BaseException))
                return bishop
            elif isinstance(piece, Rook):
                rook = list(filter_except(lambda z: piece.move(piece.x + str(piece.y), z),
                                          PotentialAttack.rook_pot(piece.location), BaseException))
                return rook
            elif isinstance(piece, Queen):
                queen = list(filter_except(lambda z: piece.move(piece.x + str(piece.y), z),
                                           PotentialAttack.queen_pot(piece.location), BaseException))
                return queen
            elif isinstance(piece, King):
                king = list(filter_except(lambda z: piece.move(piece.x + str(piece.y), z),
                                          PotentialAttack.king_pot(piece.location), BaseException))
                return king

    @staticmethod
    def all_for_all():
        """All attack vectors for all """
        if turn[1] % 2 == 0:
            all_pieces_attack = set(
                chain(*map(lambda x: PotentialAttack.real_attacks(x) if x != 'white' else '', w.__dict__.values()))
            )
        else:
            all_pieces_attack = set(
                chain(*map(lambda x: PotentialAttack.real_attacks(x) if x != 'black' else '', b.__dict__.values()))
            )
        return all_pieces_attack


class Game:
    """Game class"""

    @staticmethod
    def castle(one, two, obj):
        """Castling"""
        starter, finisher = obj.__dict__[save[one][1]], obj.__dict__[save[two][1]]
        # Check if both has never moved and if it's true - castle
        if starter.static and finisher.static:
            # If a king starts castling switch him with rook for simplicity
            if starter.__class__ is King:
                starter, finisher = finisher, starter
                one, two = two, one
            starter.location = (one, two, obj)
            starter.static = finisher.static = False
        else:
            print('One of your pieces has already moved!')
            raise BaseException

    @staticmethod
    def move(one, two, obj):
        """Move"""
        starter = obj.__dict__[save[one][1]]
        if starter.__class__ is King or starter.__class__ is Rook:
            starter.static = False
        starter.location = (one, two, obj)

    @staticmethod
    @Chessboard.chessboard
    @Chessboard.self_checker
    def chess_move(one, two):
        """Ходим фигурой"""
        if turn[1] % 2 != 0:
            obj = w
            # Castling conditions on a chessboard for whites
            if save[one][0] == 'K' and save[two][0] == 'R' or save[one][0] == 'R' and save[two][0] == 'K':
                Game.castle(one, two, obj)
            # Simple move or attack
            elif save[two] == '-':
                Game.move(one, two, obj)
                return True
            elif str(save[two][0]).islower():
                del b.__dict__[save[two][1]]
                Game.move(one, two, obj)
                return True
            else:
                print('Wrong move!')
                raise BaseException
        else:
            obj = b
            # Castling conditions on a chessboard for whites
            if save[one][0] == 'k' and save[two][0] == 'r' or save[one][0] == 'r' and save[two][0] == 'k':
                Game.castle(one, two, obj)
            # Simple move or attack
            elif save[two] == '-':
                Game.move(one, two, obj)
                return True
            elif str(save[two][0]).isupper():
                del w.__dict__[save[two][1]]
                Game.move(one, two, obj)
                return True
            else:
                print('Wrong move!')
                raise BaseException


w = WhitePieces()
b = BlackPieces()

q = False
turn[0] += 1

while q is False:
    if turn[1] % 2 != 0:
        glob_color = 'White'
        # All king moves (for checkmate)
        kings_moves = set(PotentialAttack.real_attacks(w.k))
        # King's location (for check)
        kings_location = w.k.x + str(w.k.y)
        color = 'white'
    else:
        glob_color = 'Black'
        kings_moves = set(PotentialAttack.real_attacks(b.k))
        kings_location = b.k.x + str(b.k.y)
        color = 'black'

    print(f'+++++++++++Turn №{turn[0]}+++++++++++')
    print()
    if turn[0] < 2 and turn[1] < 2:
        Chessboard.show_chessboard(turn[0])
        print()
    print(f'==========Turn {glob_color}==========')
    print()
    # Find out all opponent's attack vectors
    check_squares = PotentialAttack.all_for_all()
    # If all king's moves are impossible - it's a checkmate
    kings_moves -= check_squares
    while True:
        try:
            if len(kings_moves) == 0:
                print(f'Checkmate a {color} king at the turn number {turn[0]}!!')
                q = True
                break
            elif kings_location not in check_squares:
                start = input('Enter the starting point (letter then integer): ').strip().lower()
                finish = input('Enter the finishing point (letter then integer): ').strip().lower()
                Game.chess_move(start, finish)
                Chessboard.show_chessboard(turn[0])
                turn[1] += 1
                turn[0] = turn[0] + 1 if color == 'black' else turn[0] + 0
                break
            else:
                print(f'Check a {color} king!')
                start = input('Enter the starting point (letter then integer): ').strip().lower()
                finish = input('Enter the finishing point (letter then integer): ').strip().lower()
                if finish not in check_squares:
                    Game.chess_move(start, finish)
                    Chessboard.show_chessboard(turn[0])
                    turn[1] += 1
                    turn[0] = turn[0] + 1 if color == 'black' else turn[0] + 0
                    break
                else:
                    print("Check one more time!")
        except BaseException as e:
            print(e)
