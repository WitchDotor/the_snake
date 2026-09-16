import random
from typing import List, Tuple

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER_WIDTH = SCREEN_WIDTH // 2
SCREEN_CENTER_HEIGHT = SCREEN_HEIGHT // 2
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    def __init__(self, body_color: Tuple[int, int, int] = (0, 0, 0),
                 position = (SCREEN_CENTER_WIDTH, SCREEN_CENTER_HEIGHT)):
        self.position = position
        self.body_color = body_color

    def reset(self):
        """Метод перезапуска объекта"""
        self.__init__(self)

    def draw(self):
        """Метод отрисовки, реализован в дочерних классах"""
        ...


class Apple(GameObject):
    """Класс яблока, которое собирает змейка."""

    def __init__(
        self,
        body_color: Tuple[int, int, int] = SNAKE_COLOR
    ):
        """Инициализирует яблоко.

        Args:
            position: Начальная позиция (не используется, задаётся случайно).
            body_color: Цвет яблока.
        """
        super().__init__(body_color)
        self.position = (
            random.randrange(20, SCREEN_WIDTH, GRID_SIZE),
            random.randrange(20, SCREEN_WIDTH, GRID_SIZE)
        )
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Устанавливает случайную позицию яблока на игровом поле."""
        new_position = (
            random.randrange(20, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE),
            random.randrange(20, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE)
        )
        self.position = new_position

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки, управляемой игроком."""

    def __init__(
        self,
        positions=None,
        body_color: Tuple[int, int, int]=SNAKE_COLOR,
    ):
        """Инициализирует змейку.

        Args:
            positions: Координаты тела змейки.
            body_color: Цвет тела змейки.
        """
        super().__init__(body_color)
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.length = 1
        self.next_direction = RIGHT
        self.last = False

    def reset(self):
        """Сбрасывает состояние змейки и очищает её сегменты на экране."""
        for i in self.positions:
            rect = pygame.Rect((i[0], i[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        super().reset()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for pos in self.positions[:-1]:
            float_pair_first = float(pos[0])
            float_pair_second = float(pos[1])
            rect = pygame.Rect(
                (float_pair_first, float_pair_second),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        float_pair_first = float(self.positions[0][0])
        float_pair_second = float(self.positions[0][1])
        head_rect = pygame.Rect(
            (float_pair_first, float_pair_second),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        coordinate_pair = self.positions.pop()
        float_pair_first = float(coordinate_pair[0])
        float_pair_second = float(coordinate_pair[1])
        last_rect = pygame.Rect(
            (float_pair_first, float_pair_second),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Перемещает змейку в текущем направлении."""
        new_x_coordinate = (
            self.positions[0][0] + self.next_direction[0] * GRID_SIZE
        )
        new_y_coordinate = (
            self.positions[0][1] + self.next_direction[1] * GRID_SIZE
        )
        if new_x_coordinate > SCREEN_WIDTH:
            new_x_coordinate = 0
        if new_x_coordinate < 0:
            new_x_coordinate = abs(SCREEN_WIDTH - new_x_coordinate)

        if new_y_coordinate > SCREEN_HEIGHT:
            new_y_coordinate = 0
        if new_y_coordinate < 0:
            new_y_coordinate = abs(SCREEN_HEIGHT - new_y_coordinate)

        new_positions = (new_x_coordinate, new_y_coordinate)
        self.positions.insert(0, new_positions)
        self.draw()

    def eat_apple(self, apple: GameObject):
        """Обрабатывает съедание яблока: удлиняет змейку.

        Args:
            apple: Съеденное яблоко.
        """
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
            self.reset()
        apple.position = None

    def check_self_eating(self):
        """Проверяет, не съела ли змейка себя, и сбрасывает игру."""
        if self.get_head_position() in self.positions[1:]:
            self.reset()

    def update_direction(self):
        """Обновляет направление движения после нажатия клавиши."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]


# Тут опишите все классы игры.
# Функция обработки действий пользователя
def handle_keys(game_object):
    """"Обработка нажатий клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP and game_object.direction != DOWN
                    and game_object.next_direction != DOWN):
                game_object.next_direction = UP
            elif (event.key == pygame.K_DOWN and game_object.direction != UP
                  and game_object.next_direction != UP):
                game_object.next_direction = DOWN
            elif (event.key == pygame.K_LEFT
                  and game_object.next_direction != RIGHT):
                game_object.next_direction = LEFT
            elif (event.key == pygame.K_RIGHT and game_object.direction != LEFT
                  and game_object.next_direction != LEFT):
                game_object.next_direction = RIGHT


# Метод обновления направления после нажатия на кнопку
def update_direction(self):
    """"Обновление направления змейки"""
    if self.next_direction:
        self.direction = self.next_direction
        self.next_direction = None


def main():
    """"Запуск логики игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.move()

        if snake.positions[0] == apple.position:
            snake.eat_apple(apple)

        if apple.position is None:
            apple.randomize_position()

        snake.check_self_eating()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
