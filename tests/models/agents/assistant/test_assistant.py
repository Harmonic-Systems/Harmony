"""Test harmony.models.agents.assistant.assistant.*."""

from harmony.models.agents.assistant.assistant import HarmonyAssistant


def test_harmony_assistant() -> None:
    """Test HarmonyAssistant."""
    assistant = HarmonyAssistant(id="wa-1", name="assistant")  # type: ignore
    assert assistant.data.human_input_mode == "NEVER"
    assert assistant.agent_type == "assistant"
