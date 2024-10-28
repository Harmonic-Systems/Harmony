"""Test harmony.exporting.chats.chats.*."""

from harmony.exporting.chats.chats import export_chats
from harmony.models import (
    HarmonyAgent,
    HarmonyChat,
    HarmonyChatData,
    HarmonyChatMessage,
    HarmonyChatNested,
    HarmonyChatSummary,
)


def test_export_chats() -> None:
    """Test export_chats()."""
    # Given
    agent1 = HarmonyAgent(  # type: ignore
        id="wa-1",
        name="agent1",
        agent_type="assistant",
    )
    agent2 = HarmonyAgent(  # type: ignore
        id="wa-2",
        name="agent2",
        agent_type="assistant",
    )
    agent3 = HarmonyAgent(  # type: ignore
        id="wa-3",
        name="agent3",
        agent_type="assistant",
    )
    agent4 = HarmonyAgent(  # type: ignore
        id="wa-4",
        name="agent4",
        agent_type="assistant",
    )
    chat1 = HarmonyChat(
        id="wc-1",
        data=HarmonyChatData(
            name="chat1",
            description="A chat.",
            source="wa-1",
            target="wa-2",
            position=1,
            order=1,
            clear_history=False,
            message=HarmonyChatMessage(
                type="string",
                use_carryover=False,
                content="Hello, world!",
                context={},
            ),
            summary=HarmonyChatSummary(
                method=None,
                prompt="",
                args={},
            ),
            max_turns=None,
            nested_chat=HarmonyChatNested(
                message=None,
                reply=None,
            ),
            silent=False,
            real_source="wa-3",
            real_target=None,
        ),
    )
    chat2 = HarmonyChat(
        id="wc-2",
        data=HarmonyChatData(
            name="chat2",
            description="Another chat.",
            source="wa-2",
            target="wa-1",
            position=1,
            order=1,
            clear_history=False,
            message=HarmonyChatMessage(
                type="string",
                use_carryover=False,
                content='{"Goodbye": "world!"}',
                context={},
            ),
            summary=HarmonyChatSummary(
                method=None,
                prompt="",
                args={},
            ),
            max_turns=None,
            nested_chat=HarmonyChatNested(
                message=None,
                reply=None,
            ),
            silent=False,
            real_source=None,
            real_target="wa-4",
        ),
    )
    all_agents = [agent1, agent2, agent3, agent4]
    agent_names = {agent.id: agent.name for agent in all_agents}
    # When
    all_chats = [chat1]
    chat_names = {chat.id: chat.name for chat in all_chats}
    # Then
    export_chats(
        agent_names=agent_names,
        chat_names=chat_names,
        main_chats=[(chat1, agent1, agent2)],
        tabs=1,
    )
    # When
    all_chats = [chat1, chat2]
    chat_names = {chat.id: chat.name for chat in all_chats}
    chats_string, _ = export_chats(
        agent_names=agent_names,
        chat_names=chat_names,
        main_chats=[
            (chat1, agent1, agent2),
            (chat2, agent2, agent1),
        ],
        tabs=1,
    )
    # Then
    expected = """initiate_chats([
        {
            "sender": agent1,
            "recipient": agent2,
            "clear_history": False,
            "silent": False,
            "message": "Hello, world!",
        },
        {
            "sender": agent2,
            "recipient": agent1,
            "clear_history": False,
            "silent": False,
            "message": "{\\\\"Goodbye\\\\": \\\\"world!\\\\"}",
        },
    ])"""
    assert chats_string == expected
