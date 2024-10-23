"""Test harmony.models.skill.*."""

import pytest

from harmony.models.skill import HarmonySkill


def test_harmony_skill() -> None:
    """Test HarmonySkill."""
    # Given
    skill_id = "ws-1"
    name = "skill_name"
    description = "description"
    data = {"content": "def skill_name():\n    pass"}
    # When
    skill = HarmonySkill(  # type: ignore
        id=skill_id,
        name=name,
        description=description,
        data=data,  # type: ignore
    )
    # Then
    assert skill.id == skill_id
    assert skill.name == name
    assert skill.description == description
    assert skill.content == data["content"]
    assert not skill.secrets
    assert not skill.tags
    assert not skill.requirements


def test_invalid_skill() -> None:
    """Test invalid HarmonySkill."""
    with pytest.raises(ValueError):
        HarmonySkill()  # type: ignore

    # Given
    skill_id = "ws-1"
    name = "skill_name"
    description = "description"
    data = {"content": "def skill_name(4):"}
    # Then
    with pytest.raises(ValueError):
        HarmonySkill(  # type: ignore
            id=skill_id,
            name=name,
            description=description,
            data=data,  # type: ignore
        )

    # Given
    skill_id = "ws-1"
    name = "skill_name"
    description = "description"
    data = {"content": "def not_skill_name():\n    pass"}
    # Then
    with pytest.raises(ValueError):
        HarmonySkill(  # type: ignore
            id=skill_id,
            name=name,
            description=description,
            data=data,  # type: ignore
        )
