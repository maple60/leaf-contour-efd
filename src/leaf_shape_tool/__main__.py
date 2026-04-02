"""Backward-compatible module runner for ``python -m leaf_shape_tool``."""

from __future__ import annotations

import warnings

from leaf_contour_efd.main import main


if __name__ == "__main__":
    warnings.warn(
        "`python -m leaf_shape_tool` is deprecated; use `python -m leaf_contour_efd`.",
        DeprecationWarning,
        stacklevel=1,
    )
    main()
