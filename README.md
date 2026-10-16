# nice_BUB — NICE Batman Utility Belt 🦇

A personal, modular Python toolkit for building and organizing integrations, automations, and reporting solutions for **NICE CXone**.

The project follows a **monorepo** approach: reusable libraries live in `packages/`, while executable solutions live in `apps/`. Each application may maintain its own dependencies, data folders, and documentation.

> **Project status:** Early development. The repository currently contains a working authentication package and a skill reporting application, plus a placeholder package for future NICE API utilities.

## Current modules

| Component | Location | Purpose | Status |
| --- | --- | --- | --- |
| **nice_auth** | [`packages/nice_auth/`](packages/nice_auth/) | Loads NICE credentials from environment variables and requests an access token. | Implemented |
| **skillReport** | [`apps/skillReport/`](apps/skillReport/) | Queries NICE skill summaries by date range and exports selected metrics to Excel. | Implemented (basic workflow) |
| **nice_api** | [`packages/nice_api/`](packages/nice_api/) | Reserved for shared NICE API utilities. | Scaffold only; no public functionality yet |

For detailed input format, configuration, API endpoint, output columns, and troubleshooting, see **[skillReport documentation](apps/skillReport/README.md)**.

## Repository layout

```text
nice_BUB/
├── .env.example                    # Environment variable template
├── .gitignore
├── README.md                       # This guide
├── packages/
│   ├── nice_auth/
│   │   ├── pyproject.toml
│   │   ├── src/nice_auth/
│   │   │   ├── __init__.py
│   │   │   ├── config.py           # NiceConfig
│   │   │   └── client.py           # NiceClient
│   │   └── tests/test_config.py
│   └── nice_api/
│       ├── pyproject.toml          # Currently empty
│       └── src/nice_api/__init__.py
└── apps/
    ├── __init__.py
    └── skillReport/
        ├── README.md
        ├── pyproject.toml
        ├── main.py
        ├── client.py
        ├── excel.py
        └── data/
            ├── input/.gitkeep
            └── output/.gitkeep
```

## Getting started (Windows / PowerShell)

### 1. Clone the repository

```powershell
git clone https://github.com/gpelai/nice_BUB.git
cd nice_BUB
```

### 2. Create and activate a virtual environment

Use **Python 3.11 or newer** (required by `nice_auth`).

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

If you already have a compatible Python selected, you can use `python -m venv .venv` instead.

### 3. Install the shared authentication package and application dependencies

Run these commands **from the repository root**:

```powershell
python -m pip install -e ./packages/nice_auth
python -m pip install ./apps/skillReport
python -m pip install python-dotenv
```

Why three commands?

- `nice_auth` is an installable package using a `src/` layout. An editable install makes its imports available while developing.
- `skillReport` declares `httpx`, `pandas`, and `openpyxl` in its own `pyproject.toml`. Its configuration currently installs dependencies/metadata only, **not** `apps.skillReport` as an importable distribution.
- `nice_auth` imports `dotenv`, but its current `pyproject.toml` does **not** declare `python-dotenv`; install it explicitly until that packaging metadata is updated.

The repository currently has **no root-level dependency manifest**, so there is not yet a single command that installs every project component.

### 4. Configure NICE credentials

Copy the environment template:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and supply the values for:

```dotenv
NICE_CLIENT_ID="your-client-id"
NICE_CLIENT_SECRET="your-client-secret"
NICE_ACCESS_KEY_ID="your-access-key-id"
NICE_ACCESS_KEY_SECRET="your-access-key-secret"
```

`NiceConfig` reads these through `python-dotenv` and raises an error if any are missing.

**Security:** never commit `.env`, access tokens, or operational/customer data. The `.env` file is excluded by `.gitignore`. Credentials must have the API permissions required for the intended action.

## Using the modules

### `nice_auth` — shared authentication

The package exposes two classes:

- `NiceConfig`: reads and validates the four environment variables above.
- `NiceClient`: uses those credentials to request an access token from the NICE authentication endpoint.

Example (from the repository root, after installation and `.env` setup):

```python
from nice_auth.config import NiceConfig
from nice_auth.client import NiceClient

config = NiceConfig()
client = NiceClient(
    client_id=config.client_id,
    client_secret=config.client_secret,
    access_key_id=config.access_key_id,
    access_key_secret=config.access_key_secret,
)
access_token = client.get_accessToken()
```

**Current limitation:** token retrieval does not yet provide robust HTTP error handling or token refresh management. Validate that a token was returned before using it for other API requests.

### `skillReport` — Excel skill summary reports

**Input:** Create `apps/skillReport/data/input/skillid_list.xlsx` with a column named exactly `skills_id` containing numeric skill IDs.

Example:

| skills_id |
| ---: |
| 31517161 |
| 18595741 |

**Date range:** Adjust `mon_name`, `start_date`, and `end_date` at the beginning of `apps/skillReport/main.py`. The month label only names the output file; it does not set the dates automatically.

**Run from the repository root:**

```powershell
python -m apps.skillReport.main
```

**Output:** `apps/skillReport/data/output/skillReport_<month>.xlsx`, containing `skillName`, `contactsOffered`, `contactsQueued`, and `contactsHandled` for the successfully retrieved summaries.

**Current limitations:** sequential requests; no automatic retry, individual failure recovery, or partial export. An HTTP error or empty `skillSummaries` may interrupt execution before writing the Excel file. A same-named output file is overwritten.

Full guide: **[apps/skillReport/README.md](apps/skillReport/README.md)**.

### `nice_api` — planned shared utilities

The `packages/nice_api/` directory exists as an initial scaffold, but its `pyproject.toml` and module initializer are currently empty. It is **not yet a usable client library**. Add utilities here as the shared abstraction becomes necessary; do not assume it is installable or functional today.

## Tests

A credential configuration test suite exists at `packages/nice_auth/tests/test_config.py`.

To run it, first install the test runner:

```powershell
python -m pip install pytest
python -m pytest packages/nice_auth/tests
```

This covers environment-variable configuration, **not** live NICE authentication or the skill reporting workflow.

## Working with the monorepo

- **Shared integrations and utilities:** place reusable code in `packages/` and define its packaging metadata/dependencies.
- **Independent tasks and business tools:** place executable applications in `apps/`; include a dedicated README and, where useful, a `pyproject.toml`.
- **Execution:** for modules under `apps/`, launch with `python -m apps.<app_name>.main` from the repository root when absolute imports rely on that layout.
- **Data:** keep generated reports, input spreadsheets, credentials, and sensitive data outside Git. The skill report preserves empty `data/input` and `data/output` directories using `.gitkeep`.
- **Delivery:** work on feature branches, open an issue, reference it in the pull request (`Closes #N`), and merge after reviewing changes.

## Roadmap ideas (not implemented)

- Centralized authentication lifecycle, including refresh/retry logic.
- Standard reusable HTTP clients, pagination, error handling, and throttling.
- Per-skill error tracking and resumable/partial exports.
- Automated tests for API clients and Excel operations.
- A root workspace/dependency strategy as more applications are added.

## Links

- [GitHub repository](https://github.com/gpelai/nice_BUB)
- [SkillReport documentation](apps/skillReport/README.md)
- [NICE CXone Developer Portal](https://developer.niceincontact.com/API)

---

This README describes the repository state reviewed on **2026-10-16**. Consult each component's source and documentation for subsequent changes.
