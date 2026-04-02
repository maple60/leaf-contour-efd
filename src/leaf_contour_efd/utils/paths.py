"""Path utilities for output/export directories."""

from __future__ import annotations

from pathlib import Path
import sys


def _find_macos_app_bundle(executable_path: Path) -> Path | None:
    """Return the nearest ``*.app`` bundle path if the executable is inside it."""
    for parent in executable_path.parents:
        if parent.suffix.lower() == ".app":
            return parent
    return None


def get_output_base_dir() -> Path:
    """Return the base directory used for writing the ``output`` folder.

    Rules
    -----
    - Frozen on Windows/Linux: directory containing the executable.
    - Frozen macOS ``.app``: parent directory of ``MyApp.app``.
    - Non-frozen: repository/application root based on this source file location.
    """
    if getattr(sys, "frozen", False):
        executable_path = Path(sys.executable).resolve()
        if sys.platform == "darwin":
            app_bundle = _find_macos_app_bundle(executable_path)
            if app_bundle is not None:
                return app_bundle.parent
        return executable_path.parent

    # Development mode: src/leaf_contour_efd/utils/paths.py -> repo root
    return Path(__file__).resolve().parents[3]


def get_output_dir(*parts: str) -> Path:
    """Return an output subdirectory and ensure it exists."""
    out_dir = get_output_base_dir() / "output"
    if parts:
        out_dir = out_dir.joinpath(*parts)
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir
