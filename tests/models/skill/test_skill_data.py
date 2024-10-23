"""Test harmony.models.skill.skill_data.*."""

import pytest

from harmony.models.skill import HarmonySkillData


def test_harmony_skill_data() -> None:
    """Test HarmonySkillData."""
    # Given
    content = "print('hello, world')"
    secrets = {"API_KEY": "api_key"}
    # When
    skill_data = HarmonySkillData(content=content, secrets=secrets)
    # Then
    assert skill_data.content == content
    assert skill_data.secrets == secrets

    # Given
    skill_data = HarmonySkillData(content=content)  # type: ignore
    # Then
    assert skill_data.content == content
    assert not skill_data.secrets

    with pytest.raises(ValueError):
        skill_data = HarmonySkillData()  # type: ignore
