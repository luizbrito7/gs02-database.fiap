"""Analise avancada: correlacao clima x focos e clusterizacao de municipios."""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

GOLD = Path("data/gold")
MIN_FOCOS = 10  # abaixo disso a densidade vira ruido (ex.: Areiopolis)
# nomes dados apos inspecionar o perfil de cada cluster (KMeans com random_state fixo)
PERFIS = {0: "Seca prolongada", 1: "Moderado", 2: "Hotspots", 3: "Baixo risco climatico", 4: "Fogo intenso"}
FEATURES = ["log_focos", "log_densidade", "frp_medio", "pct_risco_critico", "dias_sem_chuva_medio"]


def correlacao_clima() -> pd.DataFrame:
    b = pd.read_parquet(GOLD / "bioma_mes.parquet")
    linhas = []
    for bioma, g in b.groupby("bioma"):
        for var in ["dias_sem_chuva_medio", "precipitacao_media"]:
            rho, p = spearmanr(g[var], g["focos"])
            linhas.append({"bioma": bioma, "variavel": var, "spearman": rho, "p_valor": p})
    return pd.DataFrame(linhas)


def clusterizar() -> tuple[pd.DataFrame, dict]:
    m = pd.read_parquet(GOLD / "municipios.parquet")
    m = m[m["focos_total"] >= MIN_FOCOS].dropna(subset=["frp_medio", "pct_risco_critico", "dias_sem_chuva_medio"]).copy()
    m["log_focos"] = np.log1p(m["focos_total"])
    m["log_densidade"] = np.log1p(m["focos_por_1000km2"])
    X = StandardScaler().fit_transform(m[FEATURES])

    silhuetas = {k: silhouette_score(X, KMeans(k, n_init=10, random_state=42).fit_predict(X)) for k in range(2, 9)}
    k = max(silhuetas, key=silhuetas.get)
    m["cluster"] = KMeans(k, n_init=10, random_state=42).fit_predict(X)
    return m, silhuetas


if __name__ == "__main__":
    pd.set_option("display.width", 250)
    corr = correlacao_clima()
    print(corr.round(3).to_string(index=False))

    m, silhuetas = clusterizar()
    print("\nsilhueta por k:", {k: round(v, 3) for k, v in silhuetas.items()})
    perfil = m.groupby("cluster").agg(
        municipios=("municipio_id", "size"),
        focos_total=("focos_total", "sum"),
        focos_mediana=("focos_total", "median"),
        densidade_mediana=("focos_por_1000km2", "median"),
        frp_medio=("frp_medio", "median"),
        pct_risco_critico=("pct_risco_critico", "median"),
        dias_sem_chuva=("dias_sem_chuva_medio", "median"),
        bioma=("bioma_predominante", lambda s: s.mode().iat[0]),
    )
    print(perfil.round(1).to_string())

    corr.to_parquet(GOLD / "correlacao_clima.parquet", index=False)
    m["perfil"] = m["cluster"].map(PERFIS)
    m[["municipio_id", "municipio_nome", "cluster", "perfil"]].to_parquet(GOLD / "clusters.parquet", index=False)
