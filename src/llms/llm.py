import os
from typing import Literal, Type

from src.config.agents import LLMType
from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel

from src.config.env import (
    LLM_PROVIDER,
    # OpenAI
    BASIC_API_KEY,
    BASIC_BASE_URL,
    BASIC_MODEL,
    REASONING_API_KEY,
    REASONING_BASE_URL,
    REASONING_MODEL,
    VL_API_KEY,
    VL_BASE_URL,
    VL_MODEL,
    # Azure
    AZURE_API_BASE,
    AZURE_API_KEY,
    AZURE_API_VERSION,
    BASIC_AZURE_DEPLOYMENT,
    VL_AZURE_DEPLOYMENT,
    REASONING_AZURE_DEPLOYMENT,
    # Groq
    GROQ_API_KEY,
    GROQ_MODEL,
    # Ollama
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
)


def get_llm_by_type(llm_type: LLMType) -> BaseChatModel:
    """Get the LLM for the given LLM type."""
    print(f"Getting LLM of type: {llm_type}")
    if LLM_PROVIDER == "azure":
        if llm_type == "reasoning":
            azure_deployment = REASONING_AZURE_DEPLOYMENT
        elif llm_type == "vision":
            azure_deployment = VL_AZURE_DEPLOYMENT
        else:
            azure_deployment = BASIC_AZURE_DEPLOYMENT

        return AzureChatOpenAI(
            azure_endpoint=AZURE_API_BASE,
            api_key=AZURE_API_KEY,
            api_version=AZURE_API_VERSION,
            azure_deployment=azure_deployment,
        )

    if LLM_PROVIDER == "groq":
        return ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
        )

    if LLM_PROVIDER == "ollama":
        return ChatOllama(
            base_url=OLLAMA_BASE_URL,
            model=OLLAMA_MODEL,
        )

    # Default to OpenAI
    if llm_type == "reasoning":
        model_name = REASONING_MODEL
        base_url = REASONING_BASE_URL
        api_key = REASONING_API_KEY
    elif llm_type == "vision":
        model_name = VL_MODEL
        base_url = VL_BASE_URL
        api_key = VL_API_KEY
    else:
        model_name = BASIC_MODEL
        base_url = BASIC_BASE_URL
        api_key = BASIC_API_KEY

    return ChatOpenAI(
        model_name=model_name,
        base_url=base_url,
        api_key=api_key,
    )