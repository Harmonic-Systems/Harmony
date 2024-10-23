# pylint: disable=line-too-long
"""RAG user agent.
It extends a user agent and has RAG related parameters (`retrieve_config`).
"""

from pydantic import Field
from typing_extensions import Annotated, Literal

from ..agent import HarmonyAgent
from .rag_user_data import HarmonyRagUserData
from .retrieve_config import HarmonyRagUserRetrieveConfig


class HarmonyRagUser(HarmonyAgent):
    """RAG user agent.

    It extends a user agent and has RAG related parameters.

    Attributes
    ----------
    agent_type : Literal["rag_user"]
        The agent type: 'rag_user' for a RAG user agent.
    data : HarmonyRagUserData
        The RAG user agent's data.
        See `HarmonyRagUserData` for more info.
    retrieve_config : HarmonyRagUserRetrieveConfig
        The RAG user agent's retrieve config.
    """

    agent_type: Annotated[
        Literal["rag_user"],
        Field(
            "rag_user",
            title="Agent type",
            description="The agent type: 'rag_user' for a RAG user agent",
            alias="agentType",
        ),
    ]

    data: Annotated[
        HarmonyRagUserData,
        Field(
            title="Data",
            description="The RAG user agent's data",
            default_factory=HarmonyRagUserData,
        ),
    ]

    @property
    def retrieve_config(self) -> HarmonyRagUserRetrieveConfig:
        """Get the retrieve config.

        Returns
        -------
        HarmonyRagUserRetrieveConfig
            The RAG user agent's retrieve config.
        """
        return self.data.retrieve_config
