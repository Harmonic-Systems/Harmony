"""Test the CLI."""

import argparse
import sys
from pathlib import Path

import pytest

from harmony import __version__
from harmony.__main__ import main as harmony_main  # type: ignore
from harmony.cli import get_parser, main
from harmony.models import HarmonyFlow


def test_get_parser() -> None:
    """Test the get_parser function."""
    parser = get_parser()
    assert isinstance(parser, argparse.ArgumentParser)


def test_get_version(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the get_version function.

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        Pytest fixture to capture stdout and stderr.
    """
    with pytest.raises(SystemExit):
        sys.argv = ["harmony", "--version"]
        main()
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
    assert "usage: harmony" in captured.out


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
    assert "usage: harmony" in captured.out


def test_cli_export(
    caplog: pytest.LogCaptureFixture,
    tmp_path: Path,
    harmony_flow: HarmonyFlow,
) -> None:
    """Test exporting a HarmonyFlow using the CLI.

    Parameters
    ----------
    caplog : pytest.LogCaptureFixture
        Pytest fixture to capture logs.
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
        "--export",
        "--output",
        str(output_file),
        str(input_file),
    ]
    harmony_main()
    assert "Generated" in caplog.text
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
    sys.argv = ["harmony", str(input_file)]
    harmony_main()
    assert "Summary" in caplog.text
