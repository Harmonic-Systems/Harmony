"""Test HarmonyExporter."""

from pathlib import Path

import pytest

from harmony import Harmony, HarmonyExporter
from harmony.models import HarmonyFlow

from .exporting.flow_helpers import get_flow


def test_export_load_from_file(harmony_flow: HarmonyFlow) -> None:
    """Test exporting and loading from file.

    Parameters
    ----------
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_file = Path("flow.harmony")
    exporter.export(str(output_file))
    assert output_file.exists()
    HarmonyExporter.load(output_file)
    output_file.unlink()


def test_exporter_load_invalid_path() -> None:
    """Test exporter load invalid path."""
    with pytest.raises(ValueError):
        HarmonyExporter.load(Path("non_existent_file"))


def test_exporter_use_directory(harmony_flow: HarmonyFlow) -> None:
    """Test exporter use directory.

    Parameters
    ----------
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_dir = Path("output_dir.harmony")
    output_dir.mkdir()
    with pytest.raises(IsADirectoryError):
        exporter.export(output_dir)
    output_dir.rmdir()


def test_exporter_file_exists(harmony_flow: HarmonyFlow) -> None:
    """Test exporter file exists.

    Parameters
    ----------
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_file = Path("flow.harmony")
    output_file.touch()
    with pytest.raises(FileExistsError):
        exporter.export(output_file)
    exporter.export(output_file, force=True)
    output_file.unlink()


def test_exporter_force(harmony_flow: HarmonyFlow) -> None:
    """Test exporter force.

    Parameters
    ----------
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_file = Path("flow.harmony")
    output_file.touch()
    exporter.export(output_file, force=True)
    output_file.unlink()


def test_export_to_py(harmony_flow: HarmonyFlow) -> None:
    """Test exporting to Python.

    Parameters
    ----------
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_file = Path("harmony.py")
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink()


def test_export_to_ipynb(harmony_flow: HarmonyFlow) -> None:
    """Test exporting to Jupyter Notebook.

    Parameters
    ----------
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_file = Path("harmony.ipynb")
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink()


def test_export_to_harmony(harmony_flow: HarmonyFlow) -> None:
    """Test exporting to Harmony file.

    Parameters
    ----------
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_file = Path("harmony.harmony")
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink()


def test_export_to_invalid_extension(harmony_flow: HarmonyFlow) -> None:
    """Test exporting to invalid extension.

    Parameters
    ----------
    harmony_flow : HarmonyFlow
        A HarmonyFlow instance.
    """
    harmony = Harmony(flow=harmony_flow)
    exporter = HarmonyExporter(harmony)
    output_file = Path("harmony.invalid")
    with pytest.raises(ValueError):
        exporter.export(output_file)


def test_export_complex_flow() -> None:
    """Test exporting invalid flow."""
    flow = get_flow()
    harmony = Harmony(flow=flow)
    exporter = HarmonyExporter(harmony)
    output_file = Path("flow.py")
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink()
    skill_file = Path("skill_name.py")
    assert skill_file.exists()
    skill_file.unlink()
