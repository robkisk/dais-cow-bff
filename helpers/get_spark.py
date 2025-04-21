def init_spark():
    import os

    from databricks.connect import DatabricksSession

    if "DATABRICKS_RUNTIME_VERSION" in os.environ:
        spark = DatabricksSession.builder.getOrCreate()
    else:
        spark = DatabricksSession.builder.serverless().getOrCreate()
    print(spark.conf.get("spark.databricks.workspaceUrl"))
    print(spark.conf.get("spark.databricks.clusterUsageTags.clusterId"))
    return spark
