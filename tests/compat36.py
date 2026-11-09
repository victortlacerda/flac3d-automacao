# -*- coding: utf-8 -*-
"""
Confere se os scripts que rodam DENTRO do FLAC3D 6.0 evitam sintaxe nova demais para o Python
embutido (a versão exata sai do diagnóstico; por segurança, o alvo é Python 3.6).

Recusa: f-strings, operador morsa (:=), match/case e parâmetros só-posicionais (/).

    python tests/compat36.py
"""
from __future__ import print_function

import ast
import glob
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTAS_INTERNAS = ["00_descoberta", "01_extrair"]   # scripts que rodam no Python do FLAC3D


def problemas(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        arvore = ast.parse(arquivo.read(), caminho)
    achados = []
    for no in ast.walk(arvore):
        linha = getattr(no, "lineno", "?")
        if isinstance(no, ast.JoinedStr):
            achados.append((linha, "f-string"))
        elif type(no).__name__ == "NamedExpr":
            achados.append((linha, "operador :="))
        elif type(no).__name__ == "Match":
            achados.append((linha, "match/case"))
        elif isinstance(no, ast.arguments) and getattr(no, "posonlyargs", None):
            achados.append((linha, "parâmetro só-posicional"))
    return achados


def principal():
    total = 0
    for pasta in PASTAS_INTERNAS:
        for caminho in sorted(glob.glob(os.path.join(RAIZ, pasta, "*.py"))):
            for linha, tipo in problemas(caminho):
                print("{}:{}: {} (incompatível com Python 3.6)".format(os.path.relpath(caminho, RAIZ), linha, tipo))
                total += 1
    if total:
        sys.exit(1)
    print("Compatibilidade Python 3.6: OK")


principal()
