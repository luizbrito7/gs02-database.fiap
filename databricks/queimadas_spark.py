# Databricks notebook source
# MAGIC %md
# MAGIC # Queimadas: Silver e Gold em PySpark
# MAGIC Reprocessa parte do pipeline local (`silver.py` / `gold.py`) no Databricks.
# MAGIC Entrada: Parquets da Bronze enviados para o volume `workspace.default.queimadas`.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VOLUME IF NOT EXISTS workspace.default.queimadas

# COMMAND ----------

# MAGIC %md
# MAGIC Pare aqui: envie os 24 `2024xx/2025xx.parquet` e o `ibge_censo2022.parquet` para o volume
# MAGIC (New > Add or upload data > Upload files to a volume).

# COMMAND ----------

from pyspark.sql import functions as F

VOL = "/Volumes/workspace/default/queimadas"

bronze = spark.read.parquet(f"{VOL}/20*.parquet")
ibge = spark.read.parquet(f"{VOL}/ibge_censo2022.parquet")
print(bronze.count(), "focos na Bronze (todos os satelites)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver: filtro, tipagem e limpeza
# MAGIC O plano fisico (`explain`) mostra o filtro de satelite empurrado para a leitura do Parquet (*predicate pushdown*).

# COMMAND ----------

NUMERICAS = ["lat", "lon", "numero_dias_sem_chuva", "precipitacao", "risco_fogo", "frp"]

focos = bronze.filter(F.col("satelite") == "AQUA_M-T")
for c in NUMERICAS:
    v = F.trim(F.col(c)).cast("double")
    focos = focos.withColumn(c, F.when(v == -999, None).otherwise(v))
focos = (focos
         .withColumn("data_hora_gmt", F.to_timestamp("data_hora_gmt"))
         .withColumn("municipio_id", F.col("municipio_id").cast("int"))
         .drop("satelite", "pais", "pais_id")
         .dropDuplicates(["id"]))
focos.explain()

# COMMAND ----------

municipios = (ibge.groupBy(F.col("D1C").cast("int").alias("municipio_id"), F.col("D1N").alias("municipio_nome"))
              .pivot("D2C", ["93", "6318"])
              .agg(F.first(F.col("V").cast("double")))
              .withColumnRenamed("93", "populacao")
              .withColumnRenamed("6318", "area_km2"))

silver = focos.join(municipios, "municipio_id", "left")
silver.write.mode("overwrite").saveAsTable("workspace.default.silver_focos")
print(silver.count(), "focos na Silver | sem match IBGE:", silver.filter(F.col("populacao").isNull()).count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold: indicadores por municipio

# COMMAND ----------

agg = (spark.table("workspace.default.silver_focos")
       .withColumn("ano", F.year("data_hora_gmt"))
       .groupBy("municipio_id")
       .agg(F.count("*").alias("focos_total"),
            F.sum(F.when(F.col("ano") == 2024, 1).otherwise(0)).alias("focos_2024"),
            F.sum(F.when(F.col("ano") == 2025, 1).otherwise(0)).alias("focos_2025"),
            F.avg("frp").alias("frp_medio"),
            F.avg(F.when(F.col("risco_fogo") > 0.95, 100).otherwise(0)).alias("pct_risco_critico")))

gold = (municipios.join(agg, "municipio_id", "left")
        .fillna(0, ["focos_total", "focos_2024", "focos_2025"])
        .withColumn("focos_por_1000km2", F.col("focos_total") / F.col("area_km2") * 1000))
gold.write.mode("overwrite").saveAsTable("workspace.default.gold_municipios")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Consulta analitica em SQL sobre a Gold

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT municipio_nome, focos_2024, focos_2025,
# MAGIC        ROUND((focos_2025 - focos_2024) / NULLIF(focos_2024, 0) * 100, 1) AS var_pct,
# MAGIC        ROUND(focos_por_1000km2, 1) AS densidade
# MAGIC FROM workspace.default.gold_municipios
# MAGIC ORDER BY focos_total DESC
# MAGIC LIMIT 10
