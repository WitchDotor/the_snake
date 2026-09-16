from cgitb import reset
from random import choice, randint

import pygame
import Classes
from Constants import UP, DOWN, RIGHT, LEFT, clock, SPEED



# Тут опишите все классы игры.
# Функция обработки действий пользователя
def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN and game_object.next_direction !=DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP and game_object.next_direction !=UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT  and game_object.next_direction !=RIGHT:
               #and game_object.direction != RIGHT
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT and game_object.next_direction !=LEFT:
                game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
def update_direction(self):
    if self.next_direction:
        self.direction = self.next_direction
        self.next_direction = None


def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Classes.Snake()
    apple = Classes.Apple()

    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.move()

        if snake.position[0] == apple.position:
            snake.eat_apple(apple)

        if apple.position is None:
            apple.randomize_position()

        snake.check_self_eating()
        apple.draw()

        pygame.display.update()

if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)