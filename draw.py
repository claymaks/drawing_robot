"""
This script creates a two-link robot that draws an image passed through the command line

Invocations should conform to the following structure:
`usage: python3 draw.py [-h] [--image IMAGE_PATH]`
"""
import sys
import argparse

import pygame
import cv2

from src import env
from src.robots import Pen
from linedraw import linedraw

environment = env.BuildEnvironment()

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


def draw_image(image):
    Pen.max_speed = 10
    bound = int(environment.robot.radius * (2 ** 0.5) / 2)

    original = cv2.imread(image)
    if original is None:
        raise FileNotFoundError(f"Image '{image}' not found.")
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


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", dest="image")
    args = parser.parse_args(argv)
    draw_image(args.image)

if __name__ == "__main__":
    main(sys.argv[1:])
