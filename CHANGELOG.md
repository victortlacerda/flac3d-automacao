# Changelog

## 0.1.0 (09/11/2026)
- `00_descoberta/diagnostico.py`: diagnóstico somente leitura do Python embutido, pacotes, API `itasca`
  da 6.0, modelo aberto e funções de array. Testado por mock; falta rodar no FLAC3D real.
- `01_extrair/extrair_campos.py`: zonas e gridpoints para `.npz` + `.json` com resumo de valores
  calculados. Testado por mock; **[não testado]** no FLAC3D real.
- `tests/`: `itasca` falso (bloco 2 × 2 × 2), executor de cenários, linhas de base, checagem de
  compatibilidade com Python 3.6 e GitHub Actions.
- `docs/`: roadmap, referências e exemplos do fabricante usados na validação.
