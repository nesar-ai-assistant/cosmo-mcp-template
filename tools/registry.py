"""Single source of truth for the datasets this server exposes.

Keys are short dataset ids used by every tool's ``dataset`` argument.
"access" is "bundled" (file in data/), "download" (fetched on first use
into the data cache) or "remote-query" (live service).
"""

DATASETS: dict[str, dict] = {
    "example": {
        "title": "Example dataset (replace)",
        "products": ["table"],
        "access": "bundled",
        "urls": [],
        "citation": "",
        "tools": ["example_load"],
    },
}
