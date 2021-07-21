"""Environment for robot simulation."""
import pygame

from src.robots import Pen
from src.constants import *


class BuildEnvironment(object):
    def __init__(self, urdf_file="src/robot.xml", dimensions=(1200, 700), scale=(1 / 2)):
        self.robot = Pen(urdf_file, scale)
        pygame.init()
        self.w, self.h = dimensions
        self.map = pygame.display.set_mode(dimensions)
        pygame.display.update()

    def render_map(self):
        self.map.fill(WHITE)
        virtual_map = self.map.copy()
        self.robot.animate(virtual_map, offset=(self.w // 2, self.h // 2))
        self.map.blit(virtual_map, (0, 0))
