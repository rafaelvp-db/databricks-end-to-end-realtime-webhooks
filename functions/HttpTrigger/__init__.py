"""Main code for the Azure Function that will intereact with MLflow Webhooks.
    Authors:
        - Alex Ott
        - Rafael Pierre
"""

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

def create_error(msg):
    func.HttpResponse(msg, status_code=400)

def maybe_trigger_action(req_body):

    action = "None"

    try:

        to_stage = req_body["to_stage"]
        from_stage = req_body.get("from_stage", "")
        model_name = req_body.get("model_name", "")
        model_version = req_body.get("version", 0)
        wh_id = req_body["webhook_id"]
        timestamp = req_body["event_timestamp"]
        payload_text = req_body.get("text", "")

        credentials = BasicAuthentication('', ADO_PERSONAL_ACCESS_TOKEN)
        connection = Connection(base_url = ADO_ORGANIZATION_URL, creds = credentials)
        pipeline_client = connection.clients_v6_0.get_pipelines_client()
        pipeline_id = -1

        variables = {
            'model_name': Variable(value=model_name),
            'version': Variable(value=model_version),
            'webhook_id': Variable(value=wh_id),
            'timestamp': Variable(value=timestamp),
            'text': Variable(value=payload_text),
            'stage': Variable(value=to_stage)
        }
        run_parameters = RunPipelineParameters(variables=variables)
        logging.info("Going to trigger build with parameters: %s", run_parameters)

        if to_stage == "Staging" and not from_stage == "Production":
            logging.info("Going to trigger integration pipeline")
            pipeline_id = 3
            action = f"Integration test is triggered."

        if to_stage == "Production":
            logging.info("Going to trigger release pipeline")
            pipeline_id = 2
            action = "Deployment triggered."

        if pipeline_id != -1:
            logging.info(f"Running pipeline: {pipeline_id}")
            run_pipeline = pipeline_client.run_pipeline(
                run_parameters = run_parameters,
                project = ADO_PROJECT_NAME,
                pipeline_id=pipeline_id
            )

            action = action + f' Status: {run_pipeline}'
        
        logging.info(f"Action: {action}")
        

    except Exception as e:
        logging.error("Error: " + str(e))

    return action

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Entry point for the function code. Sample payload:
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
        return create_error("It should be POST request!")

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
        ret_str = ret_str + ". Action: " + maybe_trigger_action(req_body)

    logging.info(ret_str)
    return func.HttpResponse(ret_str)