# Referências

Consultadas em 09/11/2026.

## Documentação Itasca
- [Using Python with FLAC3D, documentação 6.0](https://docs.itascacg.com/pfc600/common/docproject/source/manual/scripting/python/doc/python_flac3d.py.html):
  `it.command`, zonas, gridpoints, estruturas, extra variables, callbacks, estudo paramétrico, erros,
  `python-reset-state false`.
- [Array Style Programming with FLAC3D and NumPy, documentação 6.0](https://docs.itascacg.com/pfc600/common/docproject/source/manual/scripting/python/doc/flac3d_array_interface.py.html):
  `zonearray`, `gridpointarray`, máscaras e grupos. Os arrays são **cópias** dos dados do modelo.
- [itasca.zonearray, documentação 9.0](https://docs.itascacg.com/itasca900/common/docproject/source/manual/scripting/python/doc/itasca.zonearray.html):
  lista completa das funções de array das versões atuais, para comparar com a 6.0.
- [FLAC3D Python, documentação 9.3](https://docs.itascacg.com/itasca930/common/docproject/source/manual/scripting/python/python_flac3d.html):
  índice com o exemplo de numpy e matplotlib.
- [Using Python in FLAC3D 6 (Itasca)](https://www.itascacg.com/staging/cn/learning/tutorials/using-python-in-flac3d-6):
  webinar de introdução.

## Bibliotecas gratuitas
- [itasca-python (BSD-3)](https://github.com/itascaconsulting/itasca-python): conexão por socket com FISH
  e leitura/escrita de arquivos binários FISH. Alternativa caso seja preciso controlar o FLAC3D de fora.
- NumPy, matplotlib, openpyxl: parte externa (gráficos, Excel).
- ParaView: visualização dos `.vtu` da fase 6.

## Projetos do mesmo autor
- [plaxis3d-automacao](https://github.com/victortlacerda/plaxis3d-automacao): organização, mock com
  linhas de base, critérios de capacidade de carga, memorial.
- [slide2-automacao](https://github.com/victortlacerda/slide2-automacao): módulos numerados, roadmap,
  pytest + GitHub Actions.
