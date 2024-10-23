"""Test harmony.models.agents.rag_user.rag_user.*."""

from harmony.models.agents.rag_user.rag_user import HarmonyRagUser


def test_harmony_rag_user() -> None:
    """Test HarmonyRagUser."""
    rag_user = HarmonyRagUser(id="wa-1", name="rag_user")  # type: ignore
    assert rag_user.agent_type == "rag_user"
    assert rag_user.data.human_input_mode == "ALWAYS"
    assert rag_user.retrieve_config
