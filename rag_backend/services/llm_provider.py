from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from rag_backend.core.config import settings

def get_llm():
    """for connecting llm with azure via key valut"""
    return AzureChatOpenAI(
        azure_deployment=settings.azure_openai_deployment_name,
        azure_endpoint=settings.get_secret("endpoint_secret_name"),
        api_key=settings.get_secret("key_secret_name"),
        api_version=settings.azure_openai_api_version,
        temperature=0,
    )

def get_embeddings():
    """for embedding"""
    return AzureOpenAIEmbeddings(
        azure_deployment=settings.azure_openai_embeddings_deployment_name,
        azure_endpoint=settings.get_secret("endpoint_secret_name"),
        api_key=settings.get_secret("key_secret_name"),
        api_version=settings.azure_openai_embeddings_api_version,
    )
