"""Silver: filtra satelite de referencia, tipa, limpa e integra INPE + IBGE."""

from pathlib import Path

import numpy as np
import pandas as pd

BRONZE = Path("data/bronze")
SILVER = Path("data/silver")
SATELITE_REF = "AQUA_M-T"  # serie historica oficial do INPE
SENTINELA = -999  # valor do INPE para "sem dado"
NUMERICAS = ["lat", "lon", "numero_dias_sem_chuva", "precipitacao", "risco_fogo", "frp"]


def municipios() -> pd.DataFrame:
    raw = pd.read_parquet(BRONZE / "ibge_censo2022.parquet")
    df = raw.pivot(index=["D1C", "D1N"], columns="D2C", values="V").reset_index()
    df = df.rename(columns={"D1C": "municipio_id", "D1N": "municipio_nome",
                            "93": "populacao", "6318": "area_km2", "614": "densidade"})
    df["municipio_id"] = df["municipio_id"].astype(int)
    df["populacao"] = df["populacao"].astype(int)
    df[["densidade", "area_km2"]] = df[["densidade", "area_km2"]].astype(float)
    return df


def focos() -> pd.DataFrame:
    df = pd.read_parquet(BRONZE / "inpe_focos", filters=[("satelite", "==", SATELITE_REF)])
    df[NUMERICAS] = df[NUMERICAS].apply(lambda s: pd.to_numeric(s.str.strip())).replace(SENTINELA, np.nan)
    df["data_hora_gmt"] = pd.to_datetime(df["data_hora_gmt"])
    df["municipio_id"] = df["municipio_id"].astype(int)
    return df.drop(columns=["satelite", "pais", "pais_id"]).drop_duplicates("id")


if __name__ == "__main__":
    SILVER.mkdir(parents=True, exist_ok=True)
    mun = municipios()
    f = focos().merge(mun[["municipio_id", "populacao", "area_km2"]], on="municipio_id", how="left")

    print(f"focos: {len(f)} | municipios IBGE: {len(mun)}")
    print(f"sem match no IBGE: {f['populacao'].isna().sum()}")
    print("nulos:", f[["numero_dias_sem_chuva", "precipitacao", "risco_fogo"]].isna().sum().to_dict())

    mun.to_parquet(SILVER / "municipios.parquet", index=False)
    f.to_parquet(SILVER / "focos.parquet", index=False)
