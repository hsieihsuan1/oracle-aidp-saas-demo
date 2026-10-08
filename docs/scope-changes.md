# Public candidate scope changes

This candidate is staged for review. No new repository has been created, nothing has been published, and the profile README has not changed.

## Naming decision

Suggested public name: `oracle-aidp-saas-demo`. The README title and first paragraph explicitly say "AIDP-inspired" and "local". A more neutral option is `enterprise-data-workspace-demo` if avoiding the implication of a live cloud deployment matters more than preserving the source project's name. Publication and profile wording need review.

## Preserved and adapted

- Original inventory, purchasing, manufacturing and financial generator functions and ERP-style field names.
- Seeded local random generators; replaced realistic personal user labels and supplier names with explicit synthetic labels.
- Trimmed Oracle analytical table definitions, marked untested reference only. Removed document vector store DDL, user creation and credential configuration. Removed the source's misleading F3111 work-order-header mapping; remaining field names are illustrative.
- Source AP snapshot date 2026-04-26, stated prominently rather than presented as current data.

## Replaced

- Source notebooks had indentation/syntax failures. Replaced them with one small executable local worksheet, verified through tests, rather than advertising a cloud notebook run.
- A SQLite read-only workspace, fixed query API and static UI replace the Oracle execution path.
- Synthetic financial/operational joins plus static policy citations replace Select AI/vector-search claims. No hidden mock LLM response or simulated vector score.
- Newly added test suite, browser smoke and candidate-only CI workflow.

## Excluded

Live JDE/Fusion connectors, including the JDE path that disabled certificate verification; OCI credentials and auth flows; provisioning; source generated Parquet files; original notebooks and their outputs; personal details; private source URLs; cloud validation scripts. Cloud services were not provisioned, tested or billed.

The source README described more than the public candidate implements. The source Select AI SQL used an OCI model configuration rather than validating the README's Gemini claim. Neither claim is carried into this candidate.

## Review before publication

Confirm name and this reduced, accurately labeled local scope. The screenshot shows the actual synthetic integrated query with three result rows, not a mock cloud dashboard. The README lists limitations. The Oracle reference is not a working cloud deployment. Publishing, setting GitHub metadata and adding a profile link remain separate review steps.
