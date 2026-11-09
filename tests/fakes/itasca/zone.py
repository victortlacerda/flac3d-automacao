# -*- coding: utf-8 -*-
"""itasca.zone falso."""
from . import _modelo


class Zone(object):
    def __init__(self, dados):
        self._d = dados

    def id(self):
        return self._d["id"]

    def pos(self):
        return self._d["pos"]

    def vol(self):
        return self._d["vol"]

    def model(self):
        return self._d["modelo"]

    def group(self, slot="default"):
        if slot != "default":
            return "None"
        return self._d["grupo"]

    def stress(self):
        return self._d["stress"]

    def gridpoints(self):
        from .gridpoint import Gridpoint
        return tuple(Gridpoint(_modelo.GRIDPOINTS[i]) for i in self._d["gps"])

    def __repr__(self):
        return "<itasca.zone.Zone (falso) ID : {}>".format(self._d["id"])


def count():
    return len(_modelo.ZONAS)


def list():  # noqa: A001 - mesmo nome do itasca real
    return iter([Zone(d) for d in _modelo.ZONAS])


def find(id_zona):
    for d in _modelo.ZONAS:
        if d["id"] == id_zona:
            return Zone(d)
    return None
