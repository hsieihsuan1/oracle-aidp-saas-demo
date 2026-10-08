"""Adapted synthetic generator. Local-only; no cloud writes."""
import random

rng = random.Random(42)
from datetime import date, timedelta

import pandas as pd

SUPPLIERS = [
    (500, "Synthetic Supplier 1"),
    (501, "Synthetic Supplier 2"),
    (502, "Synthetic Supplier 3"),
    (503, "Synthetic Supplier 4"),
    (504, "Synthetic Supplier 5"),
]

ITEMS_FOR_PO = [10001, 10002, 10005, 10007, 10011, 10015, 10020,
                10026, 10028, 10034, 10036, 10043, 10045, 10046, 10047]

BRANCHES = ["SP01", "SP02", "RS01", "MG01", "RJ01"]
STATUSES = ["20", "28", "40", "99"]  # Approved, Received, Closed, Cancelled
STATUS_WEIGHTS = [0.4, 0.3, 0.2, 0.1]
LINE_STATUSES = ["20", "28", "40"]


def jde_date(d: date) -> int:
    """Converte date para formato JDE CYYDDD."""
    century = 1 if d.year >= 2000 else 0
    yy = d.year % 100
    ddd = d.timetuple().tm_yday
    return century * 100000 + yy * 1000 + ddd


def generate_po_header(n: int = 25) -> pd.DataFrame:
    rows = []
    base_date = date(2026, 1, 1)
    for i in range(n):
        order_date = base_date + timedelta(days=rng.randint(0, 115))
        req_date = order_date + timedelta(days=rng.randint(7, 30))
        supp_id, _ = rng.choice(SUPPLIERS)
        status = rng.choices(STATUSES, STATUS_WEIGHTS)[0]
        rows.append({
            "PHDOCO": 4000 + i + 1,
            "PHDCTO": "OP",
            "PHKCOO": "00001",
            "PHVEND": supp_id,
            "PHTRDJ": jde_date(order_date),
            "PHDRQJ": jde_date(req_date),
            "PHST": status,
            "PHCO": "00001",
        })
    return pd.DataFrame(rows)


def generate_po_detail(df_header: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, hdr in df_header.iterrows():
        n_lines = rng.randint(1, 5)
        items = rng.sample(ITEMS_FOR_PO, k=min(n_lines, len(ITEMS_FOR_PO)))
        for j, itm in enumerate(items):
            qty = round(rng.uniform(10, 500), 2)
            unit_cost = round(rng.uniform(5, 2000), 2)
            qty_open = qty if hdr["PHST"] == "20" else round(qty * rng.uniform(0, 0.3), 2)
            rows.append({
                "PDDOCO": hdr["PHDOCO"],
                "PDDCTO": "OP",
                "PDLNID": (j + 1) * 1.0,
                "PDITM": itm,
                "PDMCU": rng.choice(BRANCHES),
                "PDUORG": qty,
                "PDUOPN": qty_open,
                "PDPRRC": unit_cost,
                "PDAOPN": round(qty_open * unit_cost, 2),
                "PDST": "20" if qty_open > 0 else "40",
            })
    return pd.DataFrame(rows)
