"""Gold: features e indicadores por municipio e por bioma/mes."""

from pathlib import Path

import pandas as pd

SILVER = Path("data/silver")
GOLD = Path("data/gold")
# Classes oficiais do Risco de Fogo INPE (RiscoFogo_Sucinto.pdf)
RISCO_BINS = [0, 0.15, 0.4, 0.7, 0.95, 1.0]
RISCO_CLASSES = ["minimo", "baixo", "medio", "alto", "critico"]


def features_foco(f: pd.DataFrame) -> pd.DataFrame:
    f["ano"] = f["data_hora_gmt"].dt.year
    f["ano_mes"] = f["data_hora_gmt"].dt.to_period("M").astype(str)
    f["classe_risco"] = pd.cut(f["risco_fogo"], RISCO_BINS, labels=RISCO_CLASSES, include_lowest=True)
    f["risco_critico"] = f["classe_risco"] == "critico"
    return f


def por_municipio(f: pd.DataFrame, mun: pd.DataFrame) -> pd.DataFrame:
    agg = f.groupby("municipio_id").agg(
        focos_total=("id", "size"),
        frp_medio=("frp", "mean"),
        dias_sem_chuva_medio=("numero_dias_sem_chuva", "mean"),
        pct_risco_critico=("risco_critico", "mean"),
        bioma_predominante=("bioma", lambda s: s.mode().iat[0]),
    )
    anual = f.pivot_table(index="municipio_id", columns="ano", values="id", aggfunc="size", fill_value=0)
    anual.columns = [f"focos_{a}" for a in anual.columns]

    g = mun.merge(agg, on="municipio_id", how="left").merge(anual, on="municipio_id", how="left")
    cols_focos = ["focos_total", "focos_2024", "focos_2025"]
    g[cols_focos] = g[cols_focos].fillna(0).astype(int)
    g["focos_por_1000km2"] = g["focos_total"] / g["area_km2"] * 1000
    g["focos_por_100mil_hab"] = g["focos_total"] / g["populacao"] * 100_000
    g["var_anual_pct"] = (g["focos_2025"] - g["focos_2024"]) / g["focos_2024"].where(g["focos_2024"] > 0) * 100
    g["pct_risco_critico"] *= 100
    return g


def por_bioma_mes(f: pd.DataFrame) -> pd.DataFrame:
    return f.groupby(["bioma", "ano_mes"], as_index=False).agg(
        focos=("id", "size"),
        frp_medio=("frp", "mean"),
        precipitacao_media=("precipitacao", "mean"),
        dias_sem_chuva_medio=("numero_dias_sem_chuva", "mean"),
    )


if __name__ == "__main__":
    GOLD.mkdir(parents=True, exist_ok=True)
    f = features_foco(pd.read_parquet(SILVER / "focos.parquet"))
    mun = pd.read_parquet(SILVER / "municipios.parquet")

    g_mun = por_municipio(f, mun)
    g_bioma = por_bioma_mes(f)
    g_mun.to_parquet(GOLD / "municipios.parquet", index=False)
    g_bioma.to_parquet(GOLD / "bioma_mes.parquet", index=False)

    print(f"gold municipios: {len(g_mun)} | bioma_mes: {len(g_bioma)}")
    print(f"soma focos confere com silver: {g_mun['focos_total'].sum() == len(f)}")
