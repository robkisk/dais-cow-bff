# COMMAND ----------
import argparse
import os
import random
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import polars as pl
import pyspark.sql.functions as F
from pyspark.sql.functions import col, current_date, lit, sum, when
from pyspark.sql.window import Window

from helpers.get_spark import init_spark

# COMMAND ----------
spark = init_spark()


# # COMMAND ----------
# parser = argparse.ArgumentParser("simple_example")
# parser.add_argument("--catalog", help="Catalog to use", type=str)
# parser.add_argument("--schema", help="Schema to use", type=str)
# parser.add_argument("--envsubpath", help="sub_path to use", type=str)
# parser.add_argument("--container", help="container to use", type=str)
# parser.add_argument("--storageacct", help="storage account to use", type=str)
# args = parser.parse_args()
#
# catalog_name = str(args.catalog)
# schema_name = str(args.schema)
# envsubpath = str(args.envsubpath)
# container = str(args.container)
# storageacct = str(args.storageacct)
#
# COMMAND ----------
# debugging with dbconnect interactive jupyter only
# catalog_name = "bu1_dev"
# schema_name = "proj1_schema"
# adls_sub_path = "prod"
# container = "prod"
# storageacct = "storaccrobkisk"

# COMMAND ----------
# adls_root_path = f"abfss://prod@{storageacct}.dfs.core.windows.net"
table_name = "bu1_dev.default.cows_bff"
# tbl_sub_path = f"demo_folder_root/{envsubpath}/cows_bff"

# COMMAND ----------
# spark.sql(
#     f"CREATE CATALOG IF NOT EXISTS {catalog_name} MANAGED LOCATION '{adls_root_path}/demo_folder_root'"
# )
# spark.sql(
#     f"GRANT ALL PRIVILEGES ON catalog {catalog_name} TO `robby.kiskanyan@databricks.com`"
# )

# COMMAND ----------
# spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_name}")
# spark.sql(
#     f"GRANT ALL PRIVILEGES ON SCHEMA {catalog_name}.{schema_name} TO `robby.kiskanyan@databricks.com`"
# )

# COMMAND ----------

start_epoch = 1684540800
end_epoch = 1685620800
day = 86400

cows = [
    "Butterscotch",
    "Hershey",
    "Mocha",
    "Nutella",
    "Brandy",
    "Peaches",
    "Marshmallow",
    "Popcorn",
    "Muffin",
    "Daisy",
    "Buttercup",
    "Dottie",
    "Magic",
    "Nellie",
]

meal_1_start = 32400

# we will only focus on one meal
meal_2_start = 64800

meal_duration_start = -600
meal_duration_end = 2400


# COMMAND ----------
index = start_epoch
import calendar
import datetime

import pandas as pd

meal_data2 = None
data = []
while True:
    if index > end_epoch:
        break
    date = datetime.datetime.fromtimestamp(index)
    for cow in cows:
        r1 = random.randint(meal_duration_start, meal_duration_end)
        r2 = random.randint(meal_duration_start, meal_duration_end)
        begin = r1
        end = r2
        if r1 > r2:
            begin = r2
            end = r1
        meal_start_seconds = round(meal_1_start + begin)
        meal_end_seconds = round(meal_1_start + end)
        meal_data1 = {
            "cow_name": cow,
            "meal_start": meal_start_seconds,
            "meal_end": meal_end_seconds,
            "meal_start_time": str(datetime.timedelta(seconds=meal_start_seconds)),
            "meal_end_time": str(datetime.timedelta(seconds=meal_end_seconds)),
            "duration": meal_end_seconds - meal_start_seconds,
            "date": date,
            "day": calendar.day_name[date.weekday()],
        }
        data.append(meal_data1)
        # we cheat and add Mocha's best friend Cocoa
        if cow == "Mocha":
            cocoa_meal_start_seconds = round(
                meal_start_seconds - (random.randint(0, 500) / 10000.0)
            )
            cocoa_meal_end_seconds = round(
                meal_end_seconds - (random.randint(0, 500) / 10000.0)
            )
            meal_data2 = {
                "cow_name": "Cocoa",
                "meal_start": cocoa_meal_start_seconds,
                "meal_end": cocoa_meal_end_seconds,
                "meal_start_time": str(
                    datetime.timedelta(seconds=cocoa_meal_start_seconds)
                ),
                "meal_end_time": str(
                    datetime.timedelta(seconds=cocoa_meal_end_seconds)
                ),
                "duration": cocoa_meal_end_seconds - cocoa_meal_start_seconds,
                "date": date,
                "day": calendar.day_name[date.weekday()],
            }
            data.append(meal_data2)

    index = index + day
    df = pd.DataFrame(data)


spark_df = spark.createDataFrame(df)

# COMMAND ----------
# display(spark_df)
spark_df.show(10)

# # COMMAND ----------
# spark.sql("""
#           CREATE table prod_catalog.db.cows_bff
#           LOCATION 'abfss://dev-container@storageaccrobkisk.dfs.core.windows.net/demo_folder_root/cow_data'
#           """)

# spark_df.write.mode("overwrite").option("mergeSchema", "true").saveAsTable(
#     "dev_bu1.my_schema.cows_bff_managed"
# )

# COMMAND ----------
# create external table
spark_df.write.format("delta").mode("overwrite").option(
    "overwriteSchema", "true"
).saveAsTable(table_name)
# .option("path", f"{adls_root_path}/{tbl_sub_path}").saveAsTable(table_name)

# COMMAND ----------
spark.table(table_name).show(5)

# COMMAND ----------
