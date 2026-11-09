# Testes por mock (sem FLAC3D)

- `fakes/itasca/`: `itasca` falso com um bloco de 2 × 2 × 2 zonas de 1 m e valores conferíveis à mão
  (veja `_modelo.py`). Imita `command`, `zone`, `gridpoint`, `zonearray`, `gridpointarray` e `structure`.
- `mock/rodar.py <cenario>`: copia o script para uma pasta temporária, roda com o fake e imprime uma
  saída normalizada (datas, versões e caminhos viram `<marcadores>`).
- `baselines/`: saída esperada de cada cenário.
- `regressao.sh`: confere a compatibilidade com Python 3.6 e compara cada cenário com a linha de base;
  `--gravar` atualiza as linhas de base.
- `compat36.py`: recusa f-strings, `:=`, `match` e parâmetros só-posicionais nos scripts que rodam
  dentro do FLAC3D.

| Cenário | Script | O que confere |
| --- | --- | --- |
| `diagnostico` | `00_descoberta/diagnostico.py` | Coleta completa, sem falhas, ordem de ids conferida |
| `diagnostico_sem_itasca` | `00_descoberta/diagnostico.py` | Fora do FLAC3D: registra a falha e grava o arquivo mesmo assim |
| `extrair` | `01_extrair/extrair_campos.py` | Arrays, casamento por id, resumo (8,0 mm de recalque, σ1 = 80,06 kPa) |

```bash
pip install numpy
./tests/regressao.sh            # compara com tests/baselines/
./tests/regressao.sh --gravar   # atualiza as linhas de base (só depois de revisar a mudança)
```

O mock confere **fluxo, comandos e cálculos**, não os nomes reais da API da 6.00.69: só o FLAC3D valida
isso, e o diagnóstico mostra o que existe.
