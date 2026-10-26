# ru_isp_successors

Find successors of Russian service providers by name and active period.

    python3 ru_isp_successors/successors.py "Интел-Тел" --period 2018-2020
    python3 ru_isp_successors/successors.py "Gorcom" --min-confidence medium

Data lives in `data.json` (entities + directed edges with dates, confidence, source).
Confidence is `high/medium/low/unverified`; nothing is `high` until confirmed in EGRUL.
Tests: `python3 -m pytest ru_isp_successors` (or run the test functions directly).
