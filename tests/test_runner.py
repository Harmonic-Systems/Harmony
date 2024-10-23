"""Test HarmonyRunner."""

# pylint: disable=protected-access

from typing import Optional

import pytest

from harmony import Harmony, HarmonyIOStream, HarmonyRunner
from harmony.models import HarmonyFlow


def test_runner(harmony_flow: HarmonyFlow) -> None:
    """Test HarmonyRunner.

    Parameters
    ----------
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    runner = HarmonyRunner(harmony)
    assert runner.harmony == harmony
    assert not runner.running

    prompt_input: Optional[str] = None
    stream: HarmonyIOStream

    def on_prompt_input(prompt: str) -> None:
        nonlocal prompt_input, stream
        prompt_input = prompt
        stream.forward_input("Reply to prompt\n")

    stream = HarmonyIOStream(
        on_prompt_input=on_prompt_input,
        print_function=print,
        input_timeout=2,
    )
    with HarmonyIOStream.set_default(stream):
        runner.run(stream)
    assert not runner.running
    assert runner._stream.get() is None
    assert prompt_input is not None
    stream.close()


def test_harmony_with_invalid_requirement(
    capsys: pytest.CaptureFixture[str],
    harmony_flow: HarmonyFlow,
) -> None:
    """Test Harmony with invalid requirement.

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        Pytest fixture to capture stdout and stderr.
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    flow_dict = harmony_flow.model_dump(by_alias=True)
    # add an invalid requirement
    flow_dict["requirements"] = ["invalid_requirement"]
    harmony = Harmony.from_dict(data=flow_dict)
    runner = HarmonyRunner(harmony)
    runner._install_requirements()
    std_err = capsys.readouterr().out
    assert (
        "ERROR: No matching distribution found for invalid_requirement"
        in std_err
    )
