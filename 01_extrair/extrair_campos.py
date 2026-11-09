# -*- coding: utf-8 -*-
"""
FLAC3D 6.0 - Extração dos campos de zonas e gridpoints para NumPy. [não testado no FLAC3D real]

Roda DENTRO do FLAC3D. Lê o modelo aberto (ou restaura um .f3sav) e grava na pasta do script:

  - <SAIDA>.npz   arrays NumPy (SI: m, Pa; convenção do FLAC3D, compressão NEGATIVA)
  - <SAIDA>.json  metadados, unidades, convenção de sinais e resumo de valores calculados

Conteúdo do .npz:
  zona_id (n)            zona_pos (n,3) [m]        zona_tensao (n,3,3) [Pa]
  zona_vol (n) [m³]      zona_modelo (n) [texto]   zona_grupo (n) [texto, slot SLOT_GRUPO]
  zona_gps (n,8)         índices dos gridpoints de cada zona (ordem de gp_id; -1 = inexistente)
  gp_id (m)              gp_pos (m,3) [m]          gp_desl (m,3) [m]

O resumo do .json já vem na convenção geotécnica (recalque e compressão positivos), em mm e kPa.

Depende só de numpy. Os gráficos ficam em 02_graficos (fora do FLAC3D).
Compatível com Python 3.6 (sem f-strings).

Pré-requisito: rodar 00_descoberta/diagnostico.py uma vez e conferir em
"conferencias.arrays" que as funções usadas aqui existem na sua versão.
"""
from __future__ import print_function

import datetime
import io
import json
import os

import numpy as np

import itasca as it

VERSAO_SCRIPT = "0.1.0"

# ----------------------------------------------------------------------------- configuração ---
SAVE = None                 # None = usa o modelo aberto; ou "C:/.../modelo.f3sav"
SAIDA = "extracao"          # nome base dos arquivos de saída
SLOT_GRUPO = "default"      # slot de grupo lido de cada zona
# ----------------------------------------------------------------------------------------------


def pasta_do_script():
    arquivo = globals().get("__file__")
    if arquivo:
        return os.path.dirname(os.path.abspath(arquivo))
    return os.getcwd()


PASTA = pasta_do_script()


def submodulo(nome):
    modulo = getattr(it, nome, None)
    if modulo is None:
        modulo = __import__("itasca." + nome, fromlist=[nome])
    return modulo


def extrair():
    it.command("python-reset-state false")
    if SAVE:
        it.command("model restore '{}'".format(SAVE.replace("\\", "/")))

    za = submodulo("zonearray")
    gpa = submodulo("gridpointarray")
    zona_mod = submodulo("zone")

    if zona_mod.count() == 0:
        raise RuntimeError("Nenhuma zona no modelo: abra ou restaure um .f3sav calculado (ou defina SAVE).")

    dados = {
        "zona_id": np.asarray(za.ids()),
        "zona_pos": np.asarray(za.pos(), dtype=float),
        "zona_tensao": np.asarray(za.stress(), dtype=float),
        "zona_gps": np.asarray(za.gridpoints()),
        "gp_id": np.asarray(gpa.ids()),
        "gp_pos": np.asarray(gpa.pos(), dtype=float),
        "gp_desl": np.asarray(gpa.disp(), dtype=float),
    }

    # Atributos sem função de array na 6.0: lidos zona a zona e casados PELO ID com a ordem de za
    por_id = {}
    for z in zona_mod.list():
        por_id[int(z.id())] = (float(z.vol()), str(z.model()), str(z.group(SLOT_GRUPO)))
    faltando = [int(i) for i in dados["zona_id"] if int(i) not in por_id]
    if faltando:
        raise RuntimeError("{} zonas de za.ids() não aparecem em it.zone.list()".format(len(faltando)))
    dados["zona_vol"] = np.array([por_id[int(i)][0] for i in dados["zona_id"]])
    dados["zona_modelo"] = np.array([por_id[int(i)][1] for i in dados["zona_id"]])
    dados["zona_grupo"] = np.array([por_id[int(i)][2] for i in dados["zona_id"]])
    return dados


def resumo(dados):
    """Valores calculados, já na convenção geotécnica (compressão e recalque positivos)."""
    desl_mm = dados["gp_desl"] * 1e3
    tensao_kpa = -dados["zona_tensao"] / 1e3
    principais = np.linalg.eigvalsh(tensao_kpa)          # ordem crescente: s3, s2, s1
    s3, s2, s1 = principais[:, 0], principais[:, 1], principais[:, 2]
    p = (s1 + s2 + s3) / 3.0
    q = np.sqrt(0.5 * ((s1 - s2) ** 2 + (s2 - s3) ** 2 + (s3 - s1) ** 2))
    i_rec = int(np.argmin(desl_mm[:, 2]))
    i_hor = int(np.argmax(np.hypot(desl_mm[:, 0], desl_mm[:, 1])))
    grupos, contagem = np.unique(dados["zona_grupo"], return_counts=True)
    return {
        "recalque_max_mm": round(float(-desl_mm[i_rec, 2]), 3),
        "recalque_max_pos_m": [round(float(v), 4) for v in dados["gp_pos"][i_rec]],
        "desl_horizontal_max_mm": round(float(np.hypot(desl_mm[i_hor, 0], desl_mm[i_hor, 1])), 3),
        "desl_horizontal_max_pos_m": [round(float(v), 4) for v in dados["gp_pos"][i_hor]],
        "desl_total_max_mm": round(float(np.linalg.norm(desl_mm, axis=1).max()), 3),
        "sigma1_max_kpa": round(float(s1.max()), 2),
        "p_max_kpa": round(float(p.max()), 2),
        "q_max_kpa": round(float(q.max()), 2),
        "volume_total_m3": round(float(dados["zona_vol"].sum()), 4),
        "zonas_por_grupo": {str(g): int(c) for g, c in zip(grupos, contagem)},
    }


def gravar(dados, valores):
    caminho_npz = os.path.join(PASTA, SAIDA + ".npz")
    caminho_json = os.path.join(PASTA, SAIDA + ".json")
    np.savez_compressed(caminho_npz, **dados)
    meta = {
        "script": {"nome": "extrair_campos.py", "versao": VERSAO_SCRIPT,
                   "data": datetime.datetime.now().isoformat(timespec="seconds")},
        "save": SAVE,
        "slot_grupo": SLOT_GRUPO,
        "zonas": int(len(dados["zona_id"])),
        "gridpoints": int(len(dados["gp_id"])),
        "unidades_npz": {"comprimento": "m", "tensao": "Pa", "deslocamento": "m", "volume": "m3"},
        "sinal_npz": "FLAC3D: tração positiva, compressão negativa; deslocamento no sentido dos eixos",
        "sinal_resumo": "geotécnico: compressão positiva, recalque positivo para baixo",
        "arrays": {nome: list(valor.shape) for nome, valor in dados.items()},
        "resumo": valores,
    }
    with io.open(caminho_json, "w", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(meta, indent=2, ensure_ascii=False))
    return caminho_npz, caminho_json


def principal():
    dados = extrair()
    valores = resumo(dados)
    caminho_npz, caminho_json = gravar(dados, valores)
    print("Extração concluída: {} zonas, {} gridpoints".format(len(dados["zona_id"]), len(dados["gp_id"])))
    for chave, valor in valores.items():
        print("  {:<28} {}".format(chave, valor))
    print("Arquivos gravados:\n  {}\n  {}".format(caminho_npz, caminho_json))


principal()
