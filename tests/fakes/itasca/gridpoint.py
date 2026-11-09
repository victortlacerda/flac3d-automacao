# -*- coding: utf-8 -*-
"""itasca.gridpoint falso."""
from . import _modelo


class Gridpoint(object):
    def __init__(self, dados):
        self._d = dados

    def id(self):
        return self._d["id"]

    def pos(self):
        return self._d["pos"]

    def disp(self):
        return self._d["disp"]

    def __repr__(self):
        return "<itasca.gridpoint.Gridpoint (falso) ID : {}>".format(self._d["id"])


def count():
    return len(_modelo.GRIDPOINTS)


def list():  # noqa: A001 - mesmo nome do itasca real
    return iter([Gridpoint(d) for d in _modelo.GRIDPOINTS])
