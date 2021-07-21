import math

import pygame

from src import env
from src.robots import Pen

RESOLUTION = 1

environment = env.BuildEnvironment()


def bind(val, _min, _max):
    return min(max(_min, val), _max)


def update(visual=True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    environment.render_map()
    if visual:
        pygame.display.update()


def wait_update(robot, coords, visual=True):
    robot.move_to_pos(coords)
    while not robot.at_target:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        robot.move_to_pos(coords)
        environment.render_map()

        if visual:
            pygame.display.update()


def circles():
    environment.robot.drawing = True
    for i in range(4):
        for j in range(360 * RESOLUTION):
            environment.robot.angle['joint_2'] += math.radians(1 / RESOLUTION)
            update()

        for j in range(90 * RESOLUTION):
            environment.robot.angle['joint_1'] += math.radians(1 / RESOLUTION)
            update()


def lag():
    environment.robot.drawing = True
    for i in range(120):
        for j in range(360 * RESOLUTION):
            environment.robot.angle['joint_1'] += math.radians(1 / RESOLUTION)
            environment.robot.angle['joint_2'] -= math.radians(1.01 / RESOLUTION)
            update(visual=False)
        print(i)
        if i % 30 == 0:
            update()
    update()


def flower():
    def petal_1():
        for i in range(45 * RESOLUTION):
            environment.robot.angle['joint_1'] -= math.radians(0.33 / RESOLUTION)
            environment.robot.angle['joint_2'] += math.radians(1 / RESOLUTION)
            update()
        for i in range(45 * RESOLUTION):
            environment.robot.angle['joint_1'] -= math.radians(.11 / RESOLUTION)
            environment.robot.angle['joint_2'] += math.radians(1 / RESOLUTION)
            update()
        for i in range(45 * RESOLUTION):
            environment.robot.angle['joint_1'] += math.radians(.11 / RESOLUTION)
            environment.robot.angle['joint_2'] -= math.radians(1 / RESOLUTION)
            update()
        for i in range(45 * RESOLUTION):
            environment.robot.angle['joint_1'] += math.radians(0.33 / RESOLUTION)
            environment.robot.angle['joint_2'] -= math.radians(1 / RESOLUTION)
            update()

    def petal_2():
        for i in range(45 * RESOLUTION):
            environment.robot.angle['joint_1'] += math.radians(0.33 / RESOLUTION)
            environment.robot.angle['joint_2'] -= math.radians(1 / RESOLUTION)
            update()
        for i in range(45 * RESOLUTION):
            environment.robot.angle['joint_1'] += math.radians(.11 / RESOLUTION)
            environment.robot.angle['joint_2'] -= math.radians(1 / RESOLUTION)
            update()
        for i in range(45 * RESOLUTION):
            environment.robot.angle['joint_1'] -= math.radians(.11 / RESOLUTION)
            environment.robot.angle['joint_2'] += math.radians(1 / RESOLUTION)
            update()
        for i in range(45 * RESOLUTION):
            environment.robot.angle['joint_1'] -= math.radians(0.33 / RESOLUTION)
            environment.robot.angle['joint_2'] += math.radians(1 / RESOLUTION)
            update()

    def flip(degree=230, amount=1.00091):
        for i in range(degree * RESOLUTION):
            environment.robot.angle['joint_1'] += math.radians(amount / RESOLUTION)
            update()

    environment.robot.angle['joint_2'] = math.radians(180)
    environment.robot.angle['joint_1'] = math.radians(64.8)
    update()
    environment.robot.drawing = True

    for i in range(8):
        petal_1()
        flip()
        petal_2()
        flip(degree=5, amount=-1)

    environment.robot.drawing = False
    for i in range(12 * RESOLUTION):
        environment.robot.angle['joint_2'] += math.radians(1 / RESOLUTION)
        update()

    environment.robot.drawing = True
    for i in range(360 * 4 * RESOLUTION):
        environment.robot.angle['joint_1'] += math.radians(1 / RESOLUTION)
        environment.robot.angle['joint_2'] -= math.radians((3 / 360) / RESOLUTION)
        update()


def random_lines():
    from random import randint
    (r, g, b) = (randint(0, 225), randint(0, 225), randint(0, 225))
    (dr, dg, db) = (0, 0, 0)

    bound = int(environment.robot.radius * (2 ** 0.5) / 2)
    environment.robot.drawing = False
    for y in range(-bound, bound, 10):
        environment.robot.goto_pos((-bound, y))
        update()
        environment.robot.drawing = True
        for x in range(-bound + 5, bound, 10):
            (dr, dg, db) = (randint(-100, 100), randint(-100, 100), randint(-100, 100))
            environment.robot.color = tuple(map(lambda c: bind(c, 0, 225), (r + dr, g + dg, b + db)))
            print(environment.robot.color)
            environment.robot.goto_pos((x, y + randint(-5, 5)))
            update()
        environment.robot.drawing = False
        update()


def face():
    import cv2
    from linedraw import linedraw

    Pen.max_speed = 10
    bound = int(environment.robot.radius * (2 ** 0.5) / 2)
    original = cv2.imread("images/face.jpeg")
    modifier = bound / max(original.shape[:2])

    img = cv2.resize(original, (int(modifier * original.shape[0]), int(modifier * original.shape[1])),
                     interpolation=cv2.INTER_AREA)
    lines = linedraw._sketch(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    environment.robot.drawing = False
    for line in lines:
        wait_update(environment.robot, (line[0][0] - bound, line[0][1] - bound))
        environment.robot.drawing = True
        for point in line[1:]:
            wait_update(environment.robot, (point[0] - bound, point[1] - bound))
        environment.robot.drawing = False
        update()


if __name__ == "__main__":
    random_lines()
    environment.map.blit(environment.robot.map, (0, 0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        pygame.display.update()
