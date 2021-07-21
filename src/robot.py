import math

import pygame
import numpy as np
from urdf_parser_py.urdf import URDF, Joint, Link

from src.quaternion import Q
from src.matrix import IDENTITY, generate_translation_rotation


class Robot(object):
    def __init__(self, filename, scale=1):
        self.robot = URDF.from_xml_file(filename)
        self.xform = dict()
        self.angle = {
            name: 0 for name, joint in self.robot.joint_map.items()
        }
        self.joints = {
            name: {
                'parent': joint.parent,
                'child': joint.child,
                **joint.origin.__dict__,
            }
            for name, joint in self.robot.joint_map.items()
        }
        self.figures = {
            name: {
                'parent': self.robot.parent_map.get(name, [''])[0],
                'color': list(map(
                    lambda x: int(255 * x), link.visuals[0].material.color.rgba[:-1]
                )),
                'geometry': link.visuals[0].geometry.size,
                **link.visuals[0].origin.__dict__
            }
            for name, link in self.robot.link_map.items()
        }
        self.scale = scale
        self.buildFKTransforms()

    def coordinates(self, figure, offset=np.array([0, 0])):
        v = self.figures[figure]
        x_0, y_0 = v['xyz'][0], v['xyz'][1]
        x_1, y_1 = v['geometry'][0], v['geometry'][1]
        distance = ((x_1 / 2) ** 2 + (y_1 / 2) ** 2) ** .5

        base_coords = np.array([
            np.array([(x_0 + math.cos(math.atan2(-y_1 / 2, -x_1 / 2)) * distance),
                      (y_0 - math.sin(math.atan2(-y_1 / 2, -x_1 / 2)) * distance), 1, 1]),
            np.array([(x_0 + math.cos(math.atan2(y_1 / 2, -x_1 / 2)) * distance),
                      (y_0 - math.sin(math.atan2(y_1 / 2, -x_1 / 2)) * distance), 1, 1]),
            np.array([(x_0 + math.cos(math.atan2(y_1 / 2, x_1 / 2)) * distance),
                      (y_0 - math.sin(math.atan2(y_1 / 2, x_1 / 2)) * distance), 1, 1]),
            np.array([(x_0 + math.cos(math.atan2(-y_1 / 2, x_1 / 2)) * distance),
                      (y_0 - math.sin(math.atan2(-y_1 / 2, x_1 / 2)) * distance), 1, 1]),
        ])

        updated_coords = (
            offset + (self.scale * np.matmul(self.xform[figure], base_coords[0]))[:2],
            offset + (self.scale * np.matmul(self.xform[figure], base_coords[1]))[:2],
            offset + (self.scale * np.matmul(self.xform[figure], base_coords[2]))[:2],
            offset + (self.scale * np.matmul(self.xform[figure], base_coords[3]))[:2]
        )
        return updated_coords

    def animate(self, surface, offset=(0,0)):
        self.buildFKTransforms()
        for k, v in self.figures.items():
            pygame.draw.polygon(surface, v['color'], self.coordinates(k, np.array(offset)))

    def buildFKTransforms(self):
        self.xform[self.robot.get_root()] = generate_translation_rotation(
            IDENTITY,
            self.robot.link_map[self.robot.get_root()].origin.xyz,
            self.robot.link_map[self.robot.get_root()].origin.rpy,
        )

        for child in self.robot.child_map.get(self.robot.get_root(), [[]])[0]:
            joint = self.robot.joint_map.get(child, None)
            if type(joint) is Joint:
                self.traverseFKJoint(joint)

    def traverseFKJoint(self, joint):
        stack = generate_translation_rotation(
            self.xform[joint.parent].copy(),
            joint.origin.xyz,
            joint.origin.rpy
        )

        q = Q.to_rotation_matrix(Q.from_axis_angle(joint.axis, self.angle[joint.name]))

        self.xform[joint.name] = np.matmul(stack, q)

        self.traverseFKLink(self.robot.link_map[joint.child], joint.name)

    def traverseFKLink(self, link, parent):
        self.xform[link.name] = self.xform[parent].copy()
        for child in self.robot.child_map.get(link.name, [[]])[0]:
            joint = self.robot.joint_map.get(child, None)
            if type(joint) is Joint:
                self.traverseFKJoint(joint)
