"""Test harmony.models.chat.chat_nested.*."""

import pytest

from harmony.models.chat.chat_message import HarmonyChatMessage
from harmony.models.chat.chat_nested import HarmonyChatNested


def test_harmony_chat_nested() -> None:
    """Test HarmonyChatNested."""
    # Given
    reply = HarmonyChatMessage(
        type="string",
        use_carryover=False,
        content="Hi",
        context={},
    )
    # When
    chat_nested = HarmonyChatNested(
        message="Hello there",  # type: ignore
        reply=reply,
    )
    # Then
    assert isinstance(chat_nested.message, HarmonyChatMessage)
    assert chat_nested.message.content == "Hello there"
    assert isinstance(chat_nested.reply, HarmonyChatMessage)
    assert chat_nested.reply.type == "string"
    assert chat_nested.reply.content == "Hi"

    # Given
    reply = None  # type: ignore
    message_content = """
def nested_chat_message(recipient, messages, sender, config):
    return "Hello there"
"""
    message = HarmonyChatMessage(
        type="method",
        use_carryover=False,
        content=message_content,
        context={},
    )
    # When
    chat_nested = HarmonyChatNested(
        message=message,
        reply=reply,
    )
    # Then
    assert isinstance(chat_nested.message, HarmonyChatMessage)
    assert chat_nested.message.type == "method"
    assert chat_nested.message.content == message_content
    assert chat_nested.message_content == (
        "    # type: (ConversableAgent, list[dict], ConversableAgent, dict) ->"
        ' Union[dict, str]\n    return "Hello there"'
    )
    assert isinstance(chat_nested.reply, HarmonyChatMessage)
    assert chat_nested.reply.type == "none"
    assert chat_nested.reply.content is None

    # Given
    message_content = "Hello there"
    reply_content = """
def nested_chat_reply(recipient, messages, sender, config):
    return "Hi"
"""
    # When
    chat_nested = HarmonyChatNested(
        message={  # type: ignore
            "type": "string",
            "content": message_content,
        },
        reply={  # type: ignore
            "type": "method",
            "content": reply_content,
        },
    )
    # Then
    assert isinstance(chat_nested.message, HarmonyChatMessage)
    assert chat_nested.message.type == "string"
    assert chat_nested.message.content == "Hello there"
    assert isinstance(chat_nested.reply, HarmonyChatMessage)
    assert chat_nested.reply.type == "method"
    assert chat_nested.reply.content == reply_content
    assert chat_nested.reply_content == (
        "    # type: (ConversableAgent, list[dict], ConversableAgent, dict) ->"
        ' Union[dict, str]\n    return "Hi"'
    )

    with pytest.raises(ValueError):
        chat_nested = HarmonyChatNested(
            message=HarmonyChatMessage(
                type="string",
                use_carryover=False,
                content="Hello there",
                context={},
            ),
            reply=45,  # type: ignore
        )
