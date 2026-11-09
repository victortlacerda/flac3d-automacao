# flac3d-automacao

Automação do **Itasca FLAC3D 6.0** (6.00.69) por Python: extrai os resultados de modelos calculados e
gera gráficos, tabelas e valores calculados. Tudo gratuito e local: o Python embutido no FLAC3D e
bibliotecas livres (NumPy, matplotlib). Nenhuma API, token ou serviço externo na execução.

Segue o formato do [plaxis3d-automacao](https://github.com/victortlacerda/plaxis3d-automacao) e do
[slide2-automacao](https://github.com/victortlacerda/slide2-automacao).

## Como funciona

O Python roda **dentro** do FLAC3D, no mesmo processo do modelo (não há servidor nem porta, como no
PLAXIS). O projeto separa duas metades:

- **Dentro do FLAC3D** (só `itasca` + NumPy): ler o modelo e enviar comandos (`it.command`). Os
  extratores gravam `.npz` + `.json`.
- **Fora do FLAC3D** (Python 3.9+ comum): gráficos, cálculos, Excel e relatórios, lendo o `.npz`.

Assim a extração funciona mesmo que o Python da 6.0 não tenha matplotlib, e a parte externa é testada
no GitHub Actions sem o programa.

## Organização

| Pasta | O que é | Status |
| --- | --- | --- |
| [`00_descoberta/`](00_descoberta/) | Diagnóstico somente leitura: versão do Python, pacotes, API `itasca` da 6.0, modelo aberto | **Novo**: testado por mock, falta rodar no FLAC3D real |
| [`01_extrair/`](01_extrair/) | Zonas e gridpoints para `.npz` + resumo de valores calculados | **Novo**: testado por mock, **[não testado]** no FLAC3D |
| `02_graficos/` | Cortes, contornos, perfis, bacia de recalque, inclinômetro virtual | Planejado |
| `03_estruturas/` | Esforços em beam, pile, liner, shell, cable e geogrid; envoltórias | Planejado |
| `04_estagios_fs/` | Estágios, histórias, convergência, fator de segurança, carga × recalque | Planejado |
| `05_lote/` | Vários `.f3sav` e estudo paramétrico (restore → muda → solve → extrai) | Planejado |
| `06_vtk/` | Exportação `.vtu` para o ParaView | Planejado |
| `07_relatorio/` | Excel/CSV e memorial HTML ou Word | Planejado |
| [`tests/`](tests/) | Regressão por mock com `itasca` falso (roda **sem** o FLAC3D) | Ativo |
| [`docs/`](docs/) | Roadmap, referências e exemplos do fabricante usados na validação | — |

O roadmap completo está em [`docs/roadmap.md`](docs/roadmap.md).

## Como rodar (primeiro passo)

1. Abra o FLAC3D 6.0 com um modelo calculado (por exemplo, um do `datafiles\UsersGuide\Tutorial`).
2. Rode [`00_descoberta/diagnostico.py`](00_descoberta/README.md) no FLAC3D.
3. Envie o `diagnostico.json` gerado: ele define o que as próximas fases podem usar na sua versão.

## Testes (sem FLAC3D)

```bash
pip install numpy
./tests/regressao.sh            # compara com tests/baselines/
./tests/regressao.sh --gravar   # atualiza as linhas de base (só depois de revisar a mudança)
```

## Regras do projeto

- **Nada validado no FLAC3D real muda de comportamento.** Funções novas entram como opções, com
  padrão igual ao anterior; a regressão precisa continuar idêntica.
- Tudo que ainda não rodou no FLAC3D real fica marcado **[não testado]**, no script e no README.
- Scripts que rodam dentro do FLAC3D: compatíveis com Python 3.6 (conferido por `tests/compat36.py`),
  dependem só de `itasca` e NumPy, nunca abortam na primeira falha de leitura.
- Saídas em SI. O `.npz` guarda a convenção do FLAC3D (compressão negativa); resumos, tabelas e
  gráficos usam a convenção geotécnica (compressão e recalque positivos) e dizem isso no cabeçalho.

> **Responsabilidade técnica.** Os scripts aceleram a leitura dos resultados, mas não substituem a
> verificação do projetista. Confira os valores extraídos contra o próprio FLAC3D.
