import math

import pygame

from src import env

D_ALPHA = math.radians(0.1)

environment = env.BuildEnvironment()
running = True
toggle = False

if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        environment.robot.drawing = pygame.mouse.get_pressed(3)[0]
        environment.robot.move_to_pos(pygame.mouse.get_pos(),
                                      (environment.w // 2, environment.h // 2))

        environment.render_map()
        pygame.display.update()
    pygame.quit()
