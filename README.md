# MLflow Webhooks End-to-End Template
## Realtime Prediction Endpoints

## Motivation

* **[Databricks MLflow Webhooks](https://docs.databricks.com/applications/mlflow/model-registry-webhooks.html)** are a powerful new feature that allows customers to go to the next level in terms of MLOps best practices and CICD integration
* This repo aims on showcasing a sample use case where we deploy a realtime predicition endpoint.
* We consider a use case where a model was trained & tracked using Databricks & MLflow. With each model stage change, we want to trigger an *Azure DevOps** build pipeline, which will download the model artifacts from MLflow, buld a Docker container to package them and push this container to **Azure Container Registry**.
* It contains:
  * **Terraform IaC** code for creating all the infrastructure needed: MLflow Webhooks, Azure Functions, Azure Kubernetes Service clusters, Azure Container Registry
* Complete code for a **REST API** Docker container based on **FastAPI** in order to expose the model is also part of this repo
* **Helm Charts** for deploying the model on a Kubernetes cluster
* **CICD** pipelines for deploying a Python **Azure Function**, which acts as a Webhook listener


## Architecture

<img src="https://github.com/databricks/end-to-end-realtime-webhooks/blob/main/img/architecture.png?raw=true" />

## Workflow

<img src="https://github.com/databricks/end-to-end-realtime-webhooks/blob/main/img/workflow.png?raw=true" />

## Instructions

## Requirements
### Azure DevOps

* [Terraform](https://www.terraform.io/downloads)
* [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
* [Helm](https://helm.sh/)

### Other CICD Platforms

Coming soon!

## Deploying the Webhook and Azure Functions App Service Plan

1. Login with Azure CLI by running ```azure login```. Select the desired subscription.
2. Go to the ```terraform/webhooks``` directory.
3. Create a copy of ```terraform.tfvars.example``` and copy it to ```terraform.tfvars```.
4. Fill the correct values in ```terraform.tfvars```.
5. Run ```terraform plan```. You should see an overview of the resources that will be deployed.
6. If everything looks ok, run ```terraform deploy```. This will create an MLflow Webhook on our Databricks Workspace, along with creating some secondary infrastructure.
7. Go to the ```terraform/serving``` directory and run steps 4-7 once again. This will deploy the infrastructure for serving our model.
8. On your **Azure DevOps Project**, create a Build pipeline and point it to ```cicd/model/azure-pipelines.yaml```.
9. On your **Azure DevOps Project**, create a new Service Connection. For **type**, select **Docker Registry**. Select your Azure Subscription and the Azure Container Registry that was created with Terraform on step 8.
10. Create a variable for the Build Pipeline created on step 9 - name it **registryServiceConnection** and set the value to the service connection created on step 10
11. Create a variable for the Build Pipeline created on step 9 - name it **acrRegistryName** and set the value to the Azure Container Registry that was created by Terraform as part of step 8

## Deploying the Azure Function

1. On your **Azure DevOps Project**, create a Build pipeline and point it to ```cicd/functions/azure-pipelines.yaml```.
2. Go to **Library** and create a **Variable Group**. Choose the option to link with an existing Azure Key Vault. Look for the keyvault that was deploying with Terraform and select it. Select the secrets from the keyvault, so that they are imported into the variable group.
3. Run the Build pipeline to deploy our Azure Function.

You should be good to go! Once you change the Model stage to ```Production```, the MLflow Webhook will hopefully:

* Make a post request to the Azure Function you deployed
* This function will trigger the model build pipeline on Azure DevOps
* The pipeline will:
  * Download the model artifacts from MLflow Model Registry
  * Scan the Dockerfile for vulnerabilities
  * Build a Docker container
  * Push this Docker container into Azure Container Registry

#### Final Step

As a final step, you can deploy the container to AKS. To do so, from a terminal window:

1. Run ```make aks-install-cli``` to install Azure AKS Client and ```kubectl```
2. In the ```Makefile```, change RESOURCE_GROUP_NAME and AKS_CLUSTER_NAME accordingly. Then run ```make aks-login```.
3. Finally, run ```make helm-install``` (change ```mymodel``` accordingly as well)

### AWS / GCP
* Coming soon

## TODO-List

Please check the Issues. Feel free to contribute by solving them, or creating your first issue!

## Contributors

* [Alex Ott](https://github.com/alexott)
* [Rafael Pierre](https://github.com/rafaelvp-db)

## References

* [Azure Databricks Terraform Provider](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/terraform/azure-workspace)
* [Azure Pipelines Documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/?view=azure-devops)
* [MLflow Webhooks](https://docs.databricks.com/applications/mlflow/model-registry-webhooks.html)
* [Azure Kubernetes Services](https://azure.microsoft.com/en-us/services/kubernetes-service/)
* [Azure Container Registry](https://azure.microsoft.com/en-us/services/container-registry/)
* [Azure Machine Learning](https://azure.microsoft.com/en-us/services/machine-learning/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Helm Charts](https://helm.sh/)
