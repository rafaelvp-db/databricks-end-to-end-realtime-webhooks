"""This module contains functionality for listening to MLflow Webhooks and interacting with
Azure DevOps"""

import logging
import os

import azure.functions as func

from msrest.authentication import BasicAuthentication
from azure.devops.connection import Connection
from azure.devops.v6_0.pipelines.models import RunPipelineParameters, Variable

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

ADO_PERSONAL_ACCESS_TOKEN = os.environ["ADO_PERSONAL_ACCESS_TOKEN"]
ADO_ORGANIZATION_URL = os.environ["ADO_ORGANIZATION_URL"]
ADO_PROJECT_NAME = os.environ["ADO_PROJECT_NAME"]

def _parse_mlflow_payload(request_body: dict):

    to_stage = request_body["to_stage"]
    from_stage = request_body.get("from_stage", "")
    model_name = request_body.get("model_name", "")
    model_version = request_body.get("version", 0)
    webhook_id = request_body["webhook_id"]
    timestamp = request_body["event_timestamp"]
    payload_text = request_body.get("text", "")

    variables = {
        'model_name': Variable(value=model_name),
        'version': Variable(value=model_version),
        'webhook_id': Variable(value=webhook_id),
        'timestamp': Variable(value=timestamp),
        'text': Variable(value=payload_text),
        'stage': Variable(value=to_stage)
    }

    return variables


def _get_action(request_body):

    variables = _parse_mlflow_payload(request_body)

    action = "None"
    credentials = BasicAuthentication('', ADO_PERSONAL_ACCESS_TOKEN)
    connection = Connection(base_url = ADO_ORGANIZATION_URL, creds = credentials)
    pipeline_client = connection.clients_v6_0.get_pipelines_client()
    pipeline_id = -1
    
    run_parameters = RunPipelineParameters(variables=variables)
    logging.info("Triggering build pipeline with parameters: %s", run_parameters)

    if to_stage == "Staging" and not from_stage == "Production":
        logging.info("Triggering integration pipeline")
        pipeline_id = 3
        action = f"Integration test is triggered"

    elif to_stage == "Production":
        logging.info("Triggering release pipeline")
        pipeline_id = 2
        action = "Deployment triggered"

    elif pipeline_id != -1:
        logging.info(f"Running pipeline: {pipeline_id}")
        run_pipeline = pipeline_client.run_pipeline(
            run_parameters = run_parameters,
            project = ADO_PROJECT_NAME,
            pipeline_id=pipeline_id
        )
        action = action + f' Status: {run_pipeline}'

    logging.info(f"Action: {action}")
    return action


def trigger(req: func.HttpRequest) -> func.HttpResponse:
    """
    Entry point for the Azure Function code. Sample payload:
        {
            "model_name": "test_model",
            "version": 1,
            "webhook_id": "my_id",
            "event_timestamp": "2022-03-04 00:00",
            "text": "it works!",
            "from_stage": "DEVELOPMENT",
            "to_stage": "PRODUCTION",
            "event": "MODEL_VERSION_TRANSITIONED_STAGE"
        }
    """
    logging.info('Python HTTP trigger function processed a request.')

    if (req.method != "POST"):
        logging.error('It should be POST request!')
        return create_error("Unsupported HTTP request \
            - please use a POST request")

    try:
        req_body = req.get_json()
        logging.info("Request body: %s", req_body)
    except ValueError:
        logging.error('Can\'t parse JSON payload')
        return create_error("Can't parse JSON payload")

    try:
        event = req_body["event"]
        model_name = req_body["model_name"]
        model_version = req_body["version"]
    except Exception:
        logging.error("Can't extract data from payload")
        return create_error("Can't extract data from payload")

    ret_str = f"Processing event: {event} for model {model_name} with version {model_version}"
    logging.info(ret_str)

    if event == "MODEL_VERSION_TRANSITIONED_STAGE":
        logging.info("Triggering model action")
        ret_str = ret_str + ". Action: " + _get_action(req_body)

    logging.info(ret_str)
    return func.HttpResponse(ret_str)