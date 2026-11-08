"""Bronze: copia fiel das fontes (INPE focos mensais + IBGE Censo 2022) em Parquet."""

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

INPE_URL = "https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/mensal/Brasil/focos_mensal_br_{ym}.csv"
IBGE_URL = "https://apisidra.ibge.gov.br/values/t/4714/n6/all/v/93,6318,614/p/2022"
MESES = [f"{ano}{mes:02d}" for ano in (2024, 2025) for mes in range(1, 13)]
BRONZE = Path("data/bronze")


def com_linhagem(df: pd.DataFrame, fonte: str) -> pd.DataFrame:
    df["_fonte"] = fonte
    df["_ingerido_em"] = datetime.now(timezone.utc).isoformat()
    return df


def ingerir_inpe() -> None:
    destino = BRONZE / "inpe_focos"
    destino.mkdir(parents=True, exist_ok=True)
    for ym in MESES:
        arquivo = destino / f"{ym}.parquet"
        if arquivo.exists():
            continue
        url = INPE_URL.format(ym=ym)
        df = pd.read_csv(url, dtype=str, engine="pyarrow")
        com_linhagem(df, url).to_parquet(arquivo, index=False)
        print(f"inpe {ym}: {len(df)} linhas")


def ingerir_ibge() -> None:
    BRONZE.mkdir(parents=True, exist_ok=True)
    arquivo = BRONZE / "ibge_censo2022.parquet"
    if arquivo.exists():
        return
    df = pd.read_json(IBGE_URL, dtype=str).iloc[1:]  # 1a linha = cabecalho descritivo
    com_linhagem(df, IBGE_URL).to_parquet(arquivo, index=False)
    print(f"ibge: {len(df)} linhas")


if __name__ == "__main__":
    ingerir_ibge()
    ingerir_inpe()
