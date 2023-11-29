import os
import keyboard
from random import randint, sample

"""
Необходимо реализовать игру «Ловкий муравьед».
Главный герой – голодный, но очень ловкий муравьед бегает по двумерному полю от
одного муравейника к другому и вылавливает убегающих за границу экрана муравьёв.
Необходимо реализовать консольное приложение-игру с текстовым
псевдографическим интерфейсом (графика может быть реализована при помощи
любых текстовых и псевдографических символов). Пользователь должен управлять
объектом-муравьедом, перемещаемым по двумерному полю (с препятствиями).
Управляемый объект обладает способностью поедать объекты муравьёв,
появляющихся из объектов-муравейников, разбросанных на поле. При появлении
муравьи хаотично перемещаются по полю. Если муравей соприкасается с границей
поля, то он считается упущенным и пропадает с поля. От соприкосновения муравьеда
с муравьём – последний исчезает, а игроку начисляется 1 балл. Муравейники на поле
размещаются случайным образом в количестве до 4 штук. В каждом муравейнике
могут прятаться до 10 муравьёв. Как только на поле все муравьи оказываются съедены
или упущены, игра завершается. По завершению игры результаты игровой сессии
выводятся на экран.

муравей
муравьед
муравейник
поле
клетка поля
"""


ROWS = 10
COLUMNS = 10
CELL_IMAGE = '.'
PLAYER_IMAGE = 'P'
ANTHILL_IMAGE = 'A'
ANT_IMAGE = 'a'
UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'
ANTHILLS_MAX = 4
ANTHILLS_MIN = 4


class GameObject:
    ''' запретить создание экземпляра '''
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image


class Аnthill(GameObject):
    def __init__(self, x, y):
        self.image = ANTHILL_IMAGE
        super().__init__(x, y, self.image)


class FieldCell:
    def __init__(self, x: int, y: int) -> None:
        self.image = CELL_IMAGE
        self.x = x
        self.y = y
        self.content = None

    def draw(self) -> None:
        if self.content:
            print(self.content.image, end='')
        else:
            print(self.image, end='')


class Player(GameObject):
    def __init__(self, x=0, y=0) -> None:
        self.image = PLAYER_IMAGE
        super().__init__(x, y, self.image)


class Field:
    def __init__(self,
                 columns: int,
                 rows: int,
                 player: Player) -> None:
        self.columns = columns
        self.rows = rows
        self.player = player
        self.cells = []

    def move_player(self) -> None:
        event = keyboard.read_event()
        old_x = self.player.x
        old_y = self.player.y
        dy = 0
        dx = 0
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == RIGHT and self.player.x < self.columns - 1:
                dx += 1
            elif event.name == LEFT and self.player.x > 0:
                dx -= 1
            elif event.name == UP and self.player.y > 0:
                dy -= 1
            elif event.name == DOWN and self.player.y < self.rows - 1:
                dy += 1
            if not self.cells[self.player.y + dy][self.player.x + dx].content:
                self.player.y += dy
                self.player.x += dx
                self.cells[old_y][old_x].content = None

    def make_anthills(self) -> list:
        empty_cells = self.get_empty_cells()
        anthills_amount = randint(ANTHILLS_MIN, ANTHILLS_MAX)
        anthills_cells = sample(empty_cells, anthills_amount)
        anthills = []
        for cell in anthills_cells:
            anthill = Аnthill(cell.y, cell.x)
            cell.content = anthill
            anthills.append(anthill)
        return anthills

    def generate_field(self) -> None:
        self.cells = [
            [FieldCell(x, y) for x in range(self.columns)] for y in range(self.rows)
        ]
        self.cells[self.player.y][self.player.x].content = self.player

    def get_empty_cells(self):
        empty_cells = []
        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                if not self.cells[y][x].content:
                    empty_cells.append(self.cells[y][x])
        return empty_cells

    def draw_field(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.draw()
            print('')

    def update(self):
        self.cells[self.player.y][self.player.x].content = self.player


class Game:
    def __init__(self) -> None:
        self.player = Player(y=ROWS // 2,
                             x=COLUMNS // 2)
        self.field = Field(COLUMNS, ROWS, self.player)
        self.is_running = True

    def run(self) -> None:
        self.field.generate_field()
        self.field.make_anthills()
        while self.is_running:
            self.field.draw_field()
            self.field.move_player()
            self.field.update()
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')


game = Game()
game.run()
