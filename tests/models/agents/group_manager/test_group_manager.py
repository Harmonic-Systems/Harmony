"""Test harmony.models.agents.group_manager.group_manager.*."""

import pytest

from harmony.models.agents.group_manager.group_manager import (
    HarmonyGroupManager,
)


def test_harmony_group_manager() -> None:
    """Test HarmonyGroupManager."""
    group_manager = HarmonyGroupManager(  # type: ignore
        id="wa-1", name="group_manager"
    )
    assert group_manager.data.human_input_mode == "NEVER"
    assert group_manager.agent_type == "manager"

    group_manager.validate_transitions(agent_ids=["wa-1"])


def test_harmony_group_manager_transitions() -> None:
    """Test HarmonyGroupManager transitions."""
    group_manager1 = HarmonyGroupManager(
        id="wa-1",
        name="group_manager",
        data={  # type: ignore
            "speakers": {
                "selection_mode": "transition",
                "allow_repeat": ["wa-2"],
                "allowed_or_disallowed_transitions": {
                    "wa-2": ["wa-3"],
                    "wa-3": ["wa-2"],
                },
            }
        },
    )
    group_manager1.validate_transitions(agent_ids=["wa-2", "wa-3"])

    group_manager2 = HarmonyGroupManager(
        id="wa-1",
        name="group_manager",
        data={  # type: ignore
            "speakers": {
                "selection_mode": "transition",
                "allowed_or_disallowed_transitions": {
                    "wa-2": ["wa-3"],
                    "wa-3": ["wa-2"],
                },
            }
        },
    )
    with pytest.raises(ValueError):
        group_manager2.validate_transitions(agent_ids=["wa-2", "wa-4"])

    group_manager3 = HarmonyGroupManager(
        id="wa-1",
        name="group_manager",
        data={  # type: ignore
            "speakers": {
                "selection_mode": "transition",
                "allow_repeat": ["wa-5"],
                "allowed_or_disallowed_transitions": {
                    "wa-2": ["wa-3"],
                    "wa-3": ["wa-2"],
                },
            }
        },
    )
    with pytest.raises(ValueError):
        group_manager3.validate_transitions(agent_ids=["wa-2", "wa-3"])

    group_manager4 = HarmonyGroupManager(
        id="wa-1",
        name="group_manager",
        data={  # type: ignore
            "speakers": {
                "selection_mode": "transition",
                "allow_repeat": ["wa-2"],
                "allowed_or_disallowed_transitions": {
                    "wa-4": ["wa-3"],
                    "wa-3": ["wa-2"],
                },
            }
        },
    )
    with pytest.raises(ValueError):
        group_manager4.validate_transitions(agent_ids=["wa-2", "wa-3"])
