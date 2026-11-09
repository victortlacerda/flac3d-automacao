# -*- coding: utf-8 -*-
"""
Roda um script do projeto com o itasca FALSO e imprime uma saída normalizada para comparar
com tests/baselines/<cenario>.log.

    python tests/mock/rodar.py diagnostico
    python tests/mock/rodar.py diagnostico_sem_itasca
    python tests/mock/rodar.py extrair

O script é copiado para uma pasta temporária e rodado lá (como o FLAC3D faria, com __file__
apontando para a cópia), para os arquivos de saída não caírem dentro do repositório.
Datas, versões e caminhos que mudam de máquina para máquina são trocados por <marcadores>.
"""
from __future__ import print_function

import contextlib
import io
import json
import os
import runpy
import shutil
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FAKES = os.path.join(RAIZ, "tests", "fakes")

CENARIOS = {
    "diagnostico": ("00_descoberta/diagnostico.py", True),
    "diagnostico_sem_itasca": ("00_descoberta/diagnostico.py", False),
    "extrair": ("01_extrair/extrair_campos.py", True),
}


def rodar(script_rel, com_itasca):
    pasta = tempfile.mkdtemp(prefix="flac3d_mock_")
    copia = os.path.join(pasta, os.path.basename(script_rel))
    shutil.copy(os.path.join(RAIZ, script_rel), copia)
    caminho_original = list(sys.path)
    if com_itasca:
        sys.path.insert(0, FAKES)
    saida = io.StringIO()
    try:
        with contextlib.redirect_stdout(saida):
            runpy.run_path(copia, run_name="__flac3d__")
    finally:
        sys.path[:] = caminho_original
    comandos = []
    if com_itasca:
        from itasca import _modelo  # noqa: E402 - importado só com o fake no caminho
        comandos = list(_modelo.COMANDOS)
    return pasta, saida.getvalue(), comandos


def limpar(texto, pasta):
    return texto.replace(pasta, "<PASTA>").replace(os.sep, "/")


def normalizar_diagnostico(pasta):
    with io.open(os.path.join(pasta, "diagnostico.json"), encoding="utf-8") as arquivo:
        d = json.load(arquivo)
    d["script"]["data"] = "<data>"
    d["ambiente"] = sorted(d["ambiente"].keys())
    d["pacotes"] = {"numpy_presente": not str(d["pacotes"].get("numpy", "")).startswith("AUSENTE")}
    if "arquivo" in d["itasca"]:
        d["itasca"]["arquivo"] = "<itasca falso>"
    return d


def principal():
    cenario = sys.argv[1] if len(sys.argv) > 1 else ""
    if cenario not in CENARIOS:
        print("Uso: rodar.py {" + ",".join(sorted(CENARIOS)) + "}")
        sys.exit(2)
    script_rel, com_itasca = CENARIOS[cenario]
    pasta, saida, comandos = rodar(script_rel, com_itasca)
    try:
        print("== cenario:", cenario)
        print("== comandos enviados ao FLAC3D:")
        for linha in comandos:
            print("CMD", linha)
        if cenario.startswith("diagnostico"):
            print("== arquivos:", sorted(os.listdir(pasta)))
            print("== diagnostico.json (normalizado):")
            print(json.dumps(normalizar_diagnostico(pasta), indent=2, ensure_ascii=False, sort_keys=True))
        else:
            import numpy as np
            print("== console:")
            print(limpar(saida, pasta))
            with io.open(os.path.join(pasta, "extracao.json"), encoding="utf-8") as arquivo:
                meta = json.load(arquivo)
            meta["script"]["data"] = "<data>"
            print("== extracao.json (normalizado):")
            print(json.dumps(meta, indent=2, ensure_ascii=False, sort_keys=True))
            print("== extracao.npz:")
            with np.load(os.path.join(pasta, "extracao.npz")) as npz:
                for nome in sorted(npz.files):
                    valor = npz[nome]
                    if valor.dtype.kind in "iuf":
                        print("{:<12} {:<10} {:<8} soma={:.6g}".format(
                            nome, str(list(valor.shape)), valor.dtype.kind, float(valor.sum())))
                    else:
                        print("{:<12} {:<10} {:<8} valores={}".format(
                            nome, str(list(valor.shape)), valor.dtype.kind, sorted(set(valor.tolist()))))
    finally:
        shutil.rmtree(pasta, ignore_errors=True)


principal()
