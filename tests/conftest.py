"""Common fixtures for tests."""

import pytest

from harmony.models import (
    HarmonyAgents,
    HarmonyAgentTeachability,
    HarmonyAgentTerminationMessage,
    HarmonyAssistant,
    HarmonyAssistantData,
    HarmonyChat,
    HarmonyChatData,
    HarmonyChatMessage,
    HarmonyChatNested,
    HarmonyChatSummary,
    HarmonyFlow,
    HarmonyFlowData,
    HarmonyUserProxy,
    HarmonyUserProxyData,
)


def get_runnable_flow() -> HarmonyFlow:
    """Get a runnable HarmonyFlow instance.

    without models and skills

    Returns
    -------
    HarmonyFlow
        A HarmonyFlow instance.
    """
    user = HarmonyUserProxy(
        id="wa-1",
        name="user",
        agent_type="user",
        description="User Agent",
        type="agent",
        data=HarmonyUserProxyData(
            system_message=None,
            human_input_mode="ALWAYS",
            code_execution_config=False,
            agent_default_auto_reply="I am a user.",
            max_consecutive_auto_reply=5,
            termination=HarmonyAgentTerminationMessage(
                type="keyword",
                keywords=["bye", "goodbye"],
                criterion="found",
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
            teachability=HarmonyAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=1.5,
                max_num_retrievals=10,
            ),
        ),
        tags=["user"],
        requirements=[],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
    )
    assistant = HarmonyAssistant(
        id="wa-2",
        name="assistant",
        description="Assistant Agent",
        type="agent",
        agent_type="assistant",
        data=HarmonyAssistantData(
            system_message=None,
            human_input_mode="NEVER",
            code_execution_config=False,
            agent_default_auto_reply="I am an assistant.",
            max_consecutive_auto_reply=5,
            termination=HarmonyAgentTerminationMessage(
                type="keyword",
                keywords=["bye", "goodbye"],
                criterion="found",
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
            teachability=HarmonyAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=1.5,
                max_num_retrievals=10,
            ),
        ),
        tags=["assistant"],
        requirements=[],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
    )
    chat = HarmonyChat(
        id="wc-1",
        data=HarmonyChatData(
            name="chat_1",
            description="Description of chat 1",
            source="wa-1",
            target="wa-2",
            position=-1,
            order=0,
            clear_history=True,
            silent=False,
            max_turns=2,
            message=HarmonyChatMessage(
                type="string",
                use_carryover=False,
                content="Hello wa-1",
                context={},
            ),
            summary=HarmonyChatSummary(
                method="last_msg",
                prompt="",
                args={},
            ),
            nested_chat=HarmonyChatNested(
                message=None,
                reply=None,
            ),
            real_source=None,
            real_target=None,
        ),
    )
    agents = HarmonyAgents(
        users=[user],
        assistants=[assistant],
        managers=[],
        rag_users=[],
    )
    flow = HarmonyFlow(
        id="wf-1",
        name="flow_name",
        type="flow",
        description="Flow Description",
        data=HarmonyFlowData(
            nodes=[],
            edges=[],
            viewport={},
            agents=agents,
            models=[],
            skills=[],
            chats=[chat],
        ),
        tags=["flow"],
        requirements=[],
        storage_id="flow-1",
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
    )
    return flow


@pytest.fixture(scope="function")
def harmony_flow() -> HarmonyFlow:
    """Get a valid, runnable HarmonyFlow instance.

    without models and skills

    Returns
    -------
    HarmonyFlow
        A HarmonyFlow instance.
    """
    return get_runnable_flow()
