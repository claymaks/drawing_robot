import math

import pygame

from src import env

D_ALPHA = math.radians(0.1)

environment = env.BuildEnvironment()

if __name__ == "__main__":
    running = True
    toggle = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            environment.robot.angle['joint_1'] += D_ALPHA
        elif keys[pygame.K_q]:
            environment.robot.angle['joint_1'] -= D_ALPHA

        if keys[pygame.K_d]:
            environment.robot.angle['joint_2'] += D_ALPHA
        elif keys[pygame.K_a]:
            environment.robot.angle['joint_2'] -= D_ALPHA

        if keys[pygame.K_SPACE] and not toggle:
            toggle = True
            environment.robot.drawing = not environment.robot.drawing
        elif not keys[pygame.K_SPACE] and toggle:
            toggle = False

        if keys[pygame.K_o]:
            environment.robot.angle['joint_1'] += 10 * D_ALPHA
        elif keys[pygame.K_u]:
            environment.robot.angle['joint_1'] -= 10 * D_ALPHA

        if keys[pygame.K_l]:
            environment.robot.angle['joint_2'] += 10 * D_ALPHA
        elif keys[pygame.K_j]:
            environment.robot.angle['joint_2'] -= 10 * D_ALPHA

        if keys[pygame.K_SPACE] and not toggle:
            toggle = True
            environment.robot.drawing = not environment.robot.drawing
        elif not keys[pygame.K_SPACE] and toggle:
            toggle = False

        environment.render_map()
        pygame.display.update()
    pygame.quit()
