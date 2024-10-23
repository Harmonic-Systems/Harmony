"""Assistant agent model."""

from pydantic import Field
from typing_extensions import Annotated, Literal

from ..agent import HarmonyAgent
from .assistant_data import HarmonyAssistantData


class HarmonyAssistant(HarmonyAgent):
    """Assistant agent model.

    A `HarmonyAgent` with agent_type `assistant` and
    default `human_input_mode`: `"NEVER"`
    See `HarmonyAgent`,`HarmonyAssistantData`,`HarmonyAgentData` for more info.

    Attributes
    ----------
    agent_type : Literal["assistant"]
        The agent type: 'assistant' for an assistant agent
    data : HarmonyAssistantData
        The assistant agent's data
    """

    agent_type: Annotated[
        Literal["assistant"],
        Field(
            "assistant",
            title="Agent type",
            description="The agent type in a graph: 'assistant'",
            alias="agentType",
        ),
    ]
    data: Annotated[
        HarmonyAssistantData,
        Field(
            title="Data",
            description="The assistant agent's data",
            default_factory=HarmonyAssistantData,
        ),
    ]
