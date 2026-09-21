import pygame as pg

import random
import sys
from typing import Tuple, List

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER_WIDTH = SCREEN_WIDTH // 2
SCREEN_CENTER_HEIGHT = SCREEN_HEIGHT // 2
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_CENTER_WIDTH, SCREEN_CENTER_HEIGHT)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

USED_COLORS = {
    'RED': (255, 0, 0),
    'BLACK': (0, 0, 0),
    'GREEN': (0, 255, 0),
    'LIGHT_BLUE': (93, 216, 228)
}
BOARD_BACKGROUND_COLOR = USED_COLORS['BLACK']

BORDER_COLOR = USED_COLORS['LIGHT_BLUE']

APPLE_COLOR = USED_COLORS['RED']

SNAKE_COLOR = USED_COLORS['GREEN']

SPEED = 5

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pg.display.set_caption('Змейка')

clock = pg.time.Clock()


class GameObject:
    """Анонимный класс для игровых объектов"""

    def __init__(self, body_color: Tuple[int, int, int] = USED_COLORS['BLACK'],
                 position: Tuple[int, int] = CENTER_POSITION):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки, должен быть реализован в дочерних классах"""
        class_name = self.__class__.__name__
        message = f'Метод draw класса {class_name} должен быть реализован '
        raise NotImplementedError(message)

    def draw_rect(self, position: Tuple[int, int] = (0, 0),
                  color: Tuple[int, int, int] = None,
                  with_border=False):
        """Отрисовывает квадрат на экране. Если color == None, берется color = self.body_color. Необходим для переиспользования в методе draw()"""
        if color is None:
            color = self.body_color
        x_pos = float(position[0])
        y_pos = float(position[1])
        rect = pg.Rect(
            (x_pos, y_pos),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(screen, color, rect)
        if with_border:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблока, которое собирает змейка."""

    def __init__(
            self,
            position=(0, 0),
            body_color: Tuple[int, int, int] = APPLE_COLOR
    ):
        """Инициализирует яблоко.

        Args:
            position: Начальная позиция (не используется, задаётся случайно).
            body_color: Цвет яблока.
        """
        super().__init__(body_color, position)

    def randomize_position(self, filled_positions: List[Tuple[int, int]]):
        """Устанавливает случайную позицию яблока на игровом поле."""
        new_position = (
            random.randrange(20, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE),
            random.randrange(20, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE)
        )
        if new_position is not filled_positions:
            self.position = new_position
        else:
            self.randomize_position(filled_positions)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        self.draw_rect(position=self.position, with_border=True)


class Snake(GameObject):
    """Класс змейки, управляемой игроком."""

    def __init__(
            self,
            body_color: Tuple[int, int, int] = SNAKE_COLOR,
    ):
        """Инициализирует змейку.

        Args:
            positions: Координаты тела змейки.
            body_color: Цвет тела змейки.
        """
        super().__init__(body_color)
        self.positions = [self.position]
        self.direction = RIGHT
        self.length = 1
        self.next_direction = RIGHT
        self.last = False

    def erase_last_segment(self):
        """Затирание последнего сегмента"""
        if len(self.positions) > 1:
            last_rect = pg.Rect(
                self.positions.pop(),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def draw(self):
        """Отрисовывает змейку на экране."""
        self.draw_rect(position=self.get_head_position(), with_border=True)
        self.erase_last_segment()

    def reset(self):
        """Сбрасывает состояние змейки и очищает её сегменты на экране."""
        for _ in self.positions[0:]:
            self.erase_last_segment()
        self.__init__(self.body_color)

    def move(self):
        """Перемещает змейку в текущем направлении."""
        new_x_coordinate = (
            (self.positions[0][0] + self.next_direction[0] * GRID_SIZE)
            % SCREEN_WIDTH
        )
        new_y_coordinate = (
            (self.positions[0][1] + self.next_direction[1] * GRID_SIZE)
            % SCREEN_HEIGHT
        )
        new_positions = (new_x_coordinate, new_y_coordinate)
        self.positions.insert(0, new_positions)

    def grow(self):
        """Удлиняет змейку на 1 сегмент"""
        last_coordinate = self.positions[len(self.positions) - 1]
        if self.direction == UP:
            x_coordinate = last_coordinate[0] + DOWN[0] * GRID_SIZE
            y_coordinate = last_coordinate[1] + DOWN[1] * GRID_SIZE
            self.positions.append((x_coordinate, y_coordinate))
        elif DOWN:
            x_coordinate = last_coordinate[0] + UP[0] * GRID_SIZE
            y_coordinate = last_coordinate[1] + UP[1] * GRID_SIZE
            self.positions.append((x_coordinate, y_coordinate))
        elif RIGHT:
            x_coordinate = last_coordinate[0] + LEFT[0] * GRID_SIZE
            y_coordinate = last_coordinate[1] + LEFT[1] * GRID_SIZE
            self.positions.append((x_coordinate, y_coordinate))
        elif LEFT:
            x_coordinate = last_coordinate[0] + RIGHT[0] * GRID_SIZE
            y_coordinate = last_coordinate[1] + RIGHT[1] * GRID_SIZE
            self.positions.append((x_coordinate, y_coordinate))
        else:
            pass

    def check_self_eating(self) -> bool:
        """Проверяет, не съела ли змейка себя, и сбрасывает игру."""
        if self.get_head_position() in self.positions[1:]:
            self.reset()
            return True
        return False

    def update_direction(self):
        """Обновляет направление движения после нажатия клавиши."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]


def handle_keys(game_object):
    """Обработка нажатий клавиш"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if (event.key == pg.K_UP and game_object.direction != DOWN
                    and game_object.next_direction != DOWN):
                game_object.next_direction = UP
            elif (event.key == pg.K_DOWN and game_object.direction != UP
                  and game_object.next_direction != UP):
                game_object.next_direction = DOWN
            elif (event.key == pg.K_LEFT
                  and game_object.next_direction != RIGHT):
                game_object.next_direction = LEFT
            elif (event.key == pg.K_RIGHT and game_object.direction != LEFT
                  and game_object.next_direction != LEFT):
                game_object.next_direction = RIGHT


def main():
    """Запуск логики игры"""
    pg.init()
    apple = Apple(position=(0, 0))
    apple.randomize_position(filled_positions=[CENTER_POSITION])
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        snake.draw()
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(filled_positions=snake.positions)

        if snake.check_self_eating() and apple.position == CENTER_POSITION:
            apple.randomize_position(snake.positions)
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
