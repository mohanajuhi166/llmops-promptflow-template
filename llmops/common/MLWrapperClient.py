from azure.ai.ml import MLClient
from azure.ai.resources.client import AIClient
from azure.identity import DefaultAzureCredential


class MLWrapperClient:
    def __init__(self, config, service_type):
        self.config = config
        self.service_type = service_type

        if service_type == "AISTUDIO":
            self.ml_client = AIClient(
                subscription_id=config.subscription_id,
                resource_group_name=config.resource_group_name,
                project_name=config.workspace_name,
                credential=DefaultAzureCredential(),
            )
        else:
            self.ml_client = MLClient(
                subscription_id=config.subscription_id,
                resource_group_name=config.resource_group_name,
                workspace_name=config.workspace_name,
                credential=DefaultAzureCredential(),
            )

    def get_ml_client(self):
        return self.ml_client
