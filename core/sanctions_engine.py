# M82 SANCTIONS & SPECIAL EVENTS MODULE - V3 CLEAN

SANCTIONS_EVENTS = {
    "OFAC_GL_5Y": {
        "date_issued": "2026-08-03",
        "effective_trading": "2026-09-17",
        "countdown_days": 45,
        "asset": "PDVSA 2020 8.5%",
        "action": "AUTHORIZED - CITGO window",
        "m82_signal": "VE RISK-ON"
    },
    "JTF_HEMISPHERE": {
        "date": "2026-08-04",
        "old_name": "JTF-Southern Spear / Lanza del Sur",
        "new_name": "JTF-Hemisferio Occidental",
        "commander": "Gen. Francis Donovan SOUTHCOM",
        "doctrine": "Caribe tactical -> Hemispheric strategic",
        "impact": "Venezuela 3-phase plan becomes hemispheric pillar"
    },
    "ELSALV_CURVE": {
        "status": "Bull compression - Proof of concept",
        "yield_27s": "5.67% from >20% distressed",
        "price_54s": "$114.82 +0.99%",
        "signal": "VZLA blueprint post-GL5Y"
    }
}

ALERTS_M82_RULES = {
    "BLOCK_BUY_ENERGY": "ALERTAR - Validar Energy Resilience con WTI",
    "FALL_2%_LEISURE": "Solo si WTI -4%+ = tailwind airlines UAL",
    "RISE_2%_BIOTECH": "RISK-ON extendido",
    "DOW_ATH": "53,178 confirmed - HOLD Tech",
    "SPX_7600": "Watch 7,610 breakout with CAT + AMD"
}

def get_all_events():
    return SANCTIONS_EVENTS

def get_event_status(key="OFAC_GL_5Y"):
    return SANCTIONS_EVENTS.get(key, {})
