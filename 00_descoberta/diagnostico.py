# -*- coding: utf-8 -*-
"""
FLAC3D 6.0 - Diagnóstico do ambiente Python e do modelo aberto (SOMENTE LEITURA).

Roda DENTRO do FLAC3D. Não altera o modelo: só lê e grava dois arquivos na pasta do script
(ou na pasta de trabalho do FLAC3D, se o caminho do script não estiver disponível):

  - diagnostico.json  (completo, para colar no repositório e guiar as próximas fases)
  - diagnostico.txt   (resumo legível)

O que ele responde:
  1. Ambiente: versão do Python embutido, executável, pasta de trabalho, se __file__ existe,
     se há console de entrada (input).
  2. Pacotes: numpy, scipy, matplotlib, pandas, openpyxl, python-docx, vtk (presença e versão).
  3. Módulo itasca: quais submódulos existem na 6.00.69 e as funções de cada um.
  4. Modelo aberto (se houver): número de zonas e gridpoints, modelos constitutivos, grupos,
     métodos de um objeto Zone e Gridpoint, amostra da primeira zona, elementos estruturais.
  5. Conferências: se zonearray/gridpointarray existem, a forma (shape) de cada array e se a
     ordem de za.ids() é a mesma de it.zone.list().

Nenhuma etapa aborta o script: cada falha é registrada em "falhas" e o diagnóstico continua.
Compatível com Python 3.6 (sem f-strings).

Como rodar: veja 00_descoberta/README.md.
"""
from __future__ import print_function

import datetime
import importlib
import io
import json
import os
import platform
import sys

VERSAO_SCRIPT = "0.1.0"

# Pacotes procurados no Python do FLAC3D (nome de importação, nome exibido)
PACOTES = [
    ("numpy", "numpy"),
    ("scipy", "scipy"),
    ("matplotlib", "matplotlib"),
    ("pandas", "pandas"),
    ("openpyxl", "openpyxl"),
    ("docx", "python-docx"),
    ("vtk", "vtk"),
]

# Submódulos do itasca citados na documentação (6.0 a 9.x); a 6.0 pode não ter todos
SUBMODULOS_ITASCA = [
    "zone", "gridpoint", "zonearray", "gridpointarray",
    "structure", "interface", "interfacearray", "attach",
    "history", "fish", "vec", "util", "table", "group",
]

# Funções de array a conferir: (módulo, função, chamar_sem_argumentos)
FUNCOES_ARRAY = [
    ("zonearray", "ids", True), ("zonearray", "pos", True), ("zonearray", "stress", True),
    ("zonearray", "stress_flat", True), ("zonearray", "strain", True), ("zonearray", "volume", True),
    ("zonearray", "gridpoints", True), ("zonearray", "faces", True), ("zonearray", "neighbors", True),
    ("zonearray", "in_group", False), ("zonearray", "set_group", False), ("zonearray", "state", False),
    ("zonearray", "prop_scalar", False), ("zonearray", "set_prop_scalar", False), ("zonearray", "extra", False),
    ("gridpointarray", "ids", True), ("gridpointarray", "pos", True), ("gridpointarray", "disp", True),
    ("gridpointarray", "vel", True), ("gridpointarray", "fixity", True), ("gridpointarray", "force_app", True),
    ("gridpointarray", "extra", False),
]


def pasta_do_script():
    arquivo = globals().get("__file__")
    if arquivo:
        return os.path.dirname(os.path.abspath(arquivo))
    return os.getcwd()


PASTA = pasta_do_script()
SAIDA_JSON = os.path.join(PASTA, "diagnostico.json")
SAIDA_TXT = os.path.join(PASTA, "diagnostico.txt")

relatorio = {
    "script": {"nome": "diagnostico.py", "versao": VERSAO_SCRIPT,
               "data": datetime.datetime.now().isoformat(timespec="seconds")},
    "ambiente": {},
    "pacotes": {},
    "itasca": {"importado": False, "submodulos": {}},
    "modelo": {},
    "conferencias": {"arrays": {}, "ordem": {}},
    "falhas": [],
}


def tentar(etapa, funcao, *args):
    """Executa funcao(*args); em caso de erro, registra em 'falhas' e devolve None."""
    try:
        return funcao(*args)
    except Exception as erro:  # noqa: BLE001 - o diagnóstico não pode parar
        relatorio["falhas"].append({"etapa": etapa,
                                    "erro": "{}: {}".format(type(erro).__name__, erro)})
        return None


def simples(valor, profundidade=0):
    """Converte vec3, stens3, arrays e tuplas em listas/números para o JSON."""
    if valor is None or isinstance(valor, (bool, int, float, str)):
        return valor
    if profundidade > 4:
        return str(valor)
    tolist = getattr(valor, "tolist", None)
    if callable(tolist):
        try:
            return tolist()
        except Exception:  # noqa: BLE001
            pass
    try:
        return [simples(item, profundidade + 1) for item in valor]
    except TypeError:
        return str(valor)


def nomes_publicos(objeto):
    return sorted(nome for nome in dir(objeto) if not nome.startswith("_"))


# ---------------------------------------------------------------------------------------------
# 1. Ambiente
# ---------------------------------------------------------------------------------------------
def coletar_ambiente():
    stdin = getattr(sys, "stdin", None)
    relatorio["ambiente"] = {
        "python": sys.version.replace("\n", " "),
        "versao_info": list(sys.version_info[:3]),
        "executavel": sys.executable,
        "plataforma": platform.platform(),
        "pasta_de_trabalho": os.getcwd(),
        "pasta_saida": PASTA,
        "__file__definido": bool(globals().get("__file__")),
        "stdin_existe": stdin is not None,
        "stdin_isatty": bool(stdin is not None and hasattr(stdin, "isatty") and tentar("stdin.isatty", stdin.isatty)),
        "codificacao_padrao": sys.getdefaultencoding(),
        "sys_path_inicio": list(sys.path[:6]),
    }


# ---------------------------------------------------------------------------------------------
# 2. Pacotes
# ---------------------------------------------------------------------------------------------
def coletar_pacotes():
    for nome_import, nome_exibido in PACOTES:
        try:
            modulo = importlib.import_module(nome_import)
            relatorio["pacotes"][nome_exibido] = getattr(modulo, "__version__", "presente, sem versão")
        except Exception as erro:  # noqa: BLE001
            relatorio["pacotes"][nome_exibido] = "AUSENTE ({})".format(type(erro).__name__)


# ---------------------------------------------------------------------------------------------
# 3. Módulo itasca
# ---------------------------------------------------------------------------------------------
def importar_itasca():
    try:
        import itasca  # noqa: F401
    except Exception as erro:  # noqa: BLE001
        relatorio["falhas"].append({"etapa": "import itasca",
                                    "erro": "{}: {} (rodando fora do FLAC3D?)".format(type(erro).__name__, erro)})
        return None
    relatorio["itasca"]["importado"] = True
    relatorio["itasca"]["arquivo"] = getattr(itasca, "__file__", None)
    relatorio["itasca"]["nomes"] = nomes_publicos(itasca)
    # Mantém as variáveis Python entre model new/restore (necessário nos lotes; não altera o modelo)
    tentar("python-reset-state false", itasca.command, "python-reset-state false")
    return itasca


def coletar_submodulos(it):
    for nome in SUBMODULOS_ITASCA:
        modulo = getattr(it, nome, None)
        if modulo is None:
            try:
                modulo = importlib.import_module("itasca." + nome)
            except Exception as erro:  # noqa: BLE001
                relatorio["itasca"]["submodulos"][nome] = "AUSENTE ({})".format(type(erro).__name__)
                continue
        relatorio["itasca"]["submodulos"][nome] = nomes_publicos(modulo)


def submodulo(it, nome):
    modulo = getattr(it, nome, None)
    if modulo is not None:
        return modulo
    try:
        return importlib.import_module("itasca." + nome)
    except Exception:  # noqa: BLE001
        return None


# ---------------------------------------------------------------------------------------------
# 4. Modelo aberto
# ---------------------------------------------------------------------------------------------
def coletar_modelo(it):
    modelo = relatorio["modelo"]
    zona_mod = submodulo(it, "zone")
    gp_mod = submodulo(it, "gridpoint")
    modelo["zonas"] = tentar("zone.count", zona_mod.count) if zona_mod else None
    modelo["gridpoints"] = tentar("gridpoint.count", gp_mod.count) if gp_mod else None

    if not modelo["zonas"]:
        modelo["aviso"] = "Nenhuma zona no modelo. Abra ou restaure um .f3sav e rode de novo para a parte do modelo."
        return

    zonas = tentar("zone.list", lambda: list(zona_mod.list())) or []
    if zonas:
        z = zonas[0]
        modelo["metodos_zone"] = nomes_publicos(z)
        modelo["amostra_zona"] = {
            "id": simples(tentar("zone.id", z.id)),
            "pos": simples(tentar("zone.pos", z.pos)),
            "vol": simples(tentar("zone.vol", z.vol)),
            "model": simples(tentar("zone.model", z.model)),
            "group_default": simples(tentar("zone.group('default')", z.group, "default")),
            "stress": simples(tentar("zone.stress", z.stress)),
            "gridpoints": simples(tentar("zone.gridpoints", lambda: [g.id() for g in z.gridpoints()])),
        }

    constitutivos, grupos = {}, {}
    falhou_modelo = falhou_grupo = False
    for z in zonas:
        if not falhou_modelo:
            try:
                nome = str(z.model())
                constitutivos[nome] = constitutivos.get(nome, 0) + 1
            except Exception as erro:  # noqa: BLE001
                falhou_modelo = True
                relatorio["falhas"].append({"etapa": "zone.model (laço)", "erro": str(erro)})
        if not falhou_grupo:
            try:
                nome = str(z.group("default"))
                grupos[nome] = grupos.get(nome, 0) + 1
            except Exception as erro:  # noqa: BLE001
                falhou_grupo = True
                relatorio["falhas"].append({"etapa": "zone.group (laço)", "erro": str(erro)})
    modelo["modelos_constitutivos"] = constitutivos
    modelo["grupos_slot_default"] = grupos

    gps = tentar("gridpoint.list", lambda: list(gp_mod.list())) if gp_mod else None
    if gps:
        g = gps[0]
        modelo["metodos_gridpoint"] = nomes_publicos(g)
        modelo["amostra_gridpoint"] = {
            "id": simples(tentar("gridpoint.id", g.id)),
            "pos": simples(tentar("gridpoint.pos", g.pos)),
            "disp": simples(tentar("gridpoint.disp", g.disp)),
        }

    est_mod = submodulo(it, "structure")
    if est_mod is not None and hasattr(est_mod, "list"):
        elementos = tentar("structure.list", lambda: list(est_mod.list())) or []
        tipos = {}
        for elemento in elementos:
            tipo = type(elemento).__name__
            tipos[tipo] = tipos.get(tipo, 0) + 1
        modelo["elementos_estruturais"] = tipos
        if elementos:
            modelo["metodos_elemento_estrutural"] = nomes_publicos(elementos[0])


# ---------------------------------------------------------------------------------------------
# 5. Conferências das funções de array
# ---------------------------------------------------------------------------------------------
def coletar_arrays(it):
    arrays = relatorio["conferencias"]["arrays"]
    modulos = {}
    for nome_mod, nome_func, chamar in FUNCOES_ARRAY:
        if nome_mod not in modulos:
            modulos[nome_mod] = submodulo(it, nome_mod)
        modulo = modulos[nome_mod]
        chave = "{}.{}".format(nome_mod, nome_func)
        if modulo is None or not hasattr(modulo, nome_func):
            arrays[chave] = "AUSENTE"
            continue
        if not chamar or not relatorio["modelo"].get("zonas"):
            arrays[chave] = "existe"
            continue
        resultado = tentar(chave, getattr(modulo, nome_func))
        forma = getattr(resultado, "shape", None)
        arrays[chave] = "existe, shape {}".format(list(forma)) if forma is not None else "existe, sem shape"

    ordem = relatorio["conferencias"]["ordem"]
    za, gpa = modulos.get("zonearray"), modulos.get("gridpointarray")
    zona_mod, gp_mod = submodulo(it, "zone"), submodulo(it, "gridpoint")
    if relatorio["modelo"].get("zonas") and za is not None and hasattr(za, "ids"):
        ids_array = tentar("za.ids (ordem)", za.ids)
        ids_lista = tentar("zone.list (ordem)", lambda: [z.id() for z in zona_mod.list()])
        if ids_array is not None and ids_lista is not None:
            ordem["zonas_mesma_ordem"] = [int(v) for v in ids_array] == [int(v) for v in ids_lista]
    if relatorio["modelo"].get("gridpoints") and gpa is not None and hasattr(gpa, "ids"):
        ids_array = tentar("gpa.ids (ordem)", gpa.ids)
        ids_lista = tentar("gridpoint.list (ordem)", lambda: [g.id() for g in gp_mod.list()])
        if ids_array is not None and ids_lista is not None:
            ordem["gridpoints_mesma_ordem"] = [int(v) for v in ids_array] == [int(v) for v in ids_lista]


# ---------------------------------------------------------------------------------------------
# Saída
# ---------------------------------------------------------------------------------------------
def resumo_texto():
    amb, pac, ita, mod = (relatorio["ambiente"], relatorio["pacotes"],
                          relatorio["itasca"], relatorio["modelo"])
    linhas = [
        "DIAGNÓSTICO FLAC3D (diagnostico.py v{})".format(VERSAO_SCRIPT),
        "",
        "Python: {}".format(amb.get("python")),
        "__file__ definido: {}   stdin existe: {}".format(amb.get("__file__definido"), amb.get("stdin_existe")),
        "Pasta de saída: {}".format(PASTA),
        "",
        "Pacotes:",
    ]
    linhas += ["  {:<12} {}".format(nome, versao) for nome, versao in pac.items()]
    linhas += ["", "itasca importado: {}".format(ita.get("importado")), "Submódulos:"]
    for nome, conteudo in ita.get("submodulos", {}).items():
        texto = conteudo if isinstance(conteudo, str) else "{} nomes".format(len(conteudo))
        linhas.append("  {:<15} {}".format(nome, texto))
    linhas += ["", "Modelo:",
               "  zonas: {}   gridpoints: {}".format(mod.get("zonas"), mod.get("gridpoints"))]
    if mod.get("aviso"):
        linhas.append("  " + mod["aviso"])
    if mod.get("modelos_constitutivos"):
        linhas.append("  modelos constitutivos: {}".format(mod["modelos_constitutivos"]))
    if mod.get("grupos_slot_default"):
        linhas.append("  grupos (slot default): {}".format(mod["grupos_slot_default"]))
    if mod.get("elementos_estruturais") is not None:
        linhas.append("  elementos estruturais: {}".format(mod["elementos_estruturais"]))
    linhas += ["", "Funções de array:"]
    for chave, estado in relatorio["conferencias"]["arrays"].items():
        linhas.append("  {:<32} {}".format(chave, estado))
    for chave, valor in relatorio["conferencias"]["ordem"].items():
        linhas.append("  {:<32} {}".format(chave, valor))
    linhas += ["", "Falhas registradas: {}".format(len(relatorio["falhas"]))]
    linhas += ["  - {}: {}".format(f["etapa"], f["erro"]) for f in relatorio["falhas"]]
    return "\n".join(linhas) + "\n"


def gravar():
    with io.open(SAIDA_JSON, "w", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(relatorio, indent=2, ensure_ascii=False, default=str))
    texto = resumo_texto()
    with io.open(SAIDA_TXT, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)
    print(texto)
    print("Arquivos gravados:\n  {}\n  {}".format(SAIDA_JSON, SAIDA_TXT))


def principal():
    coletar_ambiente()
    coletar_pacotes()
    it = importar_itasca()
    if it is not None:
        coletar_submodulos(it)
        coletar_modelo(it)
        coletar_arrays(it)
    gravar()


principal()
