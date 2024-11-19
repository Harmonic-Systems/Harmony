"""Test harmony.models.agents.agent.nested_chat.*."""

from harmony.models.agents.agent.nested_chat import (
    HarmonyAgentNestedChat,
    HarmonyAgentNestedChatMessage,
)


def test_harmony_agent_nested_chat_message() -> None:
    """Test HarmonyAgentNestedChatMessage."""
    message = HarmonyAgentNestedChatMessage(
        id="message_id",
        is_reply=False,
    )
    assert message.id == "message_id"
    assert not message.is_reply


def test_harmony_agent_nested_chat() -> None:
    """Test HarmonyAgentNestedChat."""
    nested_chat = HarmonyAgentNestedChat(
        triggered_by=["wa-1"],
        messages=[HarmonyAgentNestedChatMessage(id="wc-2", is_reply=True)],
    )
    assert nested_chat.triggered_by[0] == "wa-1"
    assert nested_chat.messages[0].id == "wc-2"
    assert nested_chat.messages[0].is_reply
