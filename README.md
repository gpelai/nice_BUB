# NICE BUB - Batman Utility Belt🦇

**NICE BUB** (*Batman Utility Belt*) é um monorepo pessoal de ferramentas e componentes reutilizáveis para desenvolver soluções e automações integradas ao **NICE CXone**.

A ideia é simples: manter várias ferramentas em um único repositório, como um *cinto de utilidades*, sem misturar as regras de negócio de cada aplicação com funcionalidades que podem ser compartilhadas.

## Como o projeto é organizado

O BUB separa o código em dois grupos:

| Diretório | Papel | Como utilizar |
| --- | --- | --- |
| `packages/` | Bibliotecas reutilizáveis, como autenticação e clientes de API | Instale no ambiente Python e importe nos apps |
| `apps/` | Aplicações independentes para necessidades específicas | Consulte o README do app e execute seu ponto de entrada |

```text
nice_BUB/
├── apps/
│   └── skillReport/
│       ├── README.md          # Instruções específicas do app
│       ├── pyproject.toml     # Dependências do app
│       ├── main.py            # Ponto de entrada
│       ├── client.py
│       ├── excel.py
│       └── data/
│           ├── input/
│           └── output/
├── packages/
│   ├── nice_auth/
│   │   ├── pyproject.toml
│   │   ├── src/nice_auth/
│   │   └── tests/
│   └── nice_api/
│       ├── pyproject.toml
│       └── src/nice_api/
├── .env.example
├── .gitignore
└── README.md
```

> A árvore destaca os componentes principais. Cada app ou package pode evoluir com seus próprios testes, módulos e documentação.

## Componentes atuais

### Packages

- **`nice_auth`** — pacote compartilhado para ler credenciais do ambiente e solicitar um token de acesso ao NICE CXone.
- **`nice_api`** — estrutura inicial destinada a futuras funcionalidades reutilizáveis de integração com APIs NICE; ainda não possui uma implementação funcional documentada.

### Apps

| Aplicação | Objetivo | Documentação |
| --- | --- | --- |
| **SkillReport** | Consulta resumos de skills no NICE CXone e exporta os resultados para Excel | [README do SkillReport](apps/skillReport/README.md) |

**Regra de documentação:** o README da raiz apresenta o BUB. Configuração, parâmetros, formatos de entrada e saída, exemplos e limitações de cada ferramenta pertencem ao **README do próprio app**.

## Como começar

Os exemplos abaixo usam **PowerShell no Windows** e devem ser executados na raiz do repositório.

**1. Clone o projeto e entre na pasta:**

```powershell
git clone https://github.com/gpelai/nice_BUB.git
cd nice_BUB
```

**2. Crie e ative um ambiente virtual** (utilize Python **3.11 ou superior**, exigido pelo `nice_auth`):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Instale os packages compartilhados necessários:**

```powershell
python -m pip install -e ./packages/nice_auth
python -m pip install httpx python-dotenv
```

> Atualmente, o `pyproject.toml` de `nice_auth` não declara suas dependências de execução (`httpx` e `python-dotenv`), por isso elas são instaladas explicitamente acima. O diretório `nice_api` é apenas uma estrutura inicial e não precisa ser instalado para executar o SkillReport.

**4. Configure as credenciais da NICE:**

```powershell
Copy-Item .env.example .env
```

Preencha as variáveis no `.env` local:

```dotenv
NICE_CLIENT_ID=""
NICE_CLIENT_SECRET=""
NICE_ACCESS_KEY_ID=""
NICE_ACCESS_KEY_SECRET=""
```

Nunca inclua credenciais, tokens ou dados operacionais nos commits. O arquivo `.env` é ignorado pelo Git.

## Como usar os apps

Cada app define suas próprias dependências e procedimentos. O fluxo geral é:

1. Instalar os packages compartilhados de que ele depende.
2. Instalar as dependências declaradas no `pyproject.toml` do app, quando houver.
3. Seguir as configurações descritas no README do app.
4. Executar o módulo pela **raiz do repositório**, preservando os imports de `apps` e dos packages instalados.

**Exemplo — SkillReport:**

```powershell
python -m pip install ./apps/skillReport
python -m apps.skillReport.main
```

Para preparar o arquivo de entrada, configurar o período consultado e entender o relatório gerado, consulte o [README do SkillReport](apps/skillReport/README.md).

> O `pyproject.toml` do SkillReport declara suas dependências, mas não instala seus módulos como pacote independente; por isso, sua execução continua sendo feita a partir da raiz do monorepo.

## Como utilizar os packages

Um package reúne funcionalidades comuns, evitando copiar autenticação, clientes HTTP ou outras rotinas entre aplicações. Depois de instalado no ambiente virtual, seus módulos podem ser importados normalmente:

```python
from nice_auth.config import NiceConfig
from nice_auth.client import NiceClient
```

O app é responsável por combinar esses componentes de acordo com sua necessidade. Código genérico e reaproveitável deve ficar em `packages/`; regras e operações específicas de uma ferramenta devem ficar dentro do respectivo diretório em `apps/`.

## Como adicionar uma nova ferramenta

- Crie `apps/nomeDoApp/` com ponto de entrada, dependências e **README próprio**.
- Reutilize os packages existentes em vez de duplicar funções compartilhadas.
- Se surgir uma funcionalidade que faça sentido para vários apps, considere extraí-la para `packages/`.
- Não versione credenciais, planilhas de operação ou arquivos gerados.
- Organize mudanças com branches, issues e pull requests.

---

**Princípio do BUB:** aplicações separadas, componentes compartilhados e um único lugar para encontrar suas ferramentas NICE.
