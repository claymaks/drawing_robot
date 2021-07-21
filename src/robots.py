import math

import numpy as np
import pygame

from src.robot import Robot
from src.constants import BLACK


def center(coords):
    x, y = zip(*coords)
    return (sum(x) / len(x), sum(y) / len(y))


def pythag(coord):
    return (coord[0] * coord[0] + coord[1] * coord[1]) ** 0.5


def theta1(x, y, l1, l2, theta2):
    return math.atan2(y, x) - math.atan2((l2 * math.sin(theta2)), (l1 + l2 * math.cos(theta2)))


def theta2(x, y, l1, l2):
    return math.acos((x ** 2 + y ** 2 - l1 ** 2 - l2 ** 2) / (2 * l1 * l2))


class Pen(Robot):
    accel = 1
    max_speed = 5

    def __init__(self, filename, scale, color=BLACK):
        super().__init__(filename, scale)
        self.radius = center(self.coordinates('pen', np.array((0, 0))))[0]
        self.segment_lengths = [
            self.joints['joint_2']['xyz'][0] * scale,
            self.radius - (self.joints['joint_2']['xyz'][0] * scale)
        ]

        self.cur_coords = np.array([self.radius, 0])
        self.target_coords = np.array([self.radius, 0])
        self.velocity = 0

        self.color = color
        self.drawing = False
        self.map = None
        self.prev_coords = None

    @property
    def at_target(self):
        return (self.cur_coords == self.target_coords).all()

    def move_to_pos(self, _coord, _center=(0, 0)):
        coord = np.array(_coord, dtype=np.float64)
        center = np.array(_center, dtype=np.float64)

        self.target_coords = coord - center
        difference = self.target_coords - self.cur_coords
        distance = pythag(difference)

        self.cur_coords += self.velocity * difference / np.linalg.norm(difference)

        self.goto_pos(self.cur_coords)
        if distance < self.velocity ** 2 / (2 * Pen.accel):
            self.velocity -= Pen.accel
        else:
            self.velocity += Pen.accel
        self.velocity = max(min(Pen.max_speed, self.velocity), -Pen.max_speed)

        if distance < 3:
            self.cur_coords = self.target_coords
            self.goto_pos(self.cur_coords, (0, 0))

    def goto_pos(self, coord, center=(0, 0)):
        coord = np.array(coord)
        center = np.array(center)
        working_coord = coord - center
        combined_angle = math.atan2(*working_coord[::-1])

        if pythag(coord - center) > self.radius:
            self.angle['joint_2'] = 0
            self.angle['joint_1'] = combined_angle
            return
        try:
            self.angle['joint_2'] = theta2(*working_coord, *self.segment_lengths)
        except ValueError:
            if coord[0] > self.radius / 2:
                self.angle['joint_2'] = 0
            else:
                self.angle['joint_2'] = math.radians(180)
        self.angle['joint_1'] = theta1(*working_coord, *self.segment_lengths, self.angle['joint_2'])

    def animate(self, surface, offset=(0, 0)):
        if self.map is None:
            self.map = surface.copy()

        if self.drawing:
            coord = center(self.coordinates('pen', np.array(offset)))
            if self.prev_coords is None:
                pygame.draw.circle(self.map, self.color, coord, 0.5)
            else:
                pygame.draw.line(self.map, self.color, center(self.prev_coords), coord)
            self.prev_coords = self.coordinates('pen', np.array(offset))
        else:
            self.prev_coords = None

        surface.blit(self.map, (0, 0))
        super().animate(surface, offset)
