from typing import Optional

from langchain.llms.base import BaseLanguageModel
from langchain_openai import AzureChatOpenAI

from langflow import CustomComponent


class AzureChatOpenAIComponent(CustomComponent):
    display_name: str = "AzureOpenAI Model"
    description: str = "Generate text using LLM model from Azure OpenAI."
    documentation: str = (
        "https://python.langchain.com/docs/integrations/llms/azure_openai"
    )
    beta = False

    AZURE_OPENAI_MODELS = [
        "gpt-35-turbo",
        "gpt-35-turbo-16k",
        "gpt-35-turbo-instruct",
        "gpt-4",
        "gpt-4-32k",
        "gpt-4-vision",
    ]

    AZURE_OPENAI_API_VERSIONS = [
        "2023-03-15-preview",
        "2023-05-15",
        "2023-06-01-preview",
        "2023-07-01-preview",
        "2023-08-01-preview",
        "2023-09-01-preview",
        "2023-12-01-preview",
    ]

    def build_config(self):
        return {
            "model": {
                "display_name": "Model Name",
                "value": self.AZURE_OPENAI_MODELS[0],
                "options": self.AZURE_OPENAI_MODELS,
                "required": True,
            },
            "azure_endpoint": {
                "display_name": "Azure Endpoint",
                "required": True,
                "info": "Your Azure endpoint, including the resource.. Example: `https://example-resource.azure.openai.com/`",
            },
            "azure_deployment": {
                "display_name": "Deployment Name",
                "required": True,
            },
            "api_version": {
                "display_name": "API Version",
                "options": self.AZURE_OPENAI_API_VERSIONS,
                "value": self.AZURE_OPENAI_API_VERSIONS[-1],
                "required": True,
                "advanced": True,
            },
            "api_key": {"display_name": "API Key", "required": True, "password": True},
            "temperature": {
                "display_name": "Temperature",
                "value": 0.7,
                "field_type": "float",
                "required": False,
            },
            "max_tokens": {
                "display_name": "Max Tokens",
                "value": 1000,
                "required": False,
                "field_type": "int",
                "advanced": True,
                "info": "Maximum number of tokens to generate.",
            },
            "code": {"show": False},
            "input_value": {"display_name": "Input"},
            "stream": {
                "display_name": "Stream",
                "info": "Stream the response from the model.",
            },
        }

    def build(
        self,
        model: str,
        azure_endpoint: str,
        input_value: str,
        azure_deployment: str,
        api_key: str,
        api_version: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = 1000,
        stream: bool = False,
    ) -> BaseLanguageModel:
        try:
            output = AzureChatOpenAI(
                model=model,
                azure_endpoint=azure_endpoint,
                azure_deployment=azure_deployment,
                api_version=api_version,
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except Exception as e:
            raise ValueError("Could not connect to AzureOpenAI API.") from e
        if stream:
            result = output.stream(input_value)
        else:
            message = output.invoke(input_value)
            result = message.content if hasattr(message, "content") else message
            self.status = result
        return result
