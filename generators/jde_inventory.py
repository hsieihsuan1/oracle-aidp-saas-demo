"""Adapted synthetic generator. Local-only; no cloud writes."""
import random

rng = random.Random(42)
from datetime import datetime

import pandas as pd

ITEMS = [
    (10001, "VALV-CTRL-1", "Válvula de Controle 1\"", "UN", "IM", "S"),
    (10002, "VALV-CTRL-2", "Válvula de Controle 2\"", "UN", "IM", "S"),
    (10003, "BOMBA-CENT-A", "Bomba Centrífuga Modelo A", "UN", "MM", "S"),
    (10004, "BOMBA-CENT-B", "Bomba Centrífuga Modelo B", "UN", "MM", "S"),
    (10005, "FILTRO-100", "Filtro Industrial 100 mesh", "UN", "IM", "S"),
    (10006, "FILTRO-200", "Filtro Industrial 200 mesh", "UN", "IM", "S"),
    (10007, "MOTOR-5CV", "Motor Elétrico 5CV 220V", "UN", "MM", "S"),
    (10008, "MOTOR-10CV", "Motor Elétrico 10CV 220V", "UN", "MM", "S"),
    (10009, "COMP-AR-50", "Compressor de Ar 50L", "UN", "MM", "S"),
    (10010, "COMP-AR-100", "Compressor de Ar 100L", "UN", "MM", "S"),
    (10011, "PARAFUSO-M8", "Parafuso M8x30 Inox", "PC", "CM", "S"),
    (10012, "PARAFUSO-M10", "Parafuso M10x40 Inox", "PC", "CM", "S"),
    (10013, "PORCA-M8", "Porca M8 Inox", "PC", "CM", "S"),
    (10014, "ARRUELA-M8", "Arruela M8 Inox", "PC", "CM", "S"),
    (10015, "OLEO-ISO68", "Óleo Lubrificante ISO 68 - 20L", "GL", "OM", "S"),
    (10016, "OLEO-ISO150", "Óleo Lubrificante ISO 150 - 20L", "GL", "OM", "S"),
    (10017, "GRAXA-LIT2", "Graxa de Lítio EP2 - 1kg", "KG", "OM", "S"),
    (10018, "CORREIA-A50", "Correia Tipo A - 50\"", "UN", "CM", "S"),
    (10019, "CORREIA-B60", "Correia Tipo B - 60\"", "UN", "CM", "S"),
    (10020, "ROLAMENTO-6205", "Rolamento 6205-2RS", "UN", "CM", "S"),
    (10021, "ROLAMENTO-6305", "Rolamento 6305-2RS", "UN", "CM", "S"),
    (10022, "VEDACAO-OR10", "Vedação O-Ring 10mm", "PC", "CM", "S"),
    (10023, "VEDACAO-OR20", "Vedação O-Ring 20mm", "PC", "CM", "S"),
    (10024, "TUBO-ACO-1", "Tubo Aço Carbono 1\" x 6m", "MT", "IM", "S"),
    (10025, "TUBO-ACO-2", "Tubo Aço Carbono 2\" x 6m", "MT", "IM", "S"),
    (10026, "CABO-ELETRICO-4", "Cabo Elétrico 4mm² - rolo 100m", "RL", "EM", "S"),
    (10027, "CABO-ELETRICO-6", "Cabo Elétrico 6mm² - rolo 100m", "RL", "EM", "S"),
    (10028, "DISJUNTOR-25A", "Disjuntor Bipolar 25A", "UN", "EM", "S"),
    (10029, "DISJUNTOR-40A", "Disjuntor Bipolar 40A", "UN", "EM", "S"),
    (10030, "SENSOR-TEMP", "Sensor de Temperatura PT100", "UN", "IM", "S"),
    (10031, "SENSOR-PRESS", "Sensor de Pressão 0-10 bar", "UN", "IM", "S"),
    (10032, "CLP-S7-1200", "CLP Siemens S7-1200 CPU 1212C", "UN", "EM", "S"),
    (10033, "IHM-KTP700", "IHM Siemens KTP700 Basic", "UN", "EM", "S"),
    (10034, "INVERSOR-5CV", "Inversor de Frequência 5CV 220V", "UN", "EM", "S"),
    (10035, "INVERSOR-10CV", "Inversor de Frequência 10CV 220V", "UN", "EM", "S"),
    (10036, "RELE-TERMICO", "Relé Térmico 9-13A", "UN", "EM", "S"),
    (10037, "CONTATOR-25A", "Contator Tripolar 25A 220V", "UN", "EM", "S"),
    (10038, "CHAVE-BOIA", "Chave Boia Nível Líquido", "UN", "IM", "S"),
    (10039, "VALV-SOL-24V", "Válvula Solenóide 24VDC 1/2\"", "UN", "IM", "S"),
    (10040, "TROCADOR-CALOR", "Trocador de Calor Casco-Tubo", "UN", "MM", "S"),
    (10041, "RESINA-EPOXI", "Resina Epóxi Bicomponente - 5kg", "KG", "OM", "N"),
    (10042, "TINTA-ANTICORR", "Tinta Anticorrosiva - 3,6L", "GL", "OM", "N"),
    (10043, "DISCO-CORTE-9", "Disco de Corte 9\" x 2mm", "PC", "CM", "N"),
    (10044, "DISCO-DESBASTE", "Disco de Desbaste 9\" x 6mm", "PC", "CM", "N"),
    (10045, "ELETRODO-6013", "Eletrodo 6013 3,25mm - caixa 5kg", "CX", "OM", "N"),
    (10046, "EPI-OCULOS", "Óculos de Proteção CA 23741", "UN", "GM", "N"),
    (10047, "EPI-LUVA-VAQUETA", "Luva Vaqueta CA 5", "PAR", "GM", "N"),
    (10048, "EPI-CAPACETE", "Capacete de Segurança ABA FRONTAL", "UN", "GM", "N"),
    (10049, "FITA-ISOLANTE", "Fita Isolante Autofusão 19mmx10m", "RL", "EM", "N"),
    (10050, "SILICONE-ALTA", "Silicone Alta Temperatura 150ml", "PC", "OM", "N"),
]

BRANCHES = ["SP01", "SP02", "RS01", "MG01", "RJ01"]

SAFETY_STOCK = {
    "S": lambda: rng.randint(5, 50),
    "N": lambda: rng.randint(1, 10),
}

REORDER_POINT = {
    "S": lambda: rng.randint(10, 100),
    "N": lambda: rng.randint(2, 20),
}


def generate_f4101() -> pd.DataFrame:
    rows = []
    for itm, litm, dsc1, uom, glpt, stkt in ITEMS:
        def trunc_bytes(s, n):
            b = s.encode("utf-8")[:n]
            return b.decode("utf-8", errors="ignore")

        rows.append({
            "IMITM": itm,
            "IMLITM": trunc_bytes(litm, 25),
            "IMAITM": trunc_bytes(litm, 10),
            "IMDSC1": trunc_bytes(dsc1, 30),
            "IMDSC2": "",
            "IMSRTX": trunc_bytes(litm.replace("-", " "), 10),
            "IMUOM": uom[:2],
            "IMGLPT": glpt[:4],
            "IMSTKT": stkt[:1],
        })
    return pd.DataFrame(rows)


def generate_f41021() -> pd.DataFrame:
    rows = []
    for itm, litm, dsc1, uom, glpt, stkt in ITEMS:
        for branch in rng.sample(BRANCHES, k=rng.randint(2, 5)):
            qoh = round(rng.uniform(0, 500) if stkt == "S" else rng.uniform(0, 50), 2)
            safety = SAFETY_STOCK[stkt]()
            reorder = REORDER_POINT[stkt]()
            rows.append({
                "IBITM": itm,
                "IBMCU": branch,
                "IBLOTN": "",
                "IBLOC": f"{rng.randint(1,9)}B{rng.randint(1,9):02d}",
                "IBPQOH": qoh,
                "IBUOM": uom[:2],
                "IBSAFETY": safety,
                "IBREORDER": reorder,
            })
    return pd.DataFrame(rows)
