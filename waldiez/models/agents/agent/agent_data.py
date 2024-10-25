"""Common data structures for agents."""

from typing import List, Optional, Union

from pydantic import ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing_extensions import Annotated, Literal

from ...common import HarmonyBase
from .code_execution import HarmonyAgentCodeExecutionConfig
from .linked_skill import HarmonyAgentLinkedSkill
from .nested_chat import HarmonyAgentNestedChat
from .teachability import HarmonyAgentTeachability
from .termination_message import HarmonyAgentTerminationMessage


class HarmonyAgentData(HarmonyBase):
    """Harmony Agent Data.

    Attributes
    ----------
    system_message : Optional[str]
        The agent's system message. Default: None (depends on the agent's type)
    human_input_mode : Literal["ALWAYS", "NEVER", "TERMINATE"]
        The human input mode to use for the agent.
    code_execution_config : Union[HarmonyAgentCodeExecutionConfig, False]
        The code execution config. Either False (no execution) or a dict.
    agent_default_auto_reply : Optional[str]
        The agent's default auto reply when no input is received.
    max_consecutive_auto_reply : Optional[int]
        The maximum number or consecutive auto replies to use
        before ending the chat. Default: None (no limit).
    termination : HarmonyAgentTerminationMessage
        The message termination check to use (keyword, method, none)
    teachability : HarmonyAgentTeachability
        The agent teachability configuration.
    model_ids: List[str]
        A list of models (their ids) to link with the agent.
    skills : List[HarmonyAgentLinkedSkill]
        A list of skills (id and executor) to register.
    nested_chats : List[HarmonyAgentNestedChat]
        A list of nested chats (triggered_by, messages), to register.
    """

    model_config = ConfigDict(
        extra="ignore",
        alias_generator=to_camel,
        populate_by_name=True,
        # we have a field starting with "model_" (model_ids)
        # this is protected by default
        protected_namespaces=(),
    )

    system_message: Annotated[
        Optional[str],
        Field(
            None,
            title="System message",
            description="The agent's system message.",
            alias="systemMessage",
        ),
    ]
    human_input_mode: Annotated[
        Literal["ALWAYS", "NEVER", "TERMINATE"],
        Field(
            "NEVER",
            title="Human input mode",
            description="The human input mode to use for the agent.",
            alias="humanInputMode",
        ),
    ]
    code_execution_config: Annotated[
        Union[HarmonyAgentCodeExecutionConfig, Literal[False]],
        Field(
            False,
            title="Code execution config",
            description=(
                "The code execution config. Either False (no execution) "
                "or a `HarmonyAgentCodeExecutionConfig` with details"
            ),
            alias="codeExecutionConfig",
        ),
    ]
    agent_default_auto_reply: Annotated[
        Optional[str],
        Field(
            None,
            title="Agent's default auto reply",
            description=(
                "The agent's default auto reply when no input is received."
            ),
            alias="agentDefaultAutoReply",
        ),
    ]
    max_consecutive_auto_reply: Annotated[
        Optional[int],
        Field(
            None,
            title="Max consecutive auto reply",
            description=(
                "The maximum number or consecutive auto replies to use "
                "before ending the chat"
            ),
            alias="maxConsecutiveAutoReply",
        ),
    ]
    termination: Annotated[
        HarmonyAgentTerminationMessage,
        Field(
            title="Termination",
            description=(
                "The message termination check to use (keyword, method, none)"
            ),
            default_factory=HarmonyAgentTerminationMessage,
        ),
    ]
    teachability: Annotated[
        HarmonyAgentTeachability,
        Field(
            title="Teachability",
            description="The agent teachability configuration.",
            default_factory=HarmonyAgentTeachability,
        ),
    ]
    model_ids: Annotated[
        List[str],
        Field(
            default_factory=list,
            title="Model IDs",
            description="A list of models (their ids) to link with the agent.",
            alias="modelIds",
        ),
    ]
    skills: Annotated[
        List[HarmonyAgentLinkedSkill],
        Field(
            default_factory=list,
            title="Skills",
            description=("A list of skills (id and executor) to register."),
        ),
    ]
    nested_chats: Annotated[
        List[HarmonyAgentNestedChat],
        Field(
            default_factory=list,
            description=(
                "A list of nested chats (triggered_by, messages), to register."
            ),
            alias="nestedChats",
        ),
    ]
