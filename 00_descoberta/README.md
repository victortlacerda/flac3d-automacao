# 00_descoberta: diagnóstico do FLAC3D 6.0

**Status:** testado por mock. **[não testado]** no FLAC3D real.

`diagnostico.py` roda **dentro** do FLAC3D e **só lê**: não muda o modelo. Ele descobre o que a
API Python da versão instalada (6.00.69) oferece, antes de escrever os extratores.

## Como rodar

1. Abra o FLAC3D 6.0. Para a parte do modelo, abra ou restaure um `.f3sav` calculado. Sem modelo,
   o script ainda registra o ambiente e o módulo `itasca`.
   - Sugestão para o primeiro teste: um exemplo pequeno de
     `C:\Program Files\Itasca\Flac3d600\datafiles\UsersGuide\Tutorial`, já calculado e salvo.
2. Rode o script por **uma** das formas abaixo e anote qual funcionou:
   - **Editor do FLAC3D:** abra o `.py` no editor do programa e use o botão de executar.
   - **Linha de comando:** `program call "C:\caminho\00_descoberta\diagnostico.py"`.
     A sintaxe exata para `.py` na 6.0 é uma das coisas que este teste confirma.
3. Confira a saída no console. O script grava dois arquivos na pasta dele
   (ou na pasta de trabalho do FLAC3D, se o caminho do script não estiver disponível):
   - `diagnostico.json`: completo.
   - `diagnostico.txt`: resumo legível.
4. Envie o `diagnostico.json` (ou cole o `diagnostico.txt` na conversa). Ele vira
   `docs/diagnostico_6.00.69.json` no repositório e define o que as fases 1 a 7 podem usar.

## O que ele responde

| Pergunta | Onde aparece |
| --- | --- |
| Versão do Python embutido, executável, pasta de trabalho | `ambiente` |
| `__file__` existe? Há console de entrada (`input`)? | `ambiente.__file__definido`, `ambiente.stdin_existe` |
| numpy, scipy, matplotlib, pandas, openpyxl, python-docx, vtk | `pacotes` |
| Submódulos do `itasca` e as funções de cada um | `itasca.submodulos` |
| Zonas, gridpoints, modelos constitutivos, grupos | `modelo` |
| Métodos de um objeto Zone e Gridpoint, amostra da primeira zona | `modelo.metodos_zone`, `modelo.amostra_zona` |
| Elementos estruturais por tipo | `modelo.elementos_estruturais` |
| Funções de `zonearray` e `gridpointarray`, com o shape | `conferencias.arrays` |
| `za.ids()` tem a mesma ordem de `it.zone.list()`? | `conferencias.ordem` |
| Tudo que deu erro, sem parar o script | `falhas` |

## Observações

- O único comando enviado ao FLAC3D é `python-reset-state false`, que mantém as variáveis
  Python entre `model restore`. Ele não altera o modelo.
- O laço sobre as zonas lê `model()` e `group("default")` de cada uma. Em modelos com centenas de
  milhares de zonas isso pode levar alguns segundos.
- Se a forma de rodar for diferente das listadas acima, anote a que funcionou: ela entra no
  README principal.
