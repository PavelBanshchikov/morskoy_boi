from random import randint

class Dot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

   

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

class BoardException(Exception):
    ...

class OutOfBoard(BoardException):
    def __str__(self):
        return "Вы пытатесь стрелять вне доски"

class UsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class WrongShip(BoardException):
    ...

class Ship:

    def __init__(self, length, direction, bow: Dot,  number_of_lives):
        self.length = length
        self.direction = direction
        self.number_of_lives = number_of_lives
        self.bow = bow

    def get_length(self):
        return self.length

    def get_direction(self):
        return self.direction

    def get_bow(self):
        return self.bow

    def get_number_of_lives(self):
        return self.number_of_lives

    @property
    def dots(self):
        dots_list = []
        for i in range(self.length):
            x = self.bow.x
            y = self.bow.y

            if self.direction == 0:
                x += i

            elif self.direction == 1:
                y += i

            dots_list.append(Dot(x, y))

        return dots_list


class Board:

    def __init__(self, hid = False):
        self.field = [['0' for a in range(6)] for i in range(6)]
        self.hid = hid
        self.ships = []
        self.dead_ships = 0
        self.busy = []

    def add_ship(self, ship: Ship):
        for i in ship.dots:
            if self.out(i) or i in self.busy:
                raise WrongShip
            else:
                self.field[i.get_x()][i.get_y()] = 's'
                self.busy.append(i)
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship: Ship, hid = True ):

        ship_contour = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1,-1), (0,-1), (1,-1)]
        for i in ship.dots:
            for a,b in ship_contour:
                dot = Dot(i.get_x() + a, i.get_y() + b)
                if dot not in self.busy and not self.out(dot):
                    if not hid:
                        self.field[dot.get_x()][dot.get_y()] = '*'
                    self.busy.append(dot)

    def __str__(self):
        board = '     0 | 1 | 2 | 3 | 4 | 5 |'
        for i in range(6):
            board += f'\n {i} | ' + ' | '.join(self.field[i]) + ' |'
        if self.hid:
            board.replace('s', '0')
        return board

    def out(self, dot: Dot):
        if dot.get_y() < 0 or dot.get_y() > 5 or dot.get_x() < 0 or dot.get_x() > 5:
            return True
        else:
            return False

    def shot(self, dot:Dot):
        self.busy.append(dot)
        if self.out(dot):
            raise OutOfBoard
        if dot in self.busy:
            raise UsedException
        for ship in self.ships:
            if d in ship.dots:
                ship.number_of_lives -= 1
                self.field[dot.get_x()][dot.get_y()] = 'X'
                if ship.number_of_lives == 0:
                    print('Корабль уничтожен')
                    self.contour(ship, hid = False)
                    self.dead_ships += 1
                    return False
                else:
                    print('Корабль ранен')
                    return True
        print('Промах')
        self.field[dot.get_x()][dot.get_y()] = '*'
        return False
    def begin(self):
        self.busy = []

class Player:

    def __init__(self, my_board: Board, other_board: Board):
        self.my_board = my_board
        self.other_board = other_board

    def ask(self):
        ...

    def move(self):
        while True:
            try:
                shot = self.ask()
                repeat = self.other_board.shot(shot)
                return repeat
            except BoardException as error:
                print(error)

class User(Player):

    def ask(self):
        while True:
            ask_split = input('Введите координаты через пробел: ').split
            if len(ask_split) != 2:
                print('Введите 2 числа')
                continue

            x = ask_split[0]
            y = ask_split[1]

            if not (x.isdigit() and y.isdigit()):
                print('Введите 2 числа')
                continue

            x = int(x)
            y = int(y)

            return Dot(x,y)

class AI(Player):
    def ask(self):
        dot = Dot(randint(0,5), randint(0,5))
        print(f'Ход компьютера: {dot.get_x()},{dot.get_y()}')
        return dot

class Game:
    def __init__(self):
        board1 = self.random_board()
        board2 = self.random_board()
        board2.hid = True
        self.user = User(board1, board2)
        self.ai = AI(board2, board1)

    def random_place(self):
        lenghts = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        attemps = 0
        for i in lenghts:
            attemps += 1
            while True:
                ship = Ship(length = i, direction = randint(0,1), bow = Dot(randint(0,5), randint(0,5)),  number_of_lives = i)
                try:
                    board.add_ship(ship)
                    break
                except WrongShip:
                    ...
                if attemps >= 3000:
                    return None
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def greet(self):
        print('---------Формат ввода: x,y---------')
        print('x - номер строки, y - номер столбца')
        print('-----------------------------------')

    def loop(self):
        cnt = 0
        while True:
            print('Доска пользоваьеля:')
            print(self.user.my_board)
            print('-----------------------------------')
            print('Доска компьютера:')
            print(self.ai.my_board)
            if cnt %2 == 0:
                print('Ходит пользователь')
                repeat = self.user.move()
            else:
                print('Ходит компьютер')
                repeat = self.ai.move()

            if repeat:
                cnt -= 1

            if self.ai.my_board.dead_ships == 7:
                print('Пользователь выиграл')
                break

            if self.user.my_board.dead_ships == 7:
                print('Компьютер выиграл')
                break

            cnt +=1

    def start(self):
        self.greet()
        self.loop()

game = Game()
game.start()














board = Board(False)
ship = Ship(3, 'v', Dot(1,2), 3)
print(ship.dots)
board.add_ship(ship)
print(board)



