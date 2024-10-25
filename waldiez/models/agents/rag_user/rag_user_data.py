"""Harmony RAG user agent data."""

from pydantic import Field
from typing_extensions import Annotated

from ..user_proxy import HarmonyUserProxyData
from .retrieve_config import HarmonyRagUserRetrieveConfig


class HarmonyRagUserData(HarmonyUserProxyData):
    """RAG user agent data.

    The data for a RAG user agent.

    Attributes
    ----------
    use_message_generator: bool
        Whether to use the message generator in user's chats. Defaults to False.
    retrieve_config : HarmonyRagUserRetrieveConfig
        The RAG user agent's retrieve config.

    """

    retrieve_config: Annotated[
        HarmonyRagUserRetrieveConfig,
        Field(
            title="Retrieve Config",
            description="The RAG user agent's retrieve config",
            default_factory=HarmonyRagUserRetrieveConfig,
            alias="retrieveConfig",
        ),
    ]
