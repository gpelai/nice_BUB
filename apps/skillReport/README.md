# Skill Report — NICE CXone

Aplicação do projeto **nice_BUB** para consultar indicadores consolidados de skills na API NICE CXone e exportar os resultados para Excel (`.xlsx`).

## O que faz

1. Lê os IDs das skills em `data/input/skillid_list.xlsx`.
2. Obtém um token de acesso usando os módulos compartilhados `nice_auth.config.NiceConfig` e `nice_auth.client.NiceClient`.
3. Consulta o resumo de cada skill na API NICE CXone para um intervalo de datas definido em `main.py`.
4. Extrai quatro campos da resposta e escreve uma planilha em `data/output/`.

Cada skill é consultada **sequencialmente**. O relatório é exportado **somente após** o término de todas as consultas.

## Estrutura do pacote

```text
apps/skillReport/
├── pyproject.toml           # Metadados e dependências específicas do subprojeto
├── main.py                  # Orquestra leitura, autenticação, consultas e exportação
├── client.py                # Cliente HTTP e seleção dos campos da resposta
├── excel.py                 # Leitura e escrita de planilhas
├── data/
│   ├── input/
│   │   ├── .gitkeep
│   │   └── skillid_list.xlsx  # Criado localmente; ignorado pelo Git
│   └── output/
│       ├── .gitkeep
│       └── skillReport_*.xlsx # Gerado localmente; ignorado pelo Git
└── README.md
```

> Os diretórios `input/` e `output/` são mantidos no repositório por meio dos arquivos `.gitkeep`. O conteúdo operacional dessas pastas deve permanecer fora do versionamento.

## Pré-requisitos

- Python 3.10 ou superior e `pip` disponíveis. As dependências diretas estão declaradas em `pyproject.toml`.
- Módulos compartilhados `nice_auth` disponíveis na raiz do projeto.
- Credenciais da NICE configuradas conforme exigido por `NiceConfig` (o projeto utiliza `.env`). Nunca versione credenciais ou tokens.
- Permissões de API para consultar os resumos das skills desejadas.

## Instalação das dependências (pyproject.toml)

O `pyproject.toml` localizado em `apps/skillReport/` descreve este subprojeto e as suas dependências diretas:

| Dependência | Uso |
|---|---|
| `httpx` | Consultas HTTP à API NICE CXone |
| `pandas` | Leitura e montagem das tabelas |
| `openpyxl` | Leitura e exportação de arquivos `.xlsx` pelo pandas |

Com o ambiente virtual do `nice_BUB` ativado, abra o PowerShell **na raiz do repositório** e execute:

```powershell
python -m pip install ./apps/skillReport
```

Esse comando instala as dependências declaradas e registra os metadados do subprojeto no ambiente. O `pyproject.toml` usa uma configuração de empacotamento **sem módulos Python**, pois os fontes ainda são executados diretamente do monorepo; os imports `nice_auth` e `apps.skillReport` **não são instalados por esse comando**. Portanto, a execução continua dependendo da estrutura de pastas original e de abrir o terminal na raiz do `nice_BUB`.

> Para um setup reprodutível de todo o monorepo, também devem ser instaladas as eventuais dependências próprias de `nice_auth` e de outros componentes. O TOML deste pacote não pretende substituí-las.

Para executar após a instalação:

```powershell
python -m apps.skillReport.main
```

Os limites de versão definidos no TOML permitem atualizações dentro das faixas indicadas; **não** equivalem a um lockfile com versões exatas.

## Preparar o arquivo de entrada

Crie `apps/skillReport/data/input/skillid_list.xlsx` com uma coluna chamada **exatamente** `skills_id`:

| skills_id |
|---:|
| 31517161 |
| 18595741 |
| 18506146 |

O programa lê a primeira planilha do arquivo, remove células vazias nessa coluna e converte os IDs para números inteiros. IDs com valores inválidos podem causar erro; mantenha apenas identificadores numéricos.

## Configurar o período

No início da função `main()` em `apps/skillReport/main.py`, ajuste as três variáveis:

```python
mon_name = "mai"
start_date = "2026-05-01"
end_date = "2026-05-31"
```

- `mon_name`: sufixo do arquivo de saída, por exemplo `skillReport_mai.xlsx`.
- `start_date`: data inicial da consulta (`AAAA-MM-DD`).
- `end_date`: data final da consulta (`AAAA-MM-DD`).

**Atenção:** `mon_name` apenas define o nome do arquivo; não altera automaticamente as datas consultadas. Ajuste os três valores de modo coerente antes de cada execução.

## Executar

Abra o PowerShell **na raiz do projeto** (`nice_BUB`), com o ambiente virtual configurado, e execute:

```powershell
python -m apps.skillReport.main
```

**Não execute `python main.py` dentro de `apps/skillReport/`**: os imports absolutos (`apps.skillReport` e `nice_auth`) pressupõem a execução a partir da raiz do projeto.

O script imprime no terminal as respostas da API recebidas durante a execução e cria, ao final, um arquivo como:

```text
apps/skillReport/data/output/skillReport_mai.xlsx
```

Se já existir um arquivo com o mesmo nome, a exportação atual o sobrescreve.

## Campos exportados

O método `SkillReportClient.get_skillData()` extrai os seguintes campos de `skillSummaries[0]`:

| Coluna | Descrição |
|---|---|
| `skillName` | Nome da skill |
| `contactsOffered` | Quantidade de contatos oferecidos |
| `contactsQueued` | Quantidade de contatos enfileirados |
| `contactsHandled` | Quantidade de contatos atendidos |

A saída contém uma linha por skill processada, desde que a API retorne ao menos um item em `skillSummaries`.

## API utilizada

```http
GET https://api-na1.niceincontact.com/incontactapi/services/v34.0/skills/{skill_id}/summary
```

Parâmetros de consulta: `startDate` e `endDate`. Autenticação via header `Authorization: Bearer <access_token>`.

O host `api-na1.niceincontact.com` e a versão `v34.0` estão definidos diretamente em `client.py`. Confira a adequação desses valores antes de reutilizar o pacote em outro ambiente.

Documentação oficial: [NICE CXone Developer Portal](https://developer.niceincontact.com/API).

## Limitações atuais e resolução de problemas

- **`ModuleNotFoundError: No module named 'apps'`**: execute o módulo a partir da raiz com `python -m apps.skillReport.main`.
- **`httpx.ReadTimeout`**: o tempo limite configurado em `client.py` é `120` segundos. Uma resposta lenta ainda pode esgotá-lo; aumentar o limite não garante solução.
- **HTTP 500**: a API pode falhar para uma skill específica. O código atual mostra o status e o corpo da resposta e interrompe a execução ao chamar `raise_for_status()`. Registre o ID, as datas e a resposta para investigação.
- **Resposta vazia (`skillSummaries: []`)**: a extração atual acessa a posição `[0]` e, portanto, gera erro se não houver registros.
- **Falha durante o processamento**: não há retry automático, captura individual de falhas nem salvamento parcial. Se qualquer consulta falhar, o arquivo de saída daquela execução pode não ser gerado.
- **Dados no terminal**: `main.py` imprime a resposta completa de cada consulta. Evite compartilhar logs sem revisar possíveis dados operacionais.

## Pontos de extensão

- Adicionar novas colunas: editar o dicionário retornado por `get_skillData()` em `client.py`.
- Alterar origem ou destino dos arquivos: editar `input_path` e `output_path` em `main.py`.
- Alterar a lógica de leitura e gravação Excel: editar `excel.py`.
- Evoluções sugeridas (ainda **não implementadas**): retry com intervalo progressivo, tratamento de erro por skill, aba de falhas, exportação incremental e parametrização de datas pela linha de comando.
