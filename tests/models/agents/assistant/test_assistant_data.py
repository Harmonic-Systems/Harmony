"""Test harmony.models.agents.assistant.assistant_data.*."""

from harmony.models.agents.assistant.assistant_data import HarmonyAssistantData


def test_harmony_assistant_data() -> None:
    """Test HarmonyAssistantData."""
    assistant_data = HarmonyAssistantData()  # type: ignore
    assert assistant_data.human_input_mode == "NEVER"
