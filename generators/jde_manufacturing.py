"""Adapted synthetic generator. Local-only; no cloud writes."""
import random

rng = random.Random(42)
from datetime import date, timedelta

import pandas as pd


FINISHED_GOODS = [
    (20001, "CONJUNTO-HID-A", "Conjunto Hidráulico Modelo A"),
    (20002, "CONJUNTO-HID-B", "Conjunto Hidráulico Modelo B"),
    (20003, "PAINEL-ELETRICO-C", "Painel Elétrico de Controle C"),
    (20004, "SISTEMA-PUMP-X", "Sistema de Bombeamento X"),
    (20005, "MODULO-FILTR", "Módulo de Filtração Industrial"),
]

BRANCHES = ["SP01", "SP02", "MG01"]
WO_STATUSES = [
    ("10", "Proposed"),
    ("20", "Approved"),
    ("30", "In Process"),
    ("40", "In Process"),
    ("95", "Completed"),
    ("99", "Closed"),
]


def jde_date(d: date) -> int:
    century = 1 if d.year >= 2000 else 0
    yy = d.year % 100
    ddd = d.timetuple().tm_yday
    return century * 100000 + yy * 1000 + ddd


def generate_work_orders(n: int = 20) -> pd.DataFrame:
    rows = []
    base = date(2026, 1, 15)

    for i in range(n):
        itm_id, litm, dsc = rng.choice(FINISHED_GOODS)
        start = base + timedelta(days=rng.randint(0, 100))
        req = start + timedelta(days=rng.randint(5, 20))
        status_code, _ = rng.choices(
            WO_STATUSES,
            weights=[0.05, 0.15, 0.3, 0.2, 0.2, 0.1]
        )[0]

        qty_ord = round(rng.uniform(5, 100), 2)
        if status_code in ("95", "99"):
            qty_comp = qty_ord
        elif status_code in ("30", "40"):
            qty_comp = round(qty_ord * rng.uniform(0.1, 0.8), 2)
        else:
            qty_comp = 0.0

        rows.append({
            "WADOCO": 7000 + i + 1,
            "WADCTO": "WO",
            "WADRQJ": jde_date(req),
            "WASTRT": jde_date(start),
            "WAITMK": itm_id,
            "WAMCU": rng.choice(BRANCHES),
            "WAUORG": qty_ord,
            "WAWQTY": qty_ord - qty_comp,
            "WACMPL": qty_comp,
            "WAST": status_code,
        })

    return pd.DataFrame(rows)
