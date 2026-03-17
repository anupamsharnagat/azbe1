from pydantic_settings import BaseSettings
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import logging
import os
from dotenv import load_dotenv

# for loading .env
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Azure Key Vault Configuration
    key_vault_url: str | None = None
    endpoint_secret_name: str = "AzureOpenAIEndpoint"
    key_secret_name: str = "AzureOpenAIKey"
    
    # Direct Key Overrides (Pydantic will search environment/env_file automatically)
    azure_openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None

    # Deployment Names
    azure_openai_deployment_name: str = "gpt-4o-mini"
    azure_openai_embeddings_deployment_name: str = "text-embedding-3-large"
    
    # API Versions
    azure_openai_api_version: str = "2024-12-01-preview"
    azure_openai_embeddings_api_version: str = "2024-02-01"
    
    def get_secret(self, secret_name_attr: str) -> str:
        
        # if provided directly
        if "endpoint" in secret_name_attr.lower() and self.azure_openai_endpoint:
            return self.azure_openai_endpoint
        if "key" in secret_name_attr.lower() and self.azure_openai_api_key:
            return self.azure_openai_api_key

        # If not try Key Vault
        if not self.key_vault_url:
            logger.warning(f"No direct key for {secret_name_attr} and no KEY_VAULT_URL. Using placeholders.")
            return "mock-value-for-lab"

        secret_name = getattr(self, secret_name_attr)
        try:
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=self.key_vault_url, credential=credential)
            logger.info(f"Fetching '{secret_name}' from Key Vault...")
            return client.get_secret(secret_name).value
        except Exception as e:
            logger.error(f"Key Vault failed for '{secret_name}': {e}")
            return "fallback-mock-value"

    class Config:
        env_file = ".env"

settings = Settings()
