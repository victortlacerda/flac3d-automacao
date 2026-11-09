# -*- coding: utf-8 -*-
"""
itasca FALSO, para testar os scripts sem o FLAC3D.

Imita só o que os scripts usam, com os nomes da documentação 6.0. Confere fluxo, ordem de
comandos e cálculos; NÃO confere a mecânica nem os nomes reais da 6.00.69 (isso é o diagnóstico).
"""
from . import _modelo
from . import zone, gridpoint, zonearray, gridpointarray, structure  # noqa: F401


def command(texto):
    for linha in str(texto).strip().splitlines():
        linha = linha.strip()
        if linha:
            _modelo.COMANDOS.append(linha)
