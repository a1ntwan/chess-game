from contextlib import redirect_stdout
from more_itertools import filter_except
from itertools import product, chain
from functools import wraps

product = sorted(product('abcdefgh', '12345678'), key=lambda x: x[1], reverse=True)
save = {str(z + j): '-' for _, _ in enumerate(range(1, 65), 1) for z, j in product}
turn = [0, 1]


class Chessboard:

    @staticmethod
    def chessboard(func):
        """Декоратор шахматной доски"""

        @wraps(func)
        def wrapper(one, two):
            if len(one) == len(two) == 2 and one[0]:
                if one[0] == two[0] and one[1] == two[1]:
                    print('Вы стоите на месте!')
                    raise BaseException
                if (ord(one[0]) in range(ord('a'), ord('i')) and ord(two[0]) in range(ord('a'), ord('i'))) \
                        and (int(one[1]) in range(1, 9) and int(two[1]) in range(1, 9)):
                    return func(one, two)
                else:
                    print('Неправильные входные данные (буква старше "H" или цифра больше 8)')
                    raise BaseException
            else:
                print('Неправильные входные данные')
                raise BaseException

        return wrapper

    @staticmethod
    def self_checker(func):
        """Начинаем ход своей фигурой"""

        @wraps(func)
        def wrapper(one, two):
            if turn[1] % 2 != 0:
                if str(save[one][0]).islower() or save[one] == '-':
                    print('Выберите свою фигуру')
                    raise BaseException
                return func(one, two)
            else:
                if str(save[one][0]).isupper() or save[one] == '-':
                    print('Выберите свою фигуру')
                    raise BaseException
                return func(one, two)

        return wrapper

    @staticmethod
    def show_chessboard(num):
        """Вывод шахматной доски"""
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
    """"Этот класс описывает движение фигур"""

    def __init__(self, ini, logo, name):
        self.x, self.y = ini[0], int(ini[1])
        self.logo = logo
        self.name = name

    @property
    def location(self):
        """Это геттер месторасположения фигуры"""
        return self.x, int(self.y)

    @location.setter
    def location(self, value):
        """Это сеттер месторасположения фигуры с учетом: 1)размеров шахматной доски
            (Chessboard class), 2)обычного хода фигуры (метод move)"""
        one, two, obj = value[0], value[1], value[2]
        if obj.color == 'white':
            if w.__dict__[save[one][1]].move(one=one, two=two):
                self.x, self.y = two[0], two[1]
                # При атаке на черную фигуру удаляем объект и перемещаемся на его клетку
                if str(save[two][0]).islower():
                    del b.__dict__[save[two][1]]
                    save[two], save[one] = save[one], '-'
                # При обычном ходе или рокировке просто меняем местами фигуры
                else:
                    save[one], save[two] = save[two], save[one]
        else:
            if b.__dict__[save[one][1]].move(one=one, two=two):
                self.x, self.y = two[0], two[1]
                # При атаке на белую фигуру удаляем объект и перемещаемся на его клетку
                if str(save[two][0]).isupper():
                    del w.__dict__[save[two][1]]
                    save[two], save[one] = save[one], '-'
                # При обычном ходе или рокировке просто меняем местами фигуры
                else:
                    save[one], save[two] = save[two], save[one]


class Pawn(Move):
    """Это пешка, у нее есть:
            1) стандартный ход +
            2) ход на две клетки первым ходом +
            3) она ест +
            4) она становится любой фигурой достигнув другого конца доски +
    """

    def __init__(self, ini, logo, name):
        """Инициализация фигуры"""
        super().__init__(ini, logo, name)
        save[ini] = (self.logo, self.name)

    def move(self, one, two):
        """Обычный ход и ход на 2 клетки, если это первый ход.
        Превращение в любую фигуру, достигнув противоположного края доски"""
        # Первый ход
        if (one[1] == '2' or one[1] == '7') and (one[0] == two[0] and abs(int(two[1]) - int(one[1])) == 2):
            self.x, self.y = two[0], int(two[1])
            return self.x, self.y
        # Обычный ход
        elif str(self.logo).islower() and one[0] == two[0] and ord(one[1]) - ord(two[1]) == 1:
            self.x, self.y = two[0], int(two[1])
            return self.x, self.y
        elif str(self.logo).isupper() and one[0] == two[0] and ord(two[1]) - ord(one[1]) == 1:
            self.x, self.y = two[0], int(two[1])
            return self.x, self.y
        # Атака
        elif str(self.logo).isupper() and abs(ord(two[0]) - ord(one[0])) == 1 and ord(two[1]) - ord(one[1]) == 1:
            self.x, self.y = two[0], int(two[1])
            return self.x, self.y
        elif str(self.logo).islower() and abs(ord(two[0]) - ord(one[0])) == 1 and ord(one[1]) - ord(two[1]) == 1:
            self.x, self.y = two[0], int(two[1])
            return self.x, self.y
        else:
            print('Пешка так не ходит')
            raise BaseException

    def attack(self, one, two):
        """Дополнительный метод атаки для вычисления клеток которые может атаковать пешка"""
        if str(self.logo).isupper() and abs(ord(two[0]) - ord(one[0])) == 1 and ord(two[1]) - ord(one[1]) == 1:
            return True
        elif str(self.logo).islower() and abs(ord(two[0]) - ord(one[0])) == 1 and ord(one[1]) - ord(two[1]) == 1:
            return True


class Knight(Move):
    """Это конь, у него есть:
                1) стандартный ход +
                2) он ест +
    """

    def __init__(self, ini, logo, name):
        """Инициализация фигуры"""
        super().__init__(ini, logo, name)
        save[ini] = (self.logo, self.name)

    @staticmethod
    def move(one, two):
        """Ход коня без учета фигур на пути"""
        if (abs(ord(two[0]) - ord(one[0])) == 1 and abs(ord(two[1]) - ord(one[1])) == 2) \
                or (abs(ord(two[0]) - ord(one[0])) == 2 and abs(ord(two[1]) - ord(one[1])) == 1):
            return True
        print('Конь так не ходит')
        raise BaseException


class Rook(Move):
    """Это ладья, у нее есть:
                1) стандартный ход +
                2) рокировка с королем при условии, что никто никуда не ходил +
                3) она ест +
                4) не умеет перепрыгивать  через фигуры +
    """

    def __init__(self, ini, logo, name, static=True):
        """Инициализация фигуры"""
        super().__init__(ini, logo, name)
        self.static = static
        save[ini] = (self.logo, self.name)

    def move(self, one, two):
        """Ход ладьи с учетом стоящих на пути фигур"""
        if one[0] == two[0] and one[1] == two[1]:
            return True
        elif save[one] != '-' and save[one][1] != self.name:
            print('Ладья не умеет перепрыгивать через другие фигуры')
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
                print('Ладья так не ходит')
                raise BaseException


class Bishop(Move):
    """Это слон, у него есть:
                1) стандартный ход +
                2) он ест +
                3) не умеет перепрыгивать  через фигуры +
    """

    def __init__(self, ini, logo, name):
        """Инициализация фигуры"""
        super().__init__(ini, logo, name)
        save[ini] = (self.logo, self.name)

    def move(self, one, two):
        """Ход слона с учетем стоящих на пути фигур"""
        if one[0] == two[0] and one[1] == two[1]:
            return True
        elif save[one] != '-' and save[one][1] != self.name:
            print('Слон не умеет перепрыгивать через другие фигуры')
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
                print('Слон так не ходит')
                raise BaseException


class Queen(Move):
    """Это ферзь, у него есть:
                1) стандартный ход +
                2) он ест +
                3) не умеет перепрыгивать  через фигуры +
    """

    def __init__(self, ini, logo, name):
        """Инициализация фигуры"""
        super().__init__(ini, logo, name)
        save[ini] = (self.logo, self.name)

    def move(self, one, two):
        """Ход ферзя с учетом стоящих на пути фигур"""
        if one[0] == two[0] and one[1] == two[1]:
            return True
        elif save[one] != '-' and save[one][1] != self.name:
            print('Ферзь не умеет перепрыгивать через другие фигуры')
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
                print('Ферзь так не ходит')
                raise BaseException


class King(Move):
    """Это король, у него есть:
                1) стандартный ход +
                2) рокировка с ладьей, при условии, что никто никуда не ходил
                3) он ест +
                4) он не может ходить или есть на клетку, на которой ему будут угрожать +
    """

    def __init__(self, ini, logo, name, static=True):
        """Инициализация фигуры"""
        super().__init__(ini, logo, name)
        self.static = static
        save[ini] = (self.logo, self.name)

    @staticmethod
    def move(one, two):
        """Обычный ход короля"""
        if (ord(two[0]) == ord(one[0]) and abs(ord(two[1]) - ord(one[1])) == 1) \
                or (abs(ord(two[0]) - ord(one[0])) == 1 and abs(ord(two[1]) - ord(one[1])) <= 1):
            return True
        print('Король так не ходит')
        raise BaseException


class WhitePieces:
    """Месторасположение белых фигур"""

    def __init__(self):
        """Инициализация белых фигур"""
        self.color = 'white'
        # self.p1 = Pawn('a2', 'P', name='p1')
        self.p2 = Pawn('b6', 'P', name='p2')
        # self.p3 = Pawn('c2', 'P', name='p3')
        # self.p4 = Pawn('d2', 'P', name='p4')
        # self.p5 = Pawn('e2', 'P', name='p5')
        # self.p6 = Pawn('f2', 'P', name='p6')
        # self.p7 = Pawn('g2', 'P', name='p7')
        # self.p8 = Pawn('h2', 'P', name='p8')
        # self.r1 = Rook('a1', 'R', name='r1')
        # self.r2 = Rook('h1', 'R', name='r2')
        # self.kn1 = Knight('b1', 'N', name='kn1')
        # self.kn2 = Knight('g1', 'N', name='kn2')
        # self.b1 = Bishop('c1', 'B', name='b1')
        # self.b2 = Bishop('f1', 'B', name='b2')
        # self.q = Queen('d1', 'Q', name='q')
        self.k = King('e1', 'K', name='k')

    def delete(self, obj):
        """Удалить фигуру из класса"""
        del self.__dict__[obj]

    def append(self, ini, logo, name, cls, obj):
        """Добавить фигуру в класс при достижении пешкой противоположного  края доски"""
        if cls is Queen:
            self.__dict__[obj] = Queen(ini, logo, name)
        elif cls is Bishop:
            self.__dict__[obj] = Bishop(ini, logo, name)
        elif cls is Rook:
            self.__dict__[obj] = Rook(ini, logo, name)
        elif cls is Knight:
            self.__dict__[obj] = Knight(ini, logo, name)


class BlackPieces:
    """Месторасположение черных фигур"""

    def __init__(self):
        """Инициализация черных фигур"""
        self.color = 'black'
        # self.p1 = Pawn('a7', 'p', name='p1')
        # self.p2 = Pawn('b7', 'p', name='p2')
        # self.p3 = Pawn('c7', 'p', name='p3')
        self.p4 = Pawn('c2', 'p', name='p4')
        # self.p5 = Pawn('e7', 'p', name='p5')
        # self.p6 = Pawn('f7', 'p', name='p6')
        # self.p7 = Pawn('g7', 'p', name='p7')
        # self.p8 = Pawn('h7', 'p', name='p8')
        # self.r1 = Rook('a8', 'r', name='r1')
        # self.r2 = Rook('h8', 'r', name='r2')
        # self.kn1 = Knight('b8', 'n', name='kn1')
        # self.kn2 = Knight('g8', 'n', name='kn2')
        # self.b1 = Bishop('c8', 'b', name='b1')
        # self.b2 = Bishop('f8', 'b', name='b2')
        # self.q = Queen('d8', 'q', name='q')
        self.k = King('e8', 'k', name='k')

    def delete(self, obj):
        """Удалить фигуру из класса"""
        del self.__dict__[obj]

    def append(self, ini, logo, name, cls, obj):
        """Добавить фигуру в класс при достижении пешкой противоположного  края доски"""
        if cls is Queen:
            self.__dict__[obj] = Queen(ini, logo, name)
        elif cls is Bishop:
            self.__dict__[obj] = Bishop(ini, logo, name)
        elif cls is Rook:
            self.__dict__[obj] = Rook(ini, logo, name)
        elif cls is Knight:
            self.__dict__[obj] = Knight(ini, logo, name)


w = WhitePieces()
b = BlackPieces()


class PotentialAttack:
    """Находим все атаки всех фигур"""

    @staticmethod
    def pawn_pot(location):
        """Все клетки атаки пешки"""
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
        """Все клетки атаки коня"""
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
        """Все клетки атаки ладьи"""
        location = list(location)
        right = [chr(x) + str(location[1]) for x in range(ord(location[0]) + 1, ord('i'))]
        left = [chr(x) + str(location[1]) for x in range(ord(location[0]) - 1, ord(chr(96)), -1)]
        up = [location[0] + str(x) for x in range(int(location[1]) + 1, 9)]
        down = [location[0] + str(x) for x in range(int(location[1]) - 1, 0, -1)]
        return right + left + down + up

    @staticmethod
    def bishop_pot(location):
        """Все клетки атаки слона"""
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
        """Все клетки атаки ферзя"""
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
        """Все клетки атаки короля"""
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
        """Все клетки атаки любой фигуры в зависимости от реального положения фигур на доске"""
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
        """Находим все клетки атаки для всех фигур"""
        if turn[1] % 2 == 0:
            all_pieces_attack = set(
                chain(*map(lambda x: PotentialAttack.real_attacks(x) if x != 'white' else '', w.__dict__.values()))
            )
        else:
            all_pieces_attack = set(
                chain(*map(lambda x: PotentialAttack.real_attacks(x) if x != 'black' else '', b.__dict__.values()))
            )
        return all_pieces_attack