"""Test harmony.models.agents.agent.linked_skill.*."""

from harmony.models.agents.agent.linked_skill import HarmonyAgentLinkedSkill


def test_harmony_agent_linked_skill() -> None:
    """Test HarmonyAgentLinkedSkill."""
    linked_skill = HarmonyAgentLinkedSkill(
        id="skill_id", executor_id="agent_id"
    )
    assert linked_skill.id == "skill_id"
    assert linked_skill.executor_id == "agent_id"
