"""User proxy agent model."""

from pydantic import Field
from typing_extensions import Annotated, Literal

from ..agent import HarmonyAgent
from .user_proxy_data import HarmonyUserProxyData


class HarmonyUserProxy(HarmonyAgent):
    """User proxy agent model.

    A `HarmonyAgent` with agent_type `user` and
    default `human_input_mode`: `"ALWAYS"`
    See `HarmonyAgent`,`HarmonyUserProxyData`,`HarmonyAgentData` for more info.

    Attributes
    ----------
    agent_type : Literal["user"]
        The agent type: 'user' for a user proxy agent
    data : HarmonyUserProxyData
        The user proxy agent's data
    """

    agent_type: Annotated[
        Literal["user"],
        Field(
            "user",
            title="Agent type",
            description="The agent type in a graph: 'user'",
            alias="agentType",
        ),
    ]
    data: Annotated[
        HarmonyUserProxyData,
        Field(
            title="Data",
            description="The user proxy agent's data",
            default_factory=HarmonyUserProxyData,
        ),
    ]
