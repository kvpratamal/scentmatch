"""Define the configurable parameters for the agent."""

from typing import Annotated, Literal
from pydantic import BaseModel, Field
import os

available_prods = [
    file[:-4]
    for file in os.listdir("products")
    if file.endswith(".txt") and file != "sales_prompt.txt"
]


class Configuration(BaseModel):
    """The configuration for the agent."""

    system_prompt: str = Field(
        default="You are a helpful AI assistant.",
        description="The system prompt to use for the agent's interactions. "
        "This prompt sets the context and behavior for the agent.",
    )

    model: Annotated[
        Literal[
            "google_genai:gemma-3-12b-it",
            "google_genai:gemma-3-27b-it",
            "google_genai:gemini-2.5-flash-lite-preview-06-17",
        ],
        {"__template_metadata__": {"kind": "llm"}},
    ] = Field(
        default="google_genai:gemma-3-12b-it",
        description="The name of the language model to use for the agent's main interactions. "
        "Should be in the form: provider/model-name.",
    )

    available_products: list[Literal[*available_prods]] = Field(
        default=available_prods,
        description="The list of product's names available for the agent to use.",
    )
