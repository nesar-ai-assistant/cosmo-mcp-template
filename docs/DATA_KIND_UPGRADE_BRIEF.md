# Data-kind upgrade brief

> REVISION: the user does NOT want "tier 1/2/3" labels anywhere in the servers ("it's the content that matters,
> not the label"). Use `@data_kind("catalog" | "summary_statistic" | "published_result" | "meta")`, registry
> products keyed `catalog` / `summary_statistic` / `published_result`, and plain wording in docs/skills/README
> (e.g. "Data products" table with columns Catalogs / Summary statistics / Published results). The tier wording
> below maps tier 1 = catalog, tier 2 = summary_statistic, tier 3 = published_result.
 (cosmo-*-mcp-server family, 2026-11)

The user (Nesar, Argonne cosmologist) distinguishes three DATA TIERS:
- **Tier 1, raw / catalog-level:** per-object catalogs, photometry and light curves, per-SN SALT2 fits, shear catalogs, CMB maps, galaxy + random catalogs.
- **Tier 2, processed summary statistics measured from tier 1, with covariance:**
  - ξ±, C_ℓ, CMB bandpowers
  - P(k)/ξ(s) multipoles, BAO D/r_d
  - Hubble diagram μ(z), binned cluster counts
  - n(z), selection functions / completeness, stacked profiles
- **Tier 3, fully processed inference:** posterior chains, S8/H0/Ωm constraints, best-fit theory spectra. These are COMPARISON ONLY.

hep-genesis-agent analyses must be built on tier 1 and tier 2. Tier 3 is used only for comparison and must never be confused with data.

## What is already done (do NOT redo or edit)
The template at `~/github-integration/cosmo-mcp-template` (pushed to GitHub, commit ab5a383) now has:
- `tools/common.py`: `TIERS`, `TIER3_NOTICE`, and the `@tier(1|2|3|"meta")` decorator. Put the decorator ABOVE `@validate_call`. It sets `fn.data_tier` and stamps `metadata["data_tier"]` on results; tier-3 results also get `tier3_notice`.
- `mcp_server/server.py`: prefixes every tiered tool's description with `[TIER n ...]`.
- `tools/meta/__init__.py`: `list_<p>_datasets(tier=...)` reports tier counts. Meta tools are tagged "meta".
- `tests/test_contract.py`: new tests require all of the following:
  - `@tier` on every science tool
  - `tools/registry.py` `products` given as a dict `{"tier1": [...], "tier2": [...], "tier3": [...]}`
  - at least 1 tier-1 and at least 1 tier-2 dataset
  - at least 1 tier-1 and at least 1 tier-2 tool
- `docs/CONVENTIONS.md`: a "Data tiers" section. READ IT.

These five files have ALREADY been copied into your server and must stay byte-identical to the template: `mcp_server/server.py`, `tools/common.py`, `tools/meta/__init__.py`, `tests/test_contract.py`, `docs/CONVENTIONS.md`. Your server currently fails 4 contract tests; your job makes them pass.

## Your job (one server, independently; do not touch other repos or ~/.hermes)
1. **Classify** every dataset and product in `tools/registry.py` into tier1 / tier2 / tier3 using the dict schema. Tag EVERY tool with `@tier(...)`:
   - fetch/plot of catalogs: 1
   - data vectors / bandpowers / Hubble diagram / BAO, and the fits run on them: 2. A fit's output is the user's own inference from tier-2 data, so the tool is tier 2.
   - chains, published-constraint comparisons, best-fit theory files: 3
   - mixed tools: tag by their PRIMARY input
2. **Separate tiers in tools.** No tool may silently use a tier-3 product as a measurement or prior.
   - Explicit Gaussian priors given as user arguments are allowed, but must be labelled in the output.
   - Tier-3 tools keep working (comparison), but their docstrings must say "comparison only".
   - Rename where it helps clarity, e.g. `compare_*_with_published_*`. If you rename, update skills, tests and README.
3. **ADD REAL tier-1 and tier-2 data and tools where they are missing or thin.** This is the main work; see your server-specific list.
   - Large tier-1 data downloads on demand as SUBSETS (sky patch, tile, z-range, nside, row limit) through `tools.common.fetch_file` or streaming/TAP queries. Never download everything.
   - Each heavy tier-1 → tier-2 reduction must be:
     - a pure kernel in `<family>/kernels.py` (numpy/scipy/astropy plus declared pip_deps, JSON in, JSON out, files to cwd)
     - a `DISPATCH_KERNELS` entry
     - a `remote_site()/run_kernel()` branch, exactly as in CONVENTIONS.md
     - `fn.weight = "heavy"`

     Examples: measuring ξ(s) or P(k) multipoles from a galaxy+random catalog, ξ± from a shear catalog with treecorr, C_ℓ from a HEALPix map with healpy, SALT2 standardisation → μ(z).
   - VERIFY EVERY URL by downloading (or for huge files, a HEAD request plus a partial or subset fetch). Never invent URLs or numbers.
   - If a tier-1 product is genuinely not public or not downloadable without credentials, say so in registry `access` and README, and give the tool a clear error with manual steps.
4. **Skills:**
   - Update `<p>-tour.md` to walk tier 1 → tier 2 → own fit, then a final "compare with published (tier 3)" step.
   - Add at least 1 new science recipe that starts from tier-1 data and produces a tier-2 statistic, including sanity numbers from YOUR actual runs.
   - Keep `hpc-dispatch-handoff.md` current with the kernel list.
5. **README:** add a "Data tiers" table listing every dataset with its tier-1/2/3 products and access mode.
6. **Verify:** `.venv/bin/ruff check tools mcp_server tests`; `MPLBACKEND=Agg .venv/bin/python -m pytest -q`, network tests included, all passing; `.venv/bin/python tests/smoke_server.py`.
   - Run each new tier-1 → tier-2 tool once for real and sanity-check the numbers against the literature.
   - Save 1–2 new PNGs to `docs/figures/`.
   - You cannot view images, so check plots programmatically: not blank, axis ranges sane.
7. **Git:**
   - `git add -A && git commit -m "Data tiers: ..."` and then `git push` (the origin remote is github.com/nesar-ai-assistant/<repo>; gh is authenticated).
   - Then check CI with `gh run list -R nesar-ai-assistant/<repo> -L1`. CI runs `pytest -m "not network"` on ubuntu; make sure offline tests don't need downloads.

## Final report
- tier table: dataset → tier1 / tier2 / tier3 products
- new tools: name, tier, one line each
- new kernels
- tier-1 → tier-2 sanity numbers versus literature
- test lines (pytest + smoke), commit hash, CI status
- honest gaps: what isn't public, or what you couldn't verify
