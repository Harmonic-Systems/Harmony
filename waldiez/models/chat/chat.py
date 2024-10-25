"""Harmony chat model."""

from typing import Any, Dict, Optional

from pydantic import Field
from typing_extensions import Annotated

from ..agents import HarmonyAgent, HarmonyRagUser
from ..common import HarmonyBase
from .chat_data import HarmonyChatData
from .chat_message import HarmonyChatMessage
from .chat_nested import HarmonyChatNested


class HarmonyChat(HarmonyBase):
    """Chat class.

    Attributes
    ----------
    id : str
        The chat ID.
    data : HarmonyChatData
        The chat data.
        See `harmony.models.chat.HarmonyChatData` for more information.
    name : str
        The chat name.
    source : str
        The chat source.
    target : str
        The chat target.
    nested_chat : HarmonyChatNested
        The nested chat message/reply if any.
    message : HarmonyChatMessage
        The chat message.
    message_content : Optional[str]
        The chat message content if any. If method, the method's body.

    Functions
    ---------
    get_chat_args()
        Get the chat arguments to use in autogen.
    """

    id: Annotated[
        str,
        Field(
            ...,
            title="ID",
            description="The chat ID.",
        ),
    ]
    data: Annotated[
        HarmonyChatData,
        Field(
            ...,
            title="Data",
            description="The chat data.",
        ),
    ]

    @property
    def name(self) -> str:
        """Get the name."""
        return self.data.name

    @property
    def source(self) -> str:
        """Get the source."""
        if self.data.real_source:
            return self.data.real_source
        return self.data.source

    @property
    def target(self) -> str:
        """Get the target."""
        if self.data.real_target:
            return self.data.real_target
        return self.data.target

    @property
    def nested_chat(self) -> HarmonyChatNested:
        """Get the nested chat."""
        return self.data.nested_chat

    @property
    def message(self) -> HarmonyChatMessage:
        """Get the message."""
        if isinstance(
            self.data.message, str
        ):  # pragma: no cover (just for the lint)
            return HarmonyChatMessage(
                type="string",
                use_carryover=False,
                content=self.data.message,
                context={},
            )
        return self.data.message

    @property
    def message_content(self) -> Optional[str]:
        """Get the message content."""
        return self.data.message_content

    def get_chat_args(
        self,
        sender: Optional[HarmonyAgent] = None,
    ) -> Dict[str, Any]:
        """Get the chat arguments to use in autogen.

        Parameters
        ----------
        sender : HarmonyAgent
            The sender agent, to check if it's a RAG user.
        Returns
        -------
        dict
            The chat arguments.
        """
        args_dict = self.data.get_chat_args()
        if (
            isinstance(sender, HarmonyRagUser)
            and sender.agent_type == "rag_user"
            and self.message.type == "rag_message_generator"
        ):
            # check for n_results in agent data, to add in context
            n_results = sender.data.retrieve_config.n_results
            if isinstance(n_results, int) and n_results > 0:
                args_dict["n_results"] = n_results
        return args_dict
