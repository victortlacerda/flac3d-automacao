# Instruções para o Claude neste repositório

Automação do FLAC3D 6.0 (6.00.69) por Python. Usuário: engenheiro geotécnico, português, UTC-3.

## Regras de ouro
1. Nada validado no FLAC3D real muda de comportamento. Função nova = opção com padrão igual ao anterior.
2. Provar a não regressão: `./tests/regressao.sh` precisa continuar idêntico (só `--gravar` depois de revisar).
3. Marcar **[não testado]** tudo que não rodou no FLAC3D real, no script, no README e na resposta.
4. Scripts que rodam DENTRO do FLAC3D (`00_descoberta/`, `01_extrair/`, e os extratores futuros):
   - compatíveis com Python 3.6 (sem f-strings; `tests/compat36.py` confere);
   - só `itasca` + NumPy; nada de matplotlib/openpyxl dentro;
   - começam com `it.command("python-reset-state false")`;
   - não abortam na primeira falha de leitura: registram e seguem.
5. Nomes da API da 6.0: usar o `diagnostico.json` do usuário (`docs/diagnostico_6.00.69.json` quando existir).
   Comandos FLAC3D desconhecidos: tirar dos `.f3dat` do fabricante (`docs/exemplos_fabricante.md`) ou do
   histórico de comandos do usuário. Nunca adivinhar.
6. Casar dados de zona/gridpoint **pelo id**, nunca pela posição na lista.
7. `.npz` na convenção do FLAC3D (compressão negativa); resumos, tabelas e gráficos na convenção
   geotécnica, com a convenção escrita no cabeçalho.
8. O `itasca` falso confere fluxo e cálculo, não a mecânica: manter `tests/fakes/itasca/` alinhado aos
   nomes reais conforme forem confirmados.
