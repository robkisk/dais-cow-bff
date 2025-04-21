# Databricks notebook source
# COMMAND ----------

# MAGIC %pip install polars==1.6.0

# COMMAND ----------
# MAGIC %pip install -r ./requirements.txt


# COMMAND ----------

from datetime import datetime, timedelta

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import polars as pl
import pyspark.sql.functions as F
from pyspark.sql.functions import col, current_date, lit, sum, when
from pyspark.sql.window import Window

from helpers.get_spark import init_spark
from helpers.heatmap import compute_heatmap

spark = init_spark()

# COMMAND ----------
catalog_name = dbutils.widgets.get("catalog")
schema_name = dbutils.widgets.get("schema")

# COMMAND ----------
# catalog_name = "bu1_dev"
# schema_name = "proj1_schema"


# COMMAND ----------
# catalog_name = "bu1_dev"
# schema_name = "proj_schema1"  # make this break for run-repair with bundle deploy
table_name = f"{catalog_name}.{schema_name}.cows_bff"

# COMMAND ----------
cows_bff = spark.read.table(f"{table_name}")
cows_bff.show(5)

# COMMAND ----------

df = compute_heatmap(cows_bff)
display(df.limit(10))
df.show(10, False)

# COMMAND ----------
pdf = df.toPandas()
pdf = pdf.pivot(index="cow1", columns="cow2", values="closeness").fillna(0)

fig = px.imshow(
    pdf,
    x=pdf.columns,
    y=pdf.index,
    labels=dict(x="Cow 2", y="Cow 1", color="closeness"),
    title="Cow BFFs",
    color_continuous_scale="redor",
)
px.imshow(
    pdf,
    x=pdf.columns,
    y=pdf.index,
    labels=dict(x="Cow 2", y="Cow 1", color="closeness"),
)

# COMMAND ----------
fig.update_layout(width=800, height=500)
fig.show()

# %pip install -r ../requirements.txt
# COMMAND ----------
df.show()

# COMMAND ----------
