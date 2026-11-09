# Exemplos do fabricante usados na validação

Os exemplos vêm com o FLAC3D em `C:\Program Files\Itasca\Flac3d600\datafiles` (instalação do usuário,
6.00.69). São 1.404 arquivos: 850 `.f3dat`, 167 projetos `.f3prj`, 69 `.dat`, 43 tabelas `.tab`,
38 FISH (`.fis`/`.f3fis`) e **nenhum `.py`**. Ou seja, os exemplos são em comandos e FISH; o fluxo de
validação é rodar o exemplo, salvar o `.f3sav` e extrair pelo Python.

Quase todas as pastas de `Structure` têm `master.f3dat` (roda o caso) e `check.f3dat` (confere o
resultado). O `check.f3dat` é a referência dos extratores. Os arquivos **não** são copiados para este
repositório (são do fabricante); só os resultados extraídos entram em `exemplos/`.

## Casos por fase

| Fase | Exemplo (pasta em `datafiles`) | Para que serve | O que validar |
| --- | --- | --- | --- |
| 0 | `UsersGuide/Tutorial` | Modelos pequenos e rápidos | Diagnóstico e primeiro teste do extrator |
| 1–2 | `VerificationProblems/SquareFooting`, `CircularFooting`, `PrandtlsWedge` | Sapatas com solução teórica | Recalque, bacia, curva carga × recalque, qu |
| 1–2 | `ExampleApplications/EmbankmentLoad`, `HorizontalCut`, `SlopeCurvature` | Aterro, corte e talude | Perfis de deslocamento, plastificação, FS |
| 3 | `Structure/Liner/EmbeddedRetainingWall` | Cortina embutida (mais perto do cortina-e-muro) | Inclinômetro virtual, M e V na parede |
| 3 | `ExampleApplications/AnchoredExcavation` (17 `.f3dat`), `BracedExcavation`, `CaissonWithTiebacks` | Escavação com tirantes e escoras | Força nos tirantes, estágios, deslocamento da parede |
| 3 | `Structure/Cable/SoilNailing` | Solo grampeado | Força axial ao longo de cada grampo |
| 3 | `Structure/Pile/AxiallyLoaded`, `LaterallyLoaded`; `ExampleApplications/ConcretePile` | Estacas | N ao longo da estaca, p-y, deslocamento do topo |
| 3 | `Structure/Beam/Cantilever`, `ConcentratedLoads`, `PlasticHinge`; `Structure/Shell/Cantilever`, `PlateAppliedPressure` | Respostas analíticas simples | Esforços de beam e shell contra o `check.f3dat` |
| 3 | `Structure/Geogrid/ReinforcedEmbankment`, `PullOutTest`, `SoilInterfaceTest` | Geogrelha | Tração e mobilização |
| 3 | `Interface/DirectShearTest` | Interface | Tensões normal e cisalhante, deslizamento |
| 4 | `ExampleApplications/ExcavationInSaturatedSoil`, `ExcavationAndSupportOfShallowTunnel` | Escavação por etapas com água | Incrementos por estágio, poropressão |
| 4 | `Fluid/1DConsolidation`, `ConsolidationSettlement`, `Fluid/Footing` | Adensamento com solução teórica | Recalque × tempo, poropressão |

## Outras pastas (referência de sintaxe da 6.0)

| Pasta | Conteúdo |
| --- | --- |
| `ConstitutiveModels/` (20 casos) | Triaxial, edômetro e compressão isotrópica em vários modelos (MC, Plastic-Hardening, CYSoil, Cam-Clay, Hoek-Brown) |
| `VerificationProblems/` (13 casos) | Problemas com solução analítica: sapatas, túneis, cilindros, placas |
| `Fluid/` (18 casos) | Fluxo e adensamento |
| `Dynamic/`, `Creep/`, `Thermal/` | Fora do escopo inicial |
| `FISH/Library`, `FISH/Tutorial` | Funções FISH prontas: úteis para descobrir nomes de grandezas da 6.0 |

Os `.f3dat` também mostram a sintaxe de comandos da 6.0 (histórias, fator de segurança, estruturas).
Antes de automatizar um comando na fase 4, a sintaxe é tirada daqui ou do histórico de comandos do
usuário, nunca adivinhada.
