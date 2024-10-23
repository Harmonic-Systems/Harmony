"""Test harmony.exporting.agents.code_execution."""

from harmony.exporting.agents.code_execution import (
    get_agent_code_execution_config,
)
from harmony.models import (
    HarmonyAgent,
    HarmonyAgentCodeExecutionConfig,
    HarmonyAgentData,
)


def test_get_agent_code_execution_config() -> None:
    """Test get_agent_code_execution_config."""
    # Given
    agent = HarmonyAgent(  # type: ignore
        id="wa-1",
        name="agent1",
        agent_type="assistant",
        data=HarmonyAgentData(  # type: ignore
            code_execution_config=HarmonyAgentCodeExecutionConfig(
                use_docker=None,
                work_dir="work_dir",
                timeout=10,
                last_n_messages=3,
                functions=["ws-1"],
            ),
        ),
    )
    expected_executor = (
        "agent1_executor = LocalCommandLineCodeExecutor(\n"
        '    work_dir="work_dir",\n'
        "    timeout=10.0,\n"
        "    functions=[skill1],\n"
        ")\n\n"
    )
    expected_arg = '{"executor": agent1_executor}'
    expected_imports = "LocalCommandLineCodeExecutor"
    # When
    executor, code_execution_arg, imports = get_agent_code_execution_config(
        agent=agent, agent_name="agent1", skill_names={"ws-1": "skill1"}
    )
    # Then
    assert executor == expected_executor
    assert code_execution_arg == expected_arg
    assert imports == expected_imports


def test_get_agent_code_execution_config_no_code_execution() -> None:
    """Test get_agent_code_execution_config with no code execution."""
    # Given
    agent = HarmonyAgent(  # type: ignore
        id="wa-1",
        name="agent1",
        agent_type="assistant",
        data=HarmonyAgentData(),  # type: ignore
    )
    expected_executor = ""
    expected_arg = "False"
    expected_imports = ""
    # When
    executor, code_execution_arg, imports = get_agent_code_execution_config(
        agent=agent, agent_name="agent1", skill_names={"ws-1": "skill1"}
    )
    # Then
    assert executor == expected_executor
    assert code_execution_arg == expected_arg
    assert imports == expected_imports
