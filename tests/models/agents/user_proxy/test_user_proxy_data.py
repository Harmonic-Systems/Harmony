"""Test harmony.models.agents.user_proxy.user_proxy_data.*."""

from harmony.models.agents.user_proxy.user_proxy_data import (
    HarmonyUserProxyData,
)


def test_harmony_user_proxy_data() -> None:
    """Test HarmonyUserProxyData."""
    user_proxy_data = HarmonyUserProxyData()  # type: ignore
    assert user_proxy_data.human_input_mode == "ALWAYS"
