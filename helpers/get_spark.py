# def init_spark():
#     import os

#     from databricks.connect import DatabricksSession

#     if "DATABRICKS_RUNTIME_VERSION" in os.environ:
#         spark = DatabricksSession.builder.getOrCreate()
#     else:
#         spark = DatabricksSession.builder.serverless().getOrCreate()
#     print(spark.conf.get("spark.databricks.workspaceUrl"))
#     print(spark.conf.get("spark.databricks.clusterUsageTags.clusterId"))
#     return spark


from datetime import datetime, timedelta

import polars as pl
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pyspark.sql.functions as F
from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, current_date, lit, sum, when


def dbcn_cfg():
    config = Config(cluster_id="<cluster_id>", profile="<profile>")
    return config


def init_spark():
    spark = DatabricksSession.builder.sdkConfig(dbcn_cfg()).getOrCreate()
    print(spark.conf.get("spark.databricks.workspaceUrl"))
    print(spark.conf.get("spark.databricks.clusterUsageTags.clusterId"))
    return spark
