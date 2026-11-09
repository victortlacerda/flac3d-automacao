# Roadmap

Documento completo (arquitetura, catálogo de funcionalidades, riscos):
[Roadmap — Automação FLAC3D com Python](https://claude.ai/artifact/V6TARLHM5hNRJ5HeoSB6d1).
Este arquivo é o checklist do repositório.

Cada fase só fecha quando o critério de pronto bate no **FLAC3D real**. Os casos de validação estão em
[`exemplos_fabricante.md`](exemplos_fabricante.md).

## Fase 0: descoberta e ambiente (em andamento)
- [x] `00_descoberta/diagnostico.py` (somente leitura), testado por mock.
- [x] `itasca` falso em `tests/fakes/` e `tests/regressao.sh`.
- [x] Checagem de compatibilidade com Python 3.6 (`tests/compat36.py`) e GitHub Actions.
- [ ] Rodar o diagnóstico no FLAC3D 6.00.69 e guardar em `docs/diagnostico_6.00.69.json`.
- [ ] Anotar como o `.py` roda (editor, `program call`, outra forma) e se `input()` funciona.
- [ ] Rodar um exemplo de `UsersGuide/Tutorial`, salvar o `.f3sav` e usá-lo como modelo de teste.
- [ ] Ajustar o `itasca` falso aos nomes reais encontrados.

**Pronto quando:** API da 6.0 mapeada e versões anotadas.

## Fase 1: extração (núcleo)
- [x] `01_extrair/extrair_campos.py`: zonas e gridpoints para `.npz` + `.json`, casando por id (mock).
- [ ] Conversão de unidades e sinal num único módulo (`comum/`).
- [ ] Pontos de controle por JSON ou planilha.
- [ ] Estado plástico e poropressão, se a 6.0 oferecer por array ou por zona.

**Pronto quando:** o valor de uma zona e de um gridpoint bate com o plot e o `zone list` do FLAC3D.

## Fase 2: gráficos e valores (fora do FLAC3D)
- [ ] Cortes com contorno (deslocamento, tensão, plastificação).
- [ ] Perfis ao longo de linhas: bacia de recalque, inclinômetro virtual, deslocamento sob a sapata.
- [ ] Valores: recalque máximo, distorção angular, deslocamento horizontal máximo, p e q.

**Pronto quando:** `VerificationProblems/SquareFooting` conferido.

## Fase 3: elementos estruturais
- [ ] Esforços de beam, pile, liner, shell, cable e geogrid; envoltórias de N, V e M.
- [ ] Força em tirantes e grampos ao longo do comprimento.
- [ ] Interfaces: tensões e deslizamento.

**Pronto quando:** os `check.f3dat` de `Structure` batem, começando por `Liner/EmbeddedRetainingWall`.

## Fase 4: estágios, histórias e FS
- [ ] Um `.f3sav` por estágio; incrementos entre fases.
- [ ] Histórias: unbalanced force ratio e pontos de controle; aviso de não convergência.
- [ ] Fator de segurança e curva carga × recalque com os critérios do plaxis3d-automacao.

**Pronto quando:** `AnchoredExcavation` conferido por estágio.

## Fase 5: lote e estudo paramétrico
- [ ] Todos os `.f3sav` de uma pasta, uma linha por modelo (Excel/CSV).
- [ ] Laço restore → muda propriedade → solve → extrai, sem parar na primeira falha.
- [ ] Gráfico de sensibilidade (tornado).

## Fase 6: VTK
- [ ] `.vtu` com malha e campos por zona, conferido no ParaView.

## Fase 7: relatório
- [ ] Excel/CSV consolidado e memorial HTML ou Word com figuras, unidades e convenção de sinais.

## Ideias futuras
- Criar modelos a partir de planilha, como no slide2-automacao.
- Comparar o cálculo analítico do cortina-e-muro com o FLAC3D.
- Retroanálise de parâmetros por instrumentação.

## Decisões tomadas
- Extração dentro do FLAC3D só com `itasca` + NumPy; gráficos, Excel e relatórios fora.
- `.npz` na convenção do FLAC3D (compressão negativa); resumos e gráficos na convenção geotécnica.
- Atributos sem função de array são lidos zona a zona e casados **pelo id**, nunca pela posição.
