import pathlib
p = pathlib.Path("m82_institutional_matrix.py").read_text()

p = p.replace('"IAUX"', '"IAUX", "SOUN", "AXON", "SNDK"')

old = "# SECCIÓN WHALE SPIKES DETECTADOS"
new = """# POST-MARKET EARNINGS ALPHA MODULE - v4.4 Audit Extension
EARNINGS_MAP = {"SOUN": {"beat": 84.85, "ah": 14.45}, "AXON": {"beat": 1.96, "ah": 3.01}, "SNDK": {"beat": 12.26, "ah": -3.94}}
earnings_alpha = []
for r in valid_results:
    if r["ticker"] in EARNINGS_MAP and r.get("ext_type") in ("AH","PRE"):
        info = EARNINGS_MAP[r["ticker"]]
        earnings_alpha.append(f"{'🟢' if info['ah']>0 else '🔴'} {r['ticker']} {info['ah']:+.2f}% AH (Beat {info['beat']:.2f}%) - EXT {r['ext_pct']:+.1f}%")

# SECCIÓN WHALE SPIKES DETECTADOS"""
p = p.replace(old, new)

p = p.replace(
    'if whale_spikes:',
    '''if earnings_alpha:
            header_out.append("────────────────────────────────────────────────────")
            header_out.append("📊 POST-MARKET EARNINGS ALPHA (M82 Audit):")
            for ea in earnings_alpha[:3]:
                header_out.append(f"• {ea}")

        if whale_spikes:'''
)

pathlib.Path("m82_institutional_matrix.py").write_text(p)
print("PATCH AUDIT v4.4 APPLIED SUCCESSFULLY")
