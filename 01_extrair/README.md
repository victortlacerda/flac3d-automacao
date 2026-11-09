# 01_extrair: campos de zonas e gridpoints

**Status:** testado por mock. **[não testado]** no FLAC3D real; depende do diagnóstico da fase 0.

`extrair_campos.py` roda **dentro** do FLAC3D, lê o modelo aberto (ou restaura um `.f3sav`) e grava
os campos em NumPy, para os gráficos e cálculos rodarem fora do programa.

## Como rodar

1. Rode antes `00_descoberta/diagnostico.py` e confira em `conferencias.arrays` que existem
   `zonearray.ids`, `pos`, `stress`, `gridpoints` e `gridpointarray.ids`, `pos`, `disp`.
2. Edite o topo do script, se quiser:
   - `SAVE = None` usa o modelo aberto; ou o caminho de um `.f3sav`.
   - `SAIDA = "extracao"` é o nome base dos arquivos.
   - `SLOT_GRUPO = "default"` é o slot de grupo lido de cada zona.
3. Rode no FLAC3D do mesmo jeito que o diagnóstico.

## Saída (na pasta do script)

| Arquivo | Conteúdo |
| --- | --- |
| `extracao.npz` | `zona_id`, `zona_pos`, `zona_tensao` (n×3×3), `zona_vol`, `zona_modelo`, `zona_grupo`, `zona_gps` (n×8), `gp_id`, `gp_pos`, `gp_desl` |
| `extracao.json` | Unidades, convenção de sinais, shape de cada array e um resumo de valores calculados |

O `.npz` fica em SI e na convenção do FLAC3D (**compressão negativa**). O resumo do `.json` já vem
na convenção geotécnica (compressão e recalque positivos), em mm e kPa:

- recalque máximo e onde ocorre;
- deslocamento horizontal máximo e onde ocorre;
- deslocamento total máximo;
- σ1, p e q máximos;
- volume total e zonas por grupo.

## Validação pendente

- [ ] Comparar uma zona e um gridpoint com o `zone list` / plot do FLAC3D.
- [ ] Rodar num exemplo do fabricante (`VerificationProblems/SquareFooting`).
- [ ] Medir o tempo num modelo grande (o laço zona a zona é a parte lenta).
