-- Datasets do AI/BI Dashboard (aba Data > Add SQL dataset). Um bloco por dataset.

-- 1. focos_ano: contadores 2024 x 2025
SELECT year(data_hora_gmt) AS ano, count(*) AS focos
FROM workspace.default.silver_focos
GROUP BY ALL;

-- 2. focos_bioma_mes: evolucao mensal por bioma
SELECT date_trunc('month', data_hora_gmt) AS mes, bioma, count(*) AS focos
FROM workspace.default.silver_focos
GROUP BY ALL;

-- 3. top_municipios: ranking por volume
SELECT municipio_nome, focos_2024, focos_2025, round(focos_por_1000km2, 1) AS densidade
FROM workspace.default.gold_municipios
ORDER BY focos_total DESC
LIMIT 15;

-- 4. mapa_municipios: um ponto por municipio (centro medio dos focos)
SELECT municipio, estado, avg(lat) AS lat, avg(lon) AS lon, count(*) AS focos
FROM workspace.default.silver_focos
GROUP BY ALL;

-- 5. perfis: municipios por cluster (clusters.parquet gerado por analise.py)
SELECT perfil, count(*) AS municipios
FROM read_files('/Volumes/workspace/default/queimadas/clusters.parquet')
GROUP BY ALL;
