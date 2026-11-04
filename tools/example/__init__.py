"""Example tool family (template - replace)."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field, validate_call

from ..common import ArtifactResult, ok, resolve_outdir, tier

__all__ = ["example_load", "example_summary"]

DISPATCH_KERNELS: dict = {}


@tier(1)
@validate_call
def example_load(output_dir: Annotated[str, Field(description="Where files are written.")]) -> ArtifactResult:
    """Template tool."""
    out = resolve_outdir(output_dir)
    path = out / "example.csv"
    path.write_text("x,y\n0,0\n")
    return ok("wrote example", [path], n_rows=1)


@tier(2)
@validate_call
def example_summary(output_dir: Annotated[str, Field(description="Where files are written.")]) -> ArtifactResult:
    """Template tier-2 tool (summary statistic)."""
    return example_load(output_dir)
