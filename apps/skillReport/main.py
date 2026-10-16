from nice_auth.client import NiceClient
from nice_auth.config import NiceConfig
from apps.skillReport.client import SkillReportClient

from pathlib import Path
from apps.skillReport.excel import read_skill_ids, write_report

# import pandas as pd


def main():
    # VARS
    mon_name = "mai"
    start_date = "2026-05-01"
    end_date = "2026-05-31"

    # PATHS
    base_path = Path(__file__).parent
    input_path =  base_path / "data" / "input" / "skillid_list.xlsx"
    output_path = base_path / "data" / "output" / f"skillReport_{mon_name}.xlsx"

    # # 0. carrega lista de skill
    skill_ids = read_skill_ids(input_path)

    # 1. Carregar credenciais do .env
    config = NiceConfig()

    # 2. Criar uma instância de NiceClient
    auth = NiceClient(
        client_id=config.client_id,
        client_secret=config.client_secret,
        access_key_id=config.access_key_id,
        access_key_secret=config.access_key_secret
    )

    # 3. Obter o access_token
    access_token = auth.get_accessToken()

    # 4. Criar uma instância de SkillReportClient
    report = SkillReportClient(access_token)

    # 5. Executar get_summary()
    results = []

    for skillid in skill_ids:
        result = report.get_summary(
            skillid,
            start_date,
            end_date
        )

        print(result)
    
        # 6. Pega os dados desejados
        data = report.get_skillData(result["skillSummaries"])

        # 7. Guarda results
        results.append(data)

    # 7. Escreve excel com os dados
    write_report(output_path, results)


if __name__ == "__main__":
    main()




