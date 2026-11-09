# -*- coding: utf-8 -*-
"""itasca.gridpointarray falso."""
import numpy as np

from . import _modelo


def ids():
    return np.array([d["id"] for d in _modelo.GRIDPOINTS], dtype=np.int64)


def pos():
    return np.array([d["pos"] for d in _modelo.GRIDPOINTS], dtype=float)


def disp():
    return np.array([d["disp"] for d in _modelo.GRIDPOINTS], dtype=float)
