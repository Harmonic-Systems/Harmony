"""Helpers for getting a flow."""

from typing import List

from harmony.models import (
    HarmonyAgentCodeExecutionConfig,
    HarmonyAgentLinkedSkill,
    HarmonyAgentNestedChat,
    HarmonyAgentNestedChatMessage,
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
    HarmonyGroupManager,
    HarmonyGroupManagerData,
    HarmonyGroupManagerSpeakers,
    HarmonyModel,
    HarmonyModelData,
    HarmonyModelPrice,
    HarmonyRagUser,
    HarmonyRagUserData,
    HarmonyRagUserRetrieveConfig,
    HarmonyRagUserVectorDbConfig,
    HarmonySkill,
    HarmonySkillData,
    HarmonyUserProxy,
    HarmonyUserProxyData,
)


def get_model(model_id: str = "wm-1") -> HarmonyModel:
    """Get a HarmonyModel.

    Parameters
    ----------
    model_id : str, optional
        The model ID, by default "wm-1"

    Returns
    -------
    HarmonyModel
        A HarmonyModel instance
    """
    return HarmonyModel(
        id=model_id,
        name="model_name",
        description="Model Description",
        tags=["model"],
        requirements=[],
        type="model",
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=HarmonyModelData(
            api_type="groq",  # to cover additional requirements
            api_key="api_key",
            api_version="2020-05-03",
            base_url="https://example.com/v1",
            price=HarmonyModelPrice(
                prompt_price_per_1k=0.06,
                completion_token_price_per_1k=0.12,
            ),
            temperature=0.5,
            top_p=None,
            max_tokens=1000,
            default_headers={},
        ),
    )


def get_skill(skill_id: str = "ws-1") -> HarmonySkill:
    """Get a HarmonySkill.

    Parameters
    ----------
    skill_id : str, optional
        The skill ID, by default "ws-1"

    Returns
    -------
    HarmonySkill
        A HarmonySkill instance.
    """
    return HarmonySkill(
        id=skill_id,
        name="skill_name",
        description="Skill Description",
        tags=["skill"],
        requirements=["chess"],
        type="skill",
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=HarmonySkillData(
            content=(
                "def skill_name():\n"
                '    """Skill Description."""\n'
                "    return 'Skill Response'"
            ),
            secrets={
                "SKILL_KEY": "skill_value",
            },
        ),
    )


def get_user_proxy(agent_id: str = "wa-1") -> HarmonyUserProxy:
    """Get a HarmonyUserProxy.

    Parameters
    ----------
    agent_id : str, optional
        The agent ID, by default "wa-1"

    Returns
    -------
    HarmonyUserProxy
        A HarmonyUserProxy instance.
    """
    return HarmonyUserProxy(
        id=agent_id,
        name="user",
        description="User Agent",
        type="agent",
        agent_type="user",
        tags=["user"],
        requirements=[],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=HarmonyUserProxyData(
            system_message=None,
            human_input_mode="ALWAYS",
            code_execution_config=HarmonyAgentCodeExecutionConfig(
                work_dir="coding",
                use_docker=None,
                last_n_messages=3,
                functions=["ws-1"],
                timeout=40,
            ),
            agent_default_auto_reply="I am a user.",
            max_consecutive_auto_reply=5,
            termination=HarmonyAgentTerminationMessage(
                type="keyword",
                keywords=["bye", "goodbye"],
                criterion="found",
                method_content=None,
            ),
            model_ids=[],
            skills=[
                HarmonyAgentLinkedSkill(
                    id="ws-1",
                    executor_id="wa-2",
                )
            ],
            nested_chats=[
                HarmonyAgentNestedChat(
                    triggered_by=["wa-1"],
                    messages=[
                        HarmonyAgentNestedChatMessage(
                            id="wc-2",
                            is_reply=True,
                        ),
                        HarmonyAgentNestedChatMessage(
                            id="wc-3",
                            is_reply=False,
                        ),
                    ],
                ),
            ],
            teachability=HarmonyAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=1.5,
                max_num_retrievals=10,
            ),
        ),
    )


def get_assistant(agent_id: str = "wa-2") -> HarmonyAssistant:
    """Get a HarmonyAssistant.

    Parameters
    ----------
    agent_id : str, optional
        The agent ID, by default "wa-2"

    Returns
    -------
    HarmonyAssistant
        A HarmonyAssistant instance.
    """
    assistant_termination = (
        "def is_termination_message(message):\n"
        '    """Check if the message is a termination message."""\n'
        "    return any(\n"
        '        keyword in message.get("content", "").lower()\n'
        '        for keyword in ["bye", "goodbye"]\n'
        "    )"
    )
    return HarmonyAssistant(
        id=agent_id,
        name="assistant",
        description="Assistant Agent",
        type="agent",
        agent_type="assistant",
        tags=["assistant"],
        requirements=[],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=HarmonyAssistantData(
            system_message=None,
            human_input_mode="NEVER",
            code_execution_config=False,
            agent_default_auto_reply="I am an assistant.",
            max_consecutive_auto_reply=5,
            termination=HarmonyAgentTerminationMessage(
                type="method",
                keywords=[],
                criterion="found",
                method_content=assistant_termination,
            ),
            model_ids=["wm-1"],
            skills=[
                HarmonyAgentLinkedSkill(
                    id="ws-1",
                    executor_id="wa-2",
                ),
            ],
            nested_chats=[],
            teachability=HarmonyAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=1.5,
                max_num_retrievals=10,
            ),
        ),
    )


def get_group_manager(agent_id: str = "wa-3") -> HarmonyGroupManager:
    """Get a HarmonyGroupManager.

    Parameters
    ----------
    agent_id : str, optional
        The agent ID, by default "wa-3"

    Returns
    -------
    HarmonyGroupManager
        A HarmonyGroupManager instance.
    """
    custom_speaker_selection = (
        "def custom_speaker_selection(last_speaker, groupchat):\n"
        "    return last_speaker"
    )
    return HarmonyGroupManager(
        id=agent_id,
        name="group_manager",
        description="Group Manager Agent",
        type="agent",
        agent_type="manager",
        tags=["manager"],
        requirements=[],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=HarmonyGroupManagerData(
            max_round=10,
            admin_name="user",
            enable_clear_history=True,
            send_introductions=False,
            system_message=None,
            human_input_mode="NEVER",
            code_execution_config=False,
            agent_default_auto_reply="I am a group manager.",
            max_consecutive_auto_reply=5,
            termination=HarmonyAgentTerminationMessage(
                type="keyword",
                keywords=["TERMINATE"],
                criterion="exact",
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
            speakers=HarmonyGroupManagerSpeakers(
                selection_mode="transition",
                selection_method="custom",
                selection_custom_method=custom_speaker_selection,
                allow_repeat=["wa-1"],
                max_retries_for_selecting=3,
                allowed_or_disallowed_transitions={
                    "wa-1": ["wa-2"],
                    "wa-2": ["wa-1"],
                },
                transitions_type="allowed",
            ),
            teachability=HarmonyAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=1.5,
                max_num_retrievals=10,
            ),
        ),
    )


def get_rag_user(agent_id: str = "wa-4") -> HarmonyRagUser:
    """Get a HarmonyRagUser.

    Parameters
    ----------
    agent_id : str, optional
        The agent ID, by default "wa-4"

    Returns
    -------
    HarmonyRagUser
        A HarmonyRagUser instance.
    """
    custom_embedding = "def custom_embedding_function():\n    return list"
    return HarmonyRagUser(
        id=agent_id,
        name="rag_user",
        description="RAG User",
        tags=["rag_user"],
        requirements=[],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        type="agent",
        agent_type="rag_user",
        data=HarmonyRagUserData(
            system_message=None,
            human_input_mode="ALWAYS",
            code_execution_config=False,
            agent_default_auto_reply="I am a group manager.",
            max_consecutive_auto_reply=5,
            termination=HarmonyAgentTerminationMessage(
                type="keyword",
                criterion="ending",
                keywords=["bye", "goodbye"],
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
            retrieve_config=HarmonyRagUserRetrieveConfig(
                task="default",
                vector_db="chroma",
                db_config=HarmonyRagUserVectorDbConfig(
                    model=None,
                    use_memory=False,
                    use_local_storage=True,
                    local_storage_path="documents",
                    connection_url=None,
                    wait_until_document_ready=None,
                    wait_until_index_ready=None,
                    metadata=None,
                ),
                docs_path=[
                    "documents",
                    "C:\\Users\\username\\Documents\\file.txt",
                    "/home/username/Documents/",
                    "https://example.com/file.txt",
                ],
                new_docs=True,
                model=None,
                chunk_token_size=100,
                context_max_tokens=1000,
                chunk_mode="multi_lines",
                must_break_at_empty_line=True,
                use_custom_embedding=True,
                embedding_function=custom_embedding,
                use_custom_text_split=False,
                custom_text_split_function=None,
                use_custom_token_count=False,
                custom_token_count_function=None,
                collection_name="autogen-docs",
                custom_text_types=None,
                customized_answer_prefix=None,
                update_context=True,
                get_or_create=True,
                overwrite=True,
                recursive=True,
                distance_threshold=20,
                n_results=10,
                customized_prompt=None,
            ),
            teachability=HarmonyAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=1.5,
                max_num_retrievals=10,
            ),
        ),
    )


def get_chats(count: int = 3) -> List[HarmonyChat]:
    """Get a list of HarmonyChat instances.

    Parameters
    ----------
    count : int, optional
        The number of chats to generate, by default 3

    Returns
    -------
    List[HarmonyChat]
        A list of HarmonyChat instances
    """
    chats = []
    custom_message = (
        "def callable_message(sender, recipient, context):\n"
        '    return "hello!"'
    )
    for index in range(count):
        context = {"problem": "Solve tha task."} if index == 0 else {}
        nested_chat = HarmonyChatNested(
            message=None,
            reply=None,
        )
        source_index = index + 1
        target_index = index + 2
        chat = HarmonyChat(
            id=f"wc-{index + 1}",
            data=HarmonyChatData(
                name=f"chat_{index + 1}",
                description=f"Description of chat {index + 1}",
                source=f"wa-{source_index}",
                target=f"wa-{target_index}",
                position=-1,
                order=index,
                clear_history=True,
                silent=False,
                max_turns=5,
                message=HarmonyChatMessage(
                    type="string" if index != 2 else "method",
                    use_carryover=False,
                    content=(
                        f"Hello wa-{source_index}"
                        if index != 2
                        else custom_message
                    ),
                    context=context,
                ),
                summary=HarmonyChatSummary(
                    method="reflection_with_llm",
                    prompt="Summarize the chat.",
                    args={"summary_role": "user"},
                ),
                nested_chat=nested_chat,
                real_source=None,
                real_target=None,
            ),
        )
        chats.append(chat)
    return chats


def get_flow() -> HarmonyFlow:
    """Get a HarmonyFlow instance.

    Returns
    -------
    HarmonyFlow
        A HarmonyFlow instance.
    """
    model = get_model()
    skill = get_skill()
    user = get_user_proxy()
    assistant = get_assistant()
    manager = get_group_manager()
    rag_user = get_rag_user()
    chats = get_chats()
    agents = HarmonyAgents(
        users=[user],
        assistants=[assistant],
        managers=[manager],
        rag_users=[rag_user],
    )
    flow = HarmonyFlow(
        id="wf-1",
        name="flow_name",
        type="flow",
        description="Flow Description",
        tags=["flow"],
        requirements=[],
        storage_id="flow-1",
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=HarmonyFlowData(
            nodes=[],
            edges=[],
            viewport={},
            agents=agents,
            models=[model],
            skills=[skill],
            chats=chats,
        ),
    )
    return flow
