"""Test harmony.models.agents.user_proxy.user_proxy.*."""

from harmony.models.agents.user_proxy.user_proxy import HarmonyUserProxy


def test_harmony_user_proxy() -> None:
    """Test HarmonyUserProxy."""
    user_proxy = HarmonyUserProxy(id="wa-1", name="user")  # type: ignore
    assert user_proxy.data.human_input_mode == "ALWAYS"
    assert user_proxy.agent_type == "user"
