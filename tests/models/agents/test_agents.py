"""Test harmony.models.agents."""

from harmony.models.agents import (
    HarmonyAgents,
    HarmonyAssistant,
    HarmonyUserProxy,
)
from harmony.models.model import HarmonyModel
from harmony.models.skill import HarmonySkill


def test_harmony_agents() -> None:
    """Test HarmonyAgents."""
    model = HarmonyModel(
        id="wa-1",
        name="model",
        type="model",
        description="Model",
        tags=[],
        requirements=[],
        data={},  # type: ignore
    )
    skill = HarmonySkill(
        id="wa-2",
        name="skill",
        type="skill",
        description="Skill",
        tags=[],
        requirements=[],
        data={  # type: ignore
            "content": "def skill():\n    return 'skill'",
        },
    )
    assistant = HarmonyAssistant(
        id="wa-1",
        name="assistant",
        type="agent",
        agent_type="assistant",
        description="Assistant",
        tags=[],
        requirements=[],
        data={  # type: ignore
            "model_ids": [model.id],
            "skills": [
                {"id": skill.id, "executor_id": "wa-1"},
            ],
        },
    )
    user = HarmonyUserProxy(
        id="wa-2",
        name="user",
        type="agent",
        agent_type="user",
        description="User",
        tags=[],
        requirements=[],
        data={},  # type: ignore
    )
    agents = HarmonyAgents(
        assistants=[assistant],
        users=[user],
        managers=[],
        rag_users=[],
    )
    assert agents.assistants == [assistant]
    assert next(agents.members) == user
    agents.validate_flow(model_ids=[model.id], skill_ids=[skill.id])
