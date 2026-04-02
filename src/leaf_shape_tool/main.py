"""Backward-compatible entry point for ``leaf_shape_tool``.

Deprecated: use ``leaf_contour_efd.main`` instead.
"""

from __future__ import annotations

import warnings

from leaf_contour_efd.main import main as _main


def main() -> None:
    warnings.warn(
        "`leaf_shape_tool.main` is deprecated; use `leaf_contour_efd.main`.",
        DeprecationWarning,
        stacklevel=2,
    )
    _main()


if __name__ == "__main__":
    main()
