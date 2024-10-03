"""Waldie Message Model."""

from typing import Any, Dict, Optional, Tuple, Union

from pydantic import Field
from typing_extensions import Annotated, Literal

from ..common import WaldieBase, WaldieMethodName, check_function


class WaldieChatMessage(WaldieBase):
    """
    Waldie Message.

    A generic message with a type and content.

    If the type is not 'none',
    the content is a string.
    If the type is 'method', the content is the source code of a method.

    Attributes
    ----------
    type : Literal["string", "method", "last_carryover",  "none"]
        The type of the message: string, method, last_carryover, or none.
        If last_carryover, a method to return the context's last carryover
        will be used.
    content : Optional[str]
        The content of the message (string or method).
    context : Dict[str, Any]
        Extra context of the message.
    """

    type: Annotated[
        Literal["string", "method", "last_carryover", "none"],
        Field(
            "none",
            title="Type",
            description=(
                "The type of the message: string, method, last_carryover, or none."
            ),
        ),
    ]
    content: Annotated[
        Optional[str],
        Field(
            None,
            title="Content",
            description="The content of the message (string or method).",
        ),
    ]
    context: Annotated[
        Dict[str, Any],
        Field(
            default_factory=dict,
            title="Context",
            description="Extra context of the message.",
        ),
    ]


def validate_message_dict(
    value: Dict[
        Literal["type", "content", "context"],
        Union[Optional[str], Optional[Dict[str, Any]]],
    ],
    function_name: WaldieMethodName,
) -> WaldieChatMessage:
    """Validate a message dict.

    Check the provided message dict.
    Depending on the type, the content is validated.
    If the type is "method", the content is checked against the function name.

    Parameters
    ----------
    value : dict
        The message dict.
    function_name : str (WaldieMethodName)
        The function name.

    Returns
    -------
    WaldieChatMessage
        The validated message.

    Raises
    ------
    ValueError
        If the validation fails.
    """
    message_type, content, context = _get_message_args_from_dict(value)
    if message_type == "string":
        if not content:
            raise ValueError(
                "The message content is required for the string type"
            )
        return WaldieChatMessage(
            type="string", content=content, context=context
        )
    if message_type == "none":
        return WaldieChatMessage(type="none", content=None, context=context)
    if message_type == "method":
        if not content:
            raise ValueError(
                "The message content is required for the method type"
            )
        valid, error_or_content = check_function(content, function_name)
        if not valid:
            raise ValueError(error_or_content)
        return WaldieChatMessage(
            type="method", content=error_or_content, context=context
        )
    if message_type == "last_carryover":
        before_carryover = context.get("text", "")
        if not isinstance(before_carryover, str):
            before_carryover = ""
        return WaldieChatMessage(
            type="method",
            content=_get_last_carryover_method_content(before_carryover),
            context={},
        )
    raise ValueError("Invalid message type")  # pragma: no cover


def _get_message_args_from_dict(
    value: Dict[
        Literal["type", "content", "context"],
        Union[Optional[str], Optional[Dict[str, Any]]],
    ],
) -> Tuple[str, Optional[str], Dict[str, Any]]:
    """Get the message args from a dict.

    Parameters
    ----------
    value : dict
        The message dict.

    Returns
    -------
    tuple
        The message type, content, and context.

    Raises
    ------
    ValueError
        If the message type is invalid.
    """
    message_type = value.get("type")
    if not isinstance(message_type, str) or message_type not in (
        "string",
        "method",
        "last_carryover",
        "none",
    ):
        raise ValueError("Invalid message type")
    content = value.get("content", "")
    if not isinstance(content, str):
        content = ""
    context: Dict[str, Any] = {}
    context_value = value.get("context")
    if isinstance(context_value, dict):
        context = context_value
    if not isinstance(context, dict):  # pragma: no cover
        context = {}
    return message_type, content, context


def _get_last_carryover_method_content(extra_text: str) -> str:
    """Get the last carryover method content.

    Parameters
    ----------
    extra_text : str
        Extra text to add to the method content before the carryover.
    Returns
    -------
    str
        The last carryover method content.
    """
    method_content = '''
def callable_message(self, source, target, context):
    # type: (ConversableAgent, ConversableAgent, dict) -> Union[dict, str]
    """Return the last carryover from the context.

    Parameters
    ----------
    source : ConversableAgent
        The source agent.
    target : ConversableAgent
        The target agent.
    context : dict
        The context.

    Returns
    -------
    Union[dict, str]
        The last carryover.
    """
    carryover = context.get("carryover", "")
    if isinstance(carryover, list):
        carryover = carryover[-1]'''
    if extra_text:
        method_content += f"""
    final_message = f"{extra_text}" + carryover
    return final_message
"""
    else:
        method_content += """
    return carryover
"""
    return method_content
