"""Test the CLI."""

import re
import sys
from pathlib import Path

import pytest

from harmony import __version__
from harmony.__main__ import app as harmony_main  # type: ignore
from harmony.cli import app
from harmony.models import HarmonyFlow


def escape_ansi(text: str) -> str:
    """Remove ANSI escape sequences from a string.

    Parameters
    ----------
    text : str
        The text to process.

    Returns
    -------
    str
        The text without ANSI escape sequences.
    """
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", text)


def test_get_version(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the get_version function.

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        Pytest fixture to capture stdout and stderr.
    """
    with pytest.raises(SystemExit):
        sys.argv = ["harmony", "--version"]
        app()
    captured = capsys.readouterr()
    assert __version__ in captured.out


def test_help(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the help message.

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        Pytest fixture to capture stdout and stderr.
    """
    with pytest.raises(SystemExit):
        sys.argv = ["harmony", "--help"]
        harmony_main()
    captured = capsys.readouterr()
    assert "Usage: harmony" in escape_ansi(captured.out)


def test_empty_cli(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the CLI with no arguments.

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        Pytest fixture to capture stdout and stderr.
    """
    with pytest.raises(SystemExit):
        sys.argv = ["harmony"]
        harmony_main()
    captured = capsys.readouterr()
    assert "Usage: harmony" in escape_ansi(captured.out)


def test_cli_export(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    harmony_flow: HarmonyFlow,
) -> None:
    """Test exporting a HarmonyFlow using the CLI.

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        Pytest fixture to capture stdout and stderr.
    tmp_path : Path
        Pytest fixture to provide a temporary directory.
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    input_file = tmp_path / f"{harmony_flow.name}.harmony"
    with open(input_file, "w", encoding="utf-8") as file:
        file.write(harmony_flow.model_dump_json(by_alias=True))
    output_file = tmp_path / f"{harmony_flow.name}.ipynb"
    sys.argv = [
        "harmony",
        "convert",
        "--output",
        str(output_file),
        "--file",
        str(input_file),
    ]
    with pytest.raises(SystemExit):
        harmony_main()
    captured = capsys.readouterr()
    assert "Generated" in escape_ansi(captured.out)
    assert output_file.exists()
    output_file.unlink(missing_ok=True)


def test_cli_run(
    caplog: pytest.LogCaptureFixture,
    tmp_path: Path,
    harmony_flow_no_human_input: HarmonyFlow,
) -> None:
    """Test running a HarmonyFlow using the CLI.

    Parameters
    ----------
    caplog : pytest.LogCaptureFixture
        Pytest fixture to capture logs.
    tmp_path : Path
        Pytest fixture to provide a temporary directory.
    harmony_flow_no_human_input : HarmonyFlow
        A HarmonyFlow instance with no human input.
    """
    input_file = tmp_path / f"{harmony_flow_no_human_input.name}.harmony"
    with open(input_file, "w", encoding="utf-8") as file:
        file.write(harmony_flow_no_human_input.model_dump_json(by_alias=True))
    sys.argv = ["harmony", "run", "--file", str(input_file)]
    with pytest.raises(SystemExit):
        harmony_main()
    assert "Summary" in caplog.text


def test_cli_check(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    harmony_flow_no_human_input: HarmonyFlow,
) -> None:
    """Test checking a HarmonyFlow using the CLI.

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        Pytest fixture to capture stdout and stderr.
    tmp_path : Path
        Pytest fixture to provide a temporary directory.
    harmony_flow_no_human_input : HarmonyFlow
        A HarmonyFlow instance with no human input.
    """
    input_file = tmp_path / f"{harmony_flow_no_human_input.name}.harmony"
    with open(input_file, "w", encoding="utf-8") as file:
        file.write(harmony_flow_no_human_input.model_dump_json(by_alias=True))
    sys.argv = ["harmony", "check", "--file", str(input_file)]
    with pytest.raises(SystemExit):
        harmony_main()
    captured = capsys.readouterr()
    assert "Harmony flow is valid" in escape_ansi(captured.out)
