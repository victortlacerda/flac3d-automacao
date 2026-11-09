# -*- coding: utf-8 -*-
"""itasca.zonearray falso (só as funções usadas pelos scripts e pelo diagnóstico)."""
import numpy as np

from . import _modelo


def ids():
    return np.array([d["id"] for d in _modelo.ZONAS], dtype=np.int64)


def pos():
    return np.array([d["pos"] for d in _modelo.ZONAS], dtype=float)


def stress():
    return np.array([d["stress"] for d in _modelo.ZONAS], dtype=float)


def volume():
    return np.array([d["vol"] for d in _modelo.ZONAS], dtype=float)


def gridpoints():
    return np.array([d["gps"] for d in _modelo.ZONAS], dtype=np.int64)


def in_group(nome, slot="default"):
    return np.array([d["grupo"] == nome for d in _modelo.ZONAS], dtype=bool)
