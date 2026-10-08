# Local verification

Verified October 8, 2026 on Linux / Python 3.10 using a new isolated virtual environment and a fresh requirements install.

- 20 pytest cases passed, including execution of every notebook code cell without saved outputs.
- Browser smoke passed all four UI scenarios using real local HTTP requests and Chromium. Captured the integrated query as `demo-running.png`.
- JavaScript syntax check passed.
- Python compile check passed.
- Release-content heuristic passed. No private history, live connectors, Parquet artifacts, credential files or original notebook outputs are packaged.
- Visually inspected the captured integrated-query screen: three supplier rows, readable synthetic labels, BRL column names, frozen snapshot date, visible fixed SQL and two invented policy citations. No overlap or clipping in the inspected desktop view.

One warning remains: the installed FastAPI/Starlette TestClient announces deprecation of its httpx test transport. Tests pass; this is not a failed runtime request. No remote CI run or Oracle deployment was performed.

The content scanner is heuristic only and does not establish a complete security audit. The screenshot shows a local demo, not Oracle cloud execution.
