import math

import numpy as np
from numpy import matmul as mm

IDENTITY = np.array([[1 if i == k else 0 for i in range(4)] for k in range(4)], dtype=np.float64)


def generate_translation_rotation(prev, xyz, rpy):
    trans = IDENTITY.copy()
    trans[-1] = [*xyz, 1]
    trans = trans.T

    rotx = IDENTITY.copy()
    rotx[1][1] = math.cos(rpy[0])
    rotx[1][2] = -math.sin(rpy[0])
    rotx[2][1] = math.sin(rpy[0])
    rotx[2][2] = math.cos(rpy[0])

    roty = IDENTITY.copy()
    roty[0][0] = math.cos(rpy[1])
    roty[0][2] = math.sin(rpy[1])
    roty[2][0] = -math.sin(rpy[1])
    roty[2][2] = math.cos(rpy[1])

    rotz = IDENTITY.copy()
    rotz[0][0] = math.cos(rpy[2])
    rotz[0][1] = -math.sin(rpy[2])
    rotz[1][0] = math.sin(rpy[2])
    rotz[1][1] = math.cos(rpy[2])

    return mm(mm(mm(mm(prev, trans), rotz), roty), rotx)
