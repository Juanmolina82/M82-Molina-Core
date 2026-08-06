# M82 MACRO EVENTS V4.2 — TRUMP VS BIG OIL

TRUMP_OIL_STATEMENT = {
    "date": "2026-08-03",
    "source": "White House",
    "quote": "making too much money based on the shortage",
    "target": "Big Oil crack spread + retail gasoline margins",
    "second_leg": "Fin del conflicto Iran = desplome crudo",
    "m82_tag": "POLITICAL CEILING ON OIL RISK PREMIUM"
}

ENERGY_IMPACT_MAP = {
    "XOM": {"change": -0.24, "read": "Presion regulatoria/discurso politico - HOLD"},
    "CVX": {"change": -1.85, "read": "BOTTOM sectorial - No long hasta estabilice retorica"},
    "EOG": {"change": -2.02, "read": "Descuento margenes exploracion - BOTTOM"},
    "SLB": {"change": -0.56, "read": "Service lag"},
    "UAL": {"change": +5.82, "read": "TOP PERFORMER - Jet fuel relief directo"},
    "LHA": {"change": +2.24, "read": "Beneficiario EU"},
    "IAG": {"change": +0.37, "read": "Beneficiario EU lag"},
}

M82_ACTION_MATRIX = """
[M82 MACRO UPDATE: ENERGY REGULATORY RISK HIGH]
├── BUCKET OIL: Maintain "Hedge Oil Active" - Political ceiling $80-82
├── AIRLINES & CONSUMER: LONG UAL +5.82% / LHA +2.24% - Direct margin relief
├── VZLA SUPPLY: Trump needs heavy/medium volume 856k->1.2M bpd to force price down
│   └── GL5Y 45d Sep17 = Perfect timing to replace Iran premium with VZLA barrels
└── SIGNAL: No longs XOM/CVX until Iran headlines + WH rhetoric stabilize
"""

def get_energy_signal():
    return "HEDGE OIL ACTIVE | LONG AIRLINES | VZLA VOLUME ACCELERATOR"
