"""Adapted synthetic generator. Local-only; no cloud writes."""
import random

rng = random.Random(42)
from datetime import date, timedelta

import pandas as pd


LEDGERS = ["Ledger_BR_Principal", "Ledger_BR_Consolidado"]
PERIODS = ["Jan-26", "Feb-26", "Mar-26", "Apr-26"]
GL_ACCOUNTS = [
    ("1.1.01", "Caixa e Equivalentes"),
    ("1.1.02", "Contas a Receber"),
    ("1.2.01", "Estoque de Matéria-Prima"),
    ("1.2.02", "Estoque de Produtos Acabados"),
    ("2.1.01", "Fornecedores Nacionais"),
    ("2.1.02", "Fornecedores Internacionais"),
    ("3.1.01", "Receita de Vendas"),
    ("4.1.01", "Custo dos Produtos Vendidos"),
    ("4.2.01", "Despesas Operacionais"),
    ("4.2.02", "Despesas Administrativas"),
]

SUPPLIERS = [
    ("500", "Synthetic Supplier 1"),
    ("501", "Synthetic Supplier 2"),
    ("502", "Synthetic Supplier 3"),
    ("503", "Synthetic Supplier 4"),
    ("504", "Synthetic Supplier 5"),
    ("505", "Synthetic Supplier 6"),
    ("506", "Synthetic Supplier 7"),
]

PAYMENT_TERMS = ["NET30", "NET45", "NET60", "2/10NET30"]


def generate_gl_journals(n: int = 60) -> pd.DataFrame:
    rows = []
    base = date(2026, 1, 2)
    for i in range(n):
        post_date = base + timedelta(days=rng.randint(0, 115))
        period = PERIODS[min((post_date.month - 1), len(PERIODS) - 1)]
        acc_code, acc_desc = rng.choice(GL_ACCOUNTS)
        amount = round(rng.uniform(1000, 500000), 2)
        is_debit = rng.random() > 0.5
        rows.append({
            "JOURNAL_ID": 9000 + i + 1,
            "LEDGER_NAME": rng.choice(LEDGERS),
            "PERIOD_NAME": period,
            "ACCOUNT_CODE": acc_code,
            "ACCOUNT_DESC": acc_desc,
            "DEBIT_AMOUNT": amount if is_debit else 0,
            "CREDIT_AMOUNT": 0 if is_debit else amount,
            "CURRENCY_CODE": "BRL",
            "STATUS": rng.choice(["POSTED", "POSTED", "POSTED", "DRAFT"]),
            "POSTED_DATE": post_date.isoformat(),
            "CREATED_BY": rng.choice(["synthetic-user-01", "synthetic-user-02", "synthetic-user-03"]),
        })
    return pd.DataFrame(rows)


def generate_ap_invoices(n: int = 35) -> pd.DataFrame:
    rows = []
    base = date(2025, 11, 1)
    today = date(2026, 4, 26)

    for i in range(n):
        supp_num, supp_name = rng.choice(SUPPLIERS)
        inv_date = base + timedelta(days=rng.randint(0, 175))
        terms = rng.choice(PAYMENT_TERMS)
        days_net = int(''.join(filter(str.isdigit, terms.split("NET")[-1])) or 30)
        due_date = inv_date + timedelta(days=days_net)

        amount = round(rng.uniform(500, 150000), 2)
        paid = 0.0
        if due_date < today:
            paid = amount if rng.random() > 0.25 else round(amount * rng.uniform(0, 0.8), 2)
        elif rng.random() > 0.7:
            paid = round(amount * rng.uniform(0.1, 0.5), 2)

        remaining = round(amount - paid, 2)
        if remaining <= 0:
            status = "PAID"
        elif due_date < today and remaining > 0:
            status = "OVERDUE"
        elif paid > 0:
            status = "PARTIAL"
        else:
            status = "UNPAID"

        rows.append({
            "INVOICE_ID": 6000 + i + 1,
            "SUPPLIER_NAME": supp_name,
            "SUPPLIER_NUMBER": supp_num,
            "INVOICE_NUMBER": f"NF-{rng.randint(10000, 99999)}",
            "INVOICE_DATE": inv_date.isoformat(),
            "DUE_DATE": due_date.isoformat(),
            "AMOUNT": amount,
            "AMOUNT_PAID": paid,
            "AMOUNT_REMAINING": remaining,
            "CURRENCY_CODE": "BRL",
            "STATUS": status,
            "PAYMENT_TERMS": terms,
        })
    return pd.DataFrame(rows)
