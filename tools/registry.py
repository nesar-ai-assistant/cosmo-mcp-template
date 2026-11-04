"""Single source of truth for the datasets this server exposes.

Keys are short dataset ids used by every tool's ``dataset`` argument.

Schema (family-wide):
    "title":    human name
    "products": {"catalog": [...], "summary_statistic": [...], "published_result": [...]}
        catalog = object-level data; summary_statistic = measurements with covariance;
        published_result = chains / parameter constraints, comparison only ([] when absent)
    "access":   "bundled" | "download" | "remote-query" (+ note on size)
    "urls":     verified source URLs
    "citation": release paper(s)
    "tools":    tools that read it
"""

DATASETS: dict[str, dict] = {
    "example": {
        "title": "Example dataset (replace)",
        "products": {"catalog": ["example catalog"], "summary_statistic": ["example summary statistic"], "published_result": []},
        "access": "bundled",
        "urls": [],
        "citation": "",
        "tools": ["example_load"],
    },
}
