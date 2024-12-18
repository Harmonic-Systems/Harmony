"""Test HarmonyRunner."""

# pylint: disable=protected-access

import shutil
from pathlib import Path
from typing import Any

import pytest
from autogen.io import IOStream  # type: ignore

from harmony.models import Harmony, HarmonyFlow
from harmony.runner import HarmonyRunner, get_printer


class CustomIOStream(IOStream):
    """Custom IOStream class."""

    def print(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        flush: bool = False,
    ) -> None:
        """Print objects.

        Parameters
        ----------
        objects : Any
            Objects to print.
        sep : str, optional
            Separator, by default " ".
        end : str, optional
            End, by default 'eol'.
        flush : bool, optional
            Whether to flush, by default False.
        """
        print(*objects, sep=sep, end=end, flush=flush)

    def input(self, prompt: str = "", *, password: bool = False) -> str:
        """Get user input.

        Parameters
        ----------
        prompt : str, optional
            Prompt, by default "".
        password : bool, optional
            Whether to read a password, by default False.

        Returns
        -------
        str
            User input.
        """
        return "User input"


def test_harmony_runner(
    harmony_flow: HarmonyFlow,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test HarmonyRunner.

    Parameters
    ----------
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    tmp_path : Path
        Pytest fixture to create temporary directory.
    capsys : pytest.CaptureFixture[Optional[str]]
        Pytest fixture to capture stdout and stderr.
    """
    harmony = Harmony.from_dict(data=harmony_flow.model_dump(by_alias=True))
    output_path = tmp_path / "output.py"
    runner = HarmonyRunner(harmony)
    with IOStream.set_default(CustomIOStream()):
        runner.run(output_path=output_path)
    std_out = capsys.readouterr().out
    assert "Starting workflow" in std_out
    assert (tmp_path / "harmony_out").exists()
    shutil.rmtree(tmp_path / "harmony_out")


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
    runner.install_requirements()
    std_err = capsys.readouterr().out
    assert (
        "ERROR: No matching distribution found for invalid_requirement"
        in std_err
    )


class BadIOStream(IOStream):
    """Bad IOStream class."""

    def print(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        flush: bool = False,
    ) -> None:
        """Print objects.

        Parameters
        ----------
        objects : Any
            Objects to print.
        sep : str, optional
            Separator, by default " ".
        end : str, optional
            End, by default 'eol'.
        flush : bool, optional
            Whether to flush, by default False.

        Raises
        ------
        UnicodeEncodeError
            If the string is invalid
        """
        raise UnicodeEncodeError("utf-8", "", 0, 1, "invalid string")


def test_get_printer(capsys: pytest.CaptureFixture[str]) -> None:
    """Test get_printer.

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        Pytest fixture to capture stdout and stderr.
    """
    printer = get_printer()
    invalid_str = "This is an invalid string: 🤯"
    printer(invalid_str)
    assert "This is an invalid string: " in capsys.readouterr().out
    invalid_encoded = "This is an invalid encoded string".encode("cp1252")
    printer(invalid_encoded)
    assert "This is an invalid encoded string" in capsys.readouterr().out
    with IOStream.set_default(BadIOStream()):
        printer1 = get_printer()
        printer1(invalid_str)
    assert (
        "Could not print the message due to encoding issues."
        in capsys.readouterr().err
    )
