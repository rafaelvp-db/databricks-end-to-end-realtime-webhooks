"""Helper functions for downloading model artifacts from MLflow"""

import logging
import os

from mlflow.tracking import MlflowClient

def download_artifacts(
  model_name: str = "mymodel",
  model_version: str = "myversion",
  local_artifact_dir: str = "ml_artifacts",
  remote_artifact_dir: str = "model"
):

    if "DATABRICKS_TOKEN" not in os.environ.keys():
        raise ValueError("Authentication error; No DBAPI Token")

    client = MlflowClient()
    logging.info(f"Token: {os.environ['DATABRICKS_TOKEN']}")
    remote_model_version = client.get_model_version(
        name = model_name,
        version = model_version
    )
    run_id = remote_model_version.run_id

    if not (os.path.exists(local_artifact_dir)):
        os.mkdirs(local_artifact_dir)

    local_path = client.download_artifacts(
        run_id,
        remote_artifact_dir,
        local_artifact_dir
    )
    full_path = f"{local_path}/{remote_artifact_dir}"
    logging.info(f"Artifacts downloaded in {full_path}: {os.listdir(full_path)}")