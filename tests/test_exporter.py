"""Test HarmonyExporter."""

import uuid
from pathlib import Path

import pytest

from harmony import Harmony, HarmonyExporter
from harmony.models import HarmonyFlow

from .exporting.flow_helpers import get_flow


def test_export_load_from_file(
    tmp_path: Path, harmony_flow: HarmonyFlow
) -> None:
    """Test exporting and loading from file.

    Parameters
    ----------
    tmp_path : Path
        A pytest fixture to provide a temporary directory.
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_file = tmp_path / f"{uuid.uuid4().hex}.harmony"
    exporter.export(str(output_file))
    assert output_file.exists()
    HarmonyExporter.load(output_file)
    output_file.unlink(missing_ok=True)


def test_exporter_load_invalid_path() -> None:
    """Test exporter load invalid path."""
    with pytest.raises(ValueError):
        HarmonyExporter.load(Path("non_existent_file"))


def test_exporter_use_directory(
    tmp_path: Path, harmony_flow: HarmonyFlow
) -> None:
    """Test exporter use directory.

    Parameters
    ----------
    tmp_path : Path
        A pytest fixture to provide a temporary directory.
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_dir = tmp_path / f"{uuid.uuid4().hex}.harmony"
    output_dir.mkdir()
    with pytest.raises(IsADirectoryError):
        exporter.export(output_dir)
    output_dir.rmdir()


def test_exporter_file_exists(
    tmp_path: Path, harmony_flow: HarmonyFlow
) -> None:
    """Test exporter file exists.

    Parameters
    ----------
    tmp_path : Path
        A pytest fixture to provide a temporary directory.
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_file = tmp_path / f"{uuid.uuid4().hex}.harmony"
    output_file.touch()
    with pytest.raises(FileExistsError):
        exporter.export(output_file)
    exporter.export(output_file, force=True)
    output_file.unlink(missing_ok=True)


def test_exporter_force(tmp_path: Path, harmony_flow: HarmonyFlow) -> None:
    """Test exporter force.

    Parameters
    ----------
    tmp_path : Path
        A pytest fixture to provide a temporary directory.
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_file = tmp_path / f"{uuid.uuid4().hex}.harmony"
    output_file.touch()
    exporter.export(output_file, force=True)
    output_file.unlink(missing_ok=True)


def test_export_to_py(tmp_path: Path, harmony_flow: HarmonyFlow) -> None:
    """Test exporting to Python.

    Parameters
    ----------
    tmp_path : Path
        A pytest fixture to provide a temporary directory.
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_file = tmp_path / f"{uuid.uuid4().hex}.py"
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink(missing_ok=True)


def test_export_to_ipynb(tmp_path: Path, harmony_flow: HarmonyFlow) -> None:
    """Test exporting to Jupyter Notebook.

    Parameters
    ----------
    tmp_path : Path
        A pytest fixture to provide a temporary directory.
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_file = tmp_path / f"{uuid.uuid4().hex}.ipynb"
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink(missing_ok=True)


def test_export_to_harmony(tmp_path: Path, harmony_flow: HarmonyFlow) -> None:
    """Test exporting to Harmony file.

    Parameters
    ----------
    tmp_path : Path
        A pytest fixture to provide a temporary directory.
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_file = tmp_path / f"{uuid.uuid4().hex}.harmony"
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink(missing_ok=True)


def test_export_to_invalid_extension(
    tmp_path: Path, harmony_flow: HarmonyFlow
) -> None:
    """Test exporting to invalid extension.

    Parameters
    ----------
    tmp_path : Path
        A pytest fixture to provide a temporary directory.
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_file = tmp_path / f"{uuid.uuid4().hex}.invalid"
    with pytest.raises(ValueError):
        exporter.export(output_file)


def test_export_complex_flow(tmp_path: Path) -> None:
    """Test exporting invalid flow.

    Parameters
    ----------
    tmp_path : Path
        A pytest fixture to provide a temporary directory.
    """
    flow = get_flow()
    harmony = Harmony(flow=flow)
    exporter = HarmonyExporter(harmony)
    output_file = tmp_path / f"{uuid.uuid4().hex}.py"
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink()
    skill_file = tmp_path / "skill_name.py"
    assert skill_file.exists()
    skill_file.unlink(missing_ok=True)
