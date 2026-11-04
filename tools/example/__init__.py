"""Example tool family (template - replace)."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field, validate_call

from ..common import ArtifactResult, ok, data_kind, resolve_outdir

__all__ = ["example_load", "example_summary"]

DISPATCH_KERNELS: dict = {}


@data_kind("catalog")
@validate_call
def example_load(output_dir: Annotated[str, Field(description="Where files are written.")]) -> ArtifactResult:
    """Template tool."""
    out = resolve_outdir(output_dir)
    path = out / "example.csv"
    path.write_text("x,y\n0,0\n")
    return ok("wrote example", [path], n_rows=1)


@data_kind("summary_statistic")
@validate_call
def example_summary(output_dir: Annotated[str, Field(description="Where files are written.")]) -> ArtifactResult:
    """Template summary-statistic tool."""
    return example_load(output_dir)
