"""Path utilities for output/export directories."""

from __future__ import annotations

from pathlib import Path
import sys

from appdirs import user_data_dir

_APP_DIR_NAME = "leaf_contour_efd"


def _user_writable_base_dir() -> Path:
    """Return a user-writable directory for application outputs."""
    return Path(user_data_dir(_APP_DIR_NAME)).resolve()


def _is_writable_dir(path: Path) -> bool:
    """Return whether ``path`` can be used as a writable directory."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".write_test"
        with probe.open("w", encoding="utf-8"):
            pass
        probe.unlink(missing_ok=True)
        return True
    except OSError:
        return False


def get_output_base_dir() -> Path:
    """Return the base directory used for writing the ``output`` folder.

    Rules
    -----
    - Frozen on all platforms: user-writable application data directory.
    - Non-frozen: repository/application root when writable, otherwise user data.
    """
    fallback = _user_writable_base_dir()

    if getattr(sys, "frozen", False):
        return fallback

    # Development mode: src/leaf_contour_efd/utils/paths.py -> repo root
    repo_root = Path(__file__).resolve().parents[3]
    if _is_writable_dir(repo_root):
        return repo_root
    return fallback


def get_output_dir(*parts: str) -> Path:
    """Return an output subdirectory and ensure it exists.

    If directory creation fails in the primary base location, this function
    transparently falls back to a user-writable directory.
    """
    out_dir = get_output_base_dir() / "output"
    if parts:
        out_dir = out_dir.joinpath(*parts)

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        out_dir = _user_writable_base_dir() / "output"
        if parts:
            out_dir = out_dir.joinpath(*parts)
        out_dir.mkdir(parents=True, exist_ok=True)

    return out_dir
