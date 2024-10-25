"""Harmony flow data."""

from typing import Any, Dict, List

from pydantic import Field
from typing_extensions import Annotated

from ..agents import HarmonyAgents
from ..chat import HarmonyChat
from ..common import HarmonyBase
from ..model import HarmonyModel
from ..skill import HarmonySkill


class HarmonyFlowData(HarmonyBase):
    """Flow data class.

    Attributes
    ----------
    nodes : List[Dict[str, Any]]
        The nodes of the flow. We ignore this (UI-related)
    edges : List[Dict[str, Any]]
        The edges of the flow. We ignore this (UI-related)
    viewport : Dict[str, Any]
        The viewport of the flow. We ignore this (UI-related)
    agents : HarmonyAgents
        The agents of the flow:
        users: List[HarmonyUserProxy]
        assistants: List[HarmonyAssistant]
        managers: List[HarmonyGroupManager]
        rag_users : List[HarmonyRagUser]
        See `HarmonyAgents` for more info.
    models : List[HarmonyModel]
        The models of the flow. See `HarmonyModel`.
    skills : List[HarmonySkill]
        The skills of the flow. See `HarmonySkill`.
    chats : List[HarmonyChat]
        The chats of the flow. See `HarmonyChat`.
    """

    # the ones below (nodes,edges, viewport) we ignore
    # (they for graph connections, positions, etc.)
    nodes: Annotated[
        List[Dict[str, Any]],
        Field(default_factory=list),
    ]
    edges: Annotated[
        List[Dict[str, Any]],
        Field(default_factory=list),
    ]
    viewport: Annotated[
        Dict[str, Any],
        Field(default_factory=dict),
    ]
    # these are the ones we use.
    agents: Annotated[
        HarmonyAgents,
        Field(
            description="The agents of the flow",
            title="Agents",
            default_factory=HarmonyAgents,
        ),
    ]
    models: Annotated[
        List[HarmonyModel],
        Field(
            description="The models of the flow",
            title="Models",
            default_factory=list,
        ),
    ]
    skills: Annotated[
        List[HarmonySkill],
        Field(
            description="The skills of the flow",
            title="Skills",
            default_factory=list,
        ),
    ]
    chats: Annotated[
        List[HarmonyChat],
        Field(
            description="The chats of the flow",
            title="Chats",
            default_factory=list,
        ),
    ]
