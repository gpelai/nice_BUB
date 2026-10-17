NICE BUB 🦇 — Automação e Integração de Operações NICE CXone

Ferramentas Python para automatizar processos, consultar indicadores operacionais e desenvolver integrações reutilizáveis com a plataforma NICE CXone.

Sobre o projeto

O NICE BUB (Batman Utility Belt) é um projeto pessoal de desenvolvimento voltado à criação de ferramentas para apoiar a administração e a operação de ambientes NICE CXone.

O projeto surgiu da proposta de reunir automações e integrações em um único lugar, permitindo reutilizar componentes técnicos e desenvolver novas soluções sem começar do zero.

Seu objetivo é explorar formas de reduzir atividades manuais, facilitar o acesso a informações operacionais e padronizar tarefas recorrentes.

Problemas que o projeto busca resolver

Em ambientes de contact center, atividades como consulta de indicadores, extração de relatórios e administração de configurações podem exigir tarefas repetitivas.

O NICE BUB busca oferecer ferramentas para:

* Automatizar consultas e extrações de dados do NICE CXone.
* Consolidar informações operacionais em arquivos estruturados.
* Reutilizar mecanismos de autenticação e comunicação com APIs.
* Facilitar o desenvolvimento de novas automações para operações NICE.

Soluções disponíveis

SkillReport — Extração de indicadores de skills

Ferramenta Python que consulta indicadores de múltiplas skills por meio da API NICE CXone e consolida os resultados em Excel.

Como funciona:

1. Recebe uma planilha contendo os identificadores das skills.
2. Autentica na plataforma e consulta os indicadores para o período configurado.
3. Consolida os resultados em uma planilha Excel.

Indicadores disponíveis:

* Nome da skill
* Contatos oferecidos
* Contatos enfileirados
* Contatos atendidos

Aplicação prática: apoiar análises operacionais e consultas de desempenho de múltiplas skills.

Documentação do SkillReport

Nice Auth — Autenticação reutilizável

Componente Python para centralizar a configuração de credenciais e a obtenção de tokens de acesso às APIs NICE CXone.

Benefício: permitir que diferentes ferramentas compartilhem uma implementação de autenticação, evitando duplicação de código.

Nice API — Em desenvolvimento

Estrutura inicial destinada à construção de componentes reutilizáveis para integração com APIs NICE.

Tecnologias

Tecnologia	Aplicação
Python 3.11+	Linguagem principal e requisito do pacote de autenticação
NICE CXone REST API	Integração com a plataforma
HTTPX	Comunicação HTTP
Pandas	Manipulação de dados
OpenPyXL	Leitura e geração de arquivos Excel
python-dotenv	Configuração de credenciais locais
Git e GitHub	Versionamento e organização do desenvolvimento

As versões e faixas de dependências específicas estão documentadas nos arquivos pyproject.toml de cada componente.

Arquitetura

O projeto utiliza uma estrutura modular com separação entre aplicações e componentes compartilhados.

nice_BUB/
├── apps/
│   └── skillReport/
│       ├── main.py
│       ├── client.py
│       ├── excel.py
│       └── README.md
├── packages/
│   ├── nice_auth/
│   └── nice_api/
├── .env.example
└── README.md

* apps/: aplicações que resolvem necessidades específicas.
* packages/: componentes compartilhados utilizados por diferentes aplicações.

Como executar

Exemplo para Windows PowerShell, a partir da raiz do repositório.

1. Clone o projeto e configure o ambiente Python

git clone https://github.com/gpelai/nice_BUB.git
cd nice_BUB
python -m venv .venv
.\.venv\Scripts\Activate.ps1

2. Instale as dependências e configure as credenciais

python -m pip install -e ./packages/nice_auth
python -m pip install httpx python-dotenv
python -m pip install ./apps/skillReport
Copy-Item .env.example .env

Preencha o arquivo .env com suas credenciais NICE CXone. Nunca publique credenciais ou tokens.

3. Prepare os dados e execute o SkillReport

Crie o arquivo apps/skillReport/data/input/skillid_list.xlsx com uma coluna skills_id. Configure o período em main.py e execute:

python -m apps.skillReport.main

A aplicação gera uma planilha no diretório apps/skillReport/data/output/.

Para detalhes, consulte a documentação específica do aplicativo.

Estado atual e próximos passos

O NICE BUB está em desenvolvimento incremental.

Implementado:

* Componente compartilhado de autenticação.
* Consulta de indicadores de múltiplas skills.
* Consolidação e exportação dos resultados para Excel.
* Organização modular de aplicações e bibliotecas.

Evoluções planejadas:

* Tratamento individual de falhas nas consultas.
* Mecanismos de retry e logging.
* Parametrização de períodos e ambientes.
* Ampliação das integrações com APIs NICE.
* Novas ferramentas de administração e automação.

Motivação

O NICE BUB combina conhecimentos de operações NICE CXone com desenvolvimento Python e integração de sistemas.

Além de produzir ferramentas úteis, o projeto funciona como um ambiente de estudo e experimentação de boas práticas de desenvolvimento, arquitetura e automação aplicadas ao ecossistema NICE.

⸻

Projeto pessoal e independente, sem vínculo oficial com a NICE.