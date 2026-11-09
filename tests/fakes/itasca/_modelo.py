# -*- coding: utf-8 -*-
"""
Modelo sintético do itasca falso: bloco 2 x 2 x 2 zonas de 1 m (0 a 2 m em x, y e z).

Valores determinísticos e fáceis de conferir à mão:
  deslocamento do gridpoint: ux = 0.001 * x * z / 4, uy = 0, uz = -0.002 * z * (1 + x / 2)   [m]
  tensão da zona (Pa, compressão negativa): szz = -20e3 * (2 - zc) - 50e3, sxx = syy = 0.5 * szz,
                                            sxz = 1e3 * xc, demais = 0
  grupo: "inferior" se zc < 1, senão "superior"; modelo: "mohr-coulomb" no inferior, "elastic" no superior
"""
from __future__ import print_function

NX = NY = NZ = 2
LADO = 1.0

COMANDOS = []   # registro de it.command(), lido pelo executor de testes


def _gp_indice(i, j, k):
    return i + (NX + 1) * (j + (NY + 1) * k)


GRIDPOINTS = []
for _k in range(NZ + 1):
    for _j in range(NY + 1):
        for _i in range(NX + 1):
            _x, _y, _z = _i * LADO, _j * LADO, _k * LADO
            GRIDPOINTS.append({
                "id": len(GRIDPOINTS) + 1,
                "pos": (_x, _y, _z),
                "disp": (0.001 * _x * _z / 4.0, 0.0, -0.002 * _z * (1.0 + _x / 2.0)),
            })

ZONAS = []
for _k in range(NZ):
    for _j in range(NY):
        for _i in range(NX):
            _xc, _yc, _zc = (_i + 0.5) * LADO, (_j + 0.5) * LADO, (_k + 0.5) * LADO
            _szz = -20e3 * (2.0 - _zc) - 50e3
            _sxz = 1e3 * _xc
            # ordem dos 8 gridpoints segue a convenção do brick do FLAC3D só como referência
            _gps = [_gp_indice(_i, _j, _k), _gp_indice(_i + 1, _j, _k), _gp_indice(_i, _j + 1, _k),
                    _gp_indice(_i, _j, _k + 1), _gp_indice(_i + 1, _j + 1, _k), _gp_indice(_i, _j + 1, _k + 1),
                    _gp_indice(_i + 1, _j, _k + 1), _gp_indice(_i + 1, _j + 1, _k + 1)]
            ZONAS.append({
                "id": len(ZONAS) + 1,
                "pos": (_xc, _yc, _zc),
                "vol": LADO ** 3,
                "stress": ((0.5 * _szz, 0.0, _sxz), (0.0, 0.5 * _szz, 0.0), (_sxz, 0.0, _szz)),
                "grupo": "inferior" if _zc < 1.0 else "superior",
                "modelo": "mohr-coulomb" if _zc < 1.0 else "elastic",
                "gps": _gps,
            })
