"""Test harmony.models.chat.chat_summary.*."""

import pytest

from harmony.models.chat.chat_summary import HarmonyChatSummary


def test_harmony_chat_summary() -> None:
    """Test HarmonyChatSummary."""
    # Given
    chat_summary = HarmonyChatSummary(  # type: ignore
        prompt="prompt",
    )
    assert chat_summary.prompt == "prompt"
    assert not chat_summary.args

    # Given
    chat_summary = HarmonyChatSummary(
        method="lastMsg",
        prompt="prompt",
        args={"key": "value"},
    )
    assert chat_summary.method == "last_msg"
    summary_dump = chat_summary.model_dump(by_alias=True)
    assert summary_dump["method"] == "lastMsg"
    assert summary_dump["prompt"] == "prompt"
    assert summary_dump["args"] == {"key": "value"}
    summary_dump = chat_summary.model_dump(by_alias=False)
    assert summary_dump["method"] == "last_msg"

    # Given
    chat_summary = HarmonyChatSummary(
        method="reflectionWithLlm",
        prompt="prompt",
        args={"key": "value"},
    )
    assert chat_summary.method == "reflection_with_llm"
    summary_dump = chat_summary.model_dump(by_alias=True)
    assert summary_dump["method"] == "reflectionWithLlm"
    summary_dump = chat_summary.model_dump(by_alias=False)
    assert summary_dump["method"] == "reflection_with_llm"

    with pytest.raises(ValueError):
        chat_summary = HarmonyChatSummary(prompt=1)  # type: ignore
