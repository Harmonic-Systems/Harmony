"""Command line interface to convert or run a harmony file."""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional

from . import Harmony, __version__
from .exporter import HarmonyExporter
from .runner import HarmonyRunner

if TYPE_CHECKING:
    from autogen import ChatResult  # type: ignore[import-untyped]


def get_parser() -> argparse.ArgumentParser:
    """Get the argument parser for the Harmony package.

    Returns
    -------
    argparse.ArgumentParser
        The argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Run or export a Harmony flow.",
        prog="harmony",
    )
    parser.add_argument(
        "file",
        type=str,
        help="Path to the Harmony flow (*.harmony) file.",
    )
    parser.add_argument(
        "-e",
        "--export",
        action="store_true",
        help=(
            "Export the Harmony flow to a Python script or a jupyter notebook."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help=(
            "Path to the output file. "
            "If exporting, the file extension determines the output format. "
            "If running, the output's directory will contain "
            "the generated flow (.py) and any additional generated files."
        ),
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help=("Override the output file if it already exists. "),
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"harmony version: {__version__}",
    )
    return parser


def _log_result(result: "ChatResult") -> None:
    """Log the result of the Harmony flow."""
    logger = logging.getLogger("harmony::cli")
    logger.info("Chat History:\n")
    logger.info(result.chat_history)
    logger.info("Summary:\n")
    logger.info(result.summary)
    logger.info("Cost:\n")
    logger.info(result.cost)


def _run(data: Dict[str, Any], output_path: Optional[str]) -> None:
    """Run the Harmony flow."""
    harmony = Harmony.from_dict(data)
    runner = HarmonyRunner(harmony)
    results = runner.run(stream=None, output_path=output_path)
    if isinstance(results, list):
        for result in results:
            _log_result(result)
            sep = "-" * 80
            print(f"\n{sep}\n")
    else:
        _log_result(results)


def main() -> None:
    """Parse the command line arguments and run the Harmony flow."""
    parser = get_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    args = parser.parse_args()
    logger = _get_logger()
    harmony_file: str = args.file
    if not os.path.exists(harmony_file):
        logger.error("File not found: %s", harmony_file)
        sys.exit(1)
    if not harmony_file.endswith((".json", ".harmony")):
        logger.error("Only .json or .harmony files are supported.")
        sys.exit(1)
    with open(harmony_file, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            logger.error("Invalid .harmony file: %s. Not a valid json?", file)
            return
    if args.export is True:
        if args.output is None:
            logger.error("Please provide an output file.")
            sys.exit(1)
        if not args.output.endswith((".py", ".ipynb", ".json", ".harmony")):
            logger.error(
                "Only Python scripts, Jupyter notebooks "
                "and JSON/Harmony files are supported."
            )
            sys.exit(1)
        output_file = Path(args.output).resolve()
        harmony = Harmony.from_dict(data)
        exporter = HarmonyExporter(harmony)
        exporter.export(output_file, force=args.force)
        generated = str(output_file).replace(os.getcwd(), ".")
        logger.info("Generated: %s", generated)
    else:
        _run(data, args.output)


def _get_logger(level: int = logging.INFO) -> logging.Logger:
    """Get the logger for the Harmony package.

    Parameters
    ----------
    level : int or str, optional
        The logging level. Default is logging.INFO.

    Returns
    -------
    logging.Logger
        The logger.
    """
    # check if we already have setup a config

    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=level,
            format="%(levelname)s %(message)s",
            stream=sys.stderr,
            force=True,
        )
    logger = logging.getLogger("harmony::cli")
    current_level = logger.getEffectiveLevel()
    if current_level != level:
        logger.setLevel(level)
    return logger


if __name__ == "__main__":
    main()
