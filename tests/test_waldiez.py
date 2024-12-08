"""Test harmony.harmony.*."""

import os
import tempfile

import pytest
from autogen.version import __version__ as ag2_version  # type: ignore

from harmony import Harmony

from .exporting.flow_helpers import get_flow


def test_harmony() -> None:
    """Test Harmony with retrievechat requirement."""
    flow = get_flow()
    harmony = Harmony(flow=flow)
    assert harmony.name == flow.name

    flow_dump = harmony.model_dump_json(by_alias=True)
    with tempfile.NamedTemporaryFile(
        "w", suffix=".harmony", delete=False
    ) as file:
        file.write(flow_dump)
        file_path = file.name
        file.close()
    harmony2 = Harmony.load(file_path)
    os.remove(file_path)
    assert harmony2.name == flow.name
    assert harmony2.description == flow.description
    assert harmony2.tags == flow.tags
    assert next(harmony2.models)
    assert harmony2.has_rag_agents
    skill = next(harmony2.skills)
    assert f"pyautogen[retrievechat]=={ag2_version}" in harmony2.requirements
    assert "SKILL_KEY" in skill.secrets
    assert "SKILL_KEY" == harmony2.get_flow_env_vars()[0][0]
    for agent in harmony2.agents:
        if agent.agent_type == "manager":
            assert harmony2.get_group_chat_members(agent)
        else:
            assert not harmony2.get_group_chat_members(agent)
    assert harmony2.chats


def test_harmony_without_rag() -> None:
    """Test Harmony."""
    flow_dict = get_flow().model_dump(by_alias=True)
    # remove the rag user from the agents
    flow_dict["data"]["agents"]["ragUsers"] = []
    # also remove any chats that has source or target "wa-4" (the rag agent)
    flow_dict["data"]["chats"] = [
        chat
        for chat in flow_dict["data"]["chats"]
        if (
            chat["data"]["source"] != "wa-4"
            and chat["data"]["target"] != "wa-4"
        )
    ]
    harmony = Harmony.from_dict(data=flow_dict)
    assert harmony.name == flow_dict["name"]
    assert harmony.description == flow_dict["description"]
    assert harmony.tags == flow_dict["tags"]
    assert next(harmony.models)
    assert not harmony.has_rag_agents
    assert f"pyautogen[retrievechat]=={ag2_version}" not in harmony.requirements
    assert f"pyautogen=={ag2_version}" in harmony.requirements


def test_harmony_errors() -> None:
    """Test Harmony errors."""
    with pytest.raises(ValueError):
        Harmony.load("non_existent_file")

    with pytest.raises(ValueError):
        Harmony.from_dict(
            name="flow",
            description="flow description",
            tags=["tag"],
            requirements=["requirement"],
            data={"type": "flow", "data": {}},
        )

    with pytest.raises(ValueError):
        Harmony.from_dict(
            data={"type": "flow", "data": {}},
        )

    with pytest.raises(ValueError):
        Harmony.from_dict(
            data={"type": "other", "data": {}},
        )

    with tempfile.NamedTemporaryFile(
        "w", suffix=".harmony", delete=False
    ) as file:
        file.write("invalid json")
        file_path = file.name
        file.close()
    with pytest.raises(ValueError):
        Harmony.load(file_path)
    os.remove(file_path)
