"""
This module registers the data store.
"""
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import OneLakeDatastore, \
    OneLakeArtifact, ServicePrincipalConfiguration
from azure.ai.resources.client import AIClient
from azure.ai.resources.entities import Data
from azure.ai.resources.constants import AssetTypes
import os
import argparse
import json

pipeline_components = []

def get_aml_client(
        subscription_id,
        resource_group_name,
        workspace_name,
):
    aml_client = MLClient(
        DefaultAzureCredential(),
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        workspace_name=workspace_name,
    )

    client = AIClient(DefaultAzureCredential(),
                      subscription_id=subscription_id,
                      resource_group_name="copilot-microhack",
                      project_name="dataops-mango")

    #return aml_client
    return client

def register_data_store(
        name_datastore,
        description,
        onelake_workspace_name,
        onelake_endpoint,
        onelake_artifact_name,
        aml_client,
        client_id,
        client_secret
):

    #credentials_dict = json.loads(credentials)

    # Extract the client_id, client_secret and tenant_id
    #client_id = credentials_dict.get('clientId')
    #client_secret = credentials_dict.get('clientSecret')
    #tenant_id = "3c863c9b-2221-4236-88c3-37fe9e1d06f8"

    # store = OneLakeDatastore(
    #     name=name_datastore,
    #     description=description,
    #     one_lake_workspace_name=onelake_workspace_name,
    #     endpoint=onelake_endpoint,
    #     credentials=ServicePrincipalConfiguration(client_id=client_id,
    #                                               client_secret=client_secret,
    #                                               tenant_id=tenant_id),
    #     artifact=OneLakeArtifact(
    #     name=onelake_artifact_name,
    #     type="lake_house"
    # )
    # )
    #
    # aml_client.create_or_update(store)

    ## AI Client

    path = "https://onelake.dfs.fabric.microsoft.com/dataopstest/datalakehousetest.Lakehouse/source.csv"

    myfile = Data(
        name="my-file-test-source1",
        path=path,
        type=AssetTypes.FILE
    )

    aml_client.data.create_or_update(myfile)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--subscription_id",
        type=str,
        help="Azure subscription id",
        required=True,
    )
    parser.add_argument(
        "--resource_group_name",
        type=str,
        help="Azure resource group",
        required=True,
    )
    parser.add_argument(
        "--workspace_name",
        type=str,
        help="Azure ML workspace",
        required=True,
    )
    parser.add_argument(
        "--config_path_root_dir",
        type=str,
        help="Root dir for config file",
        required=True,
    )
    parser.add_argument(
        "--client_id",
        type=str,
        help="azure client id credentials",
        required=True,
    )

    parser.add_argument(
        "--client_secret",
        type=str,
        help="azure client secret credentials",
        required=True,
    )

    args = parser.parse_args()

    subscription_id = args.subscription_id
    resource_group_name = args.resource_group_name
    workspace_name = args.workspace_name
    config_path_root_dir = args.config_path_root_dir
    client_id = args.client_id
    client_secret = args.client_secret

    config_path = os.path.join(os.getcwd(), f"{config_path_root_dir}/configs/dataops_config.json")
    config = json.load(open(config_path))

    onelake_config = config['ONELAKE']
    onelake_workspace_name = onelake_config['WORKSPACE_NAME']
    onelake_endpoint = onelake_config['ENDPOINT']
    onelake_artifact_name = onelake_config['ARTIFACT_NAME']

    aml_client = get_aml_client(
        subscription_id,
        resource_group_name,
        workspace_name,
    )

    register_data_store(
        name_datastore=config["DATA_STORE_NAME"],
        description=config["DATA_STORE_DESCRIPTION"],
        onelake_workspace_name=onelake_workspace_name,
        onelake_endpoint=onelake_endpoint,
        onelake_artifact_name = onelake_artifact_name,
        aml_client=aml_client,
        client_id=client_id,
        client_secret=client_secret
    )

if __name__ == "__main__":
    main()
