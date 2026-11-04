"""Single source of truth for the datasets this server exposes.

Keys are short dataset ids used by every tool's ``dataset`` argument.

Schema (family-wide):
    "title":    human name
    "products": {"tier1": [...], "tier2": [...], "tier3": [...]}   (omit / [] when absent)
        tier1 = raw / catalog-level, tier2 = summary statistics + covariance,
        tier3 = published inference (chains, parameter constraints) - comparison only
    "access":   "bundled" | "download" | "remote-query" (+ note on size)
    "urls":     verified source URLs
    "citation": release paper(s)
    "tools":    tools that read it
"""

DATASETS: dict[str, dict] = {
    "example": {
        "title": "Example dataset (replace)",
        "products": {"tier1": ["example catalog"], "tier2": ["example summary statistic"], "tier3": []},
        "access": "bundled",
        "urls": [],
        "citation": "",
        "tools": ["example_load"],
    },
}
