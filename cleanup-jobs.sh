TARGET="dev";databricks jobs list -t $TARGET -o "json" | jq -r '.[].job_id' | while read -r job; do echo `databricks jobs delete $job -t $TARGET`; done
TARGET="prod"; databricks pipelines list-pipelines -t $TARGET -o "json" | jq -r '.[].pipeline_id' | while read -r pipeline; do echo `databricks pipelines delete $pipeline -t $TARGET`; done
