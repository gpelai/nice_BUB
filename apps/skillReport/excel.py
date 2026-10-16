from pathlib import Path
import pandas as pd 

def read_skill_ids(file_path: Path) -> list[int]:
    df = pd.read_excel(file_path)
    return df["skills_id"].dropna().astype(int).tolist()

def write_report(file_path: Path, data: list[dict]) -> None:
    df = pd.DataFrame(data)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(file_path, index=False)