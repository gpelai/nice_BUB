from nice_auth.client import NiceClient
from nice_auth.config import NiceConfig
from apps.skillReport.client import SkillReportClient

from pathlib import Path
import pandas as pd


def main():
    # 0. carrega lista de skill
    file_path = Path(__file__).parent / "data" / "input" / "skillid_list.xlsx"
    df = pd.read_excel(file_path)
    skill_ids = df["skills_id"].dropna().astype(int).tolist()


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
    for skillid in skill_ids:
        result = report.get_summary(
            skillid,
            "2026-10-01",
            "2026-10-15"
        )
    
        # 6. Pega os dados desejados
        data = report.get_skillData(result["skillSummaries"])

        # 7. Mostra os dados
        print(data)


if __name__ == "__main__":
    main()




