import pathlib

p = pathlib.Path("m82_institutional_matrix.py").read_text()

# Reemplazamos la sección de formateo e impresión de futuros por la cuadrícula limpia
old_futures_block = """        # FUTUROS AGRUPADOS POR ASSET CLASS
        header_out.append("────────────────────────────────────────────────────")
        header_out.append("⚡ CONTINUOUS DERIVATIVES & FUTURES (GLOBEX / CME):")
        
        FUTURES_ORDER = {
            "ES_FUT": 1, "NQ_FUT": 2, "DOW_FUT": 3, "RTY_FUT": 4,
            "WTI_FUT": 10, "GASO_FUT": 11, "NATGAS_FUT": 12,
            "GOLD_FUT": 20, "SILVER_FUT": 21, "COPPER_FUT": 22,
            "CORN_FUT": 30, "SOY_FUT": 31, "WHEAT_FUT": 32
        }
        futures_data_sorted = sorted(futures_data, key=lambda x: FUTURES_ORDER.get(x["ticker"], 99))
        
        def fmt_fut(f):
            icon = "🟢" if f["pct"] >= 0 else "🔴"
            return f"{f['ticker']}: {f['price']:.2f} {icon}{f['pct']:+.2f}%"

        eq_futs = [f for f in futures_data_sorted if f["ticker"] in ["ES_FUT","NQ_FUT","DOW_FUT","RTY_FUT"]]
        en_futs = [f for f in futures_data_sorted if f["ticker"] in ["WTI_FUT","GASO_FUT","NATGAS_FUT"]]
        me_futs = [f for f in futures_data_sorted if f["ticker"] in ["GOLD_FUT","SILVER_FUT","COPPER_FUT"]]
        ag_futs = [f for f in futures_data_sorted if f["ticker"] in ["CORN_FUT","SOY_FUT","WHEAT_FUT"]]
        
        if eq_futs: header_out.append(" • EQUITY: " + " │ ".join([fmt_fut(f) for f in eq_futs]))
        if en_futs: header_out.append(" • ENERGY: " + " │ ".join([fmt_fut(f) for f in en_futs]))
        if me_futs: header_out.append(" • METALS: " + " │ ".join([fmt_fut(f) for f in me_futs]))
        if ag_futs: header_out.append(" • AGS:    " + " │ ".join([fmt_fut(f) for f in ag_futs]))"""

new_futures_block = """        # FUTUROS AGRUPADOS POR ASSET CLASS (CUADRÍCULA LIMPIA v4.4.1)
        header_out.append("────────────────────────────────────────────────────")
        header_out.append("⚡ CONTINUOUS DERIVATIVES & FUTURES (GLOBEX / CME):")
        
        NICKNAMES = {
            "ES_FUT": "ES", "NQ_FUT": "NQ", "DOW_FUT": "YM", "RTY_FUT": "RTY",
            "WTI_FUT": "WTI", "NATGAS_FUT": "NG", "GASO_FUT": "RB",
            "GOLD_FUT": "GOLD", "SILVER_FUT": "SIL", "COPPER_FUT": "HG",
            "CORN_FUT": "CORN", "SOY_FUT": "SOY", "WHEAT_FUT": "WHT"
        }
        
        def fmt_micro(f):
            name = NICKNAMES.get(f["ticker"], f["ticker"][:4])
            icon = "🟢" if f["pct"] >= 0 else "🔴"
            return f"{name:<4} {f['price']:>7.2f} {icon}{f['pct']:>+5.2f}%"

        f_map = {f["ticker"]: f for f in futures_data}
        
        eq_list = [f_map[k] for k in ["ES_FUT","NQ_FUT","DOW_FUT","RTY_FUT"] if k in f_map]
        en_list = [f_map[k] for k in ["WTI_FUT","NATGAS_FUT","GASO_FUT"] if k in f_map]
        me_list = [f_map[k] for k in ["GOLD_FUT","SILVER_FUT","COPPER_FUT"] if k in f_map]
        ag_list = [f_map[k] for k in ["CORN_FUT","SOY_FUT","WHEAT_FUT"] if k in f_map]
        
        if eq_list: header_out.append(" 📈 EQTY │ " + " │ ".join([fmt_micro(f) for f in eq_list]))
        if en_list: header_out.append(" 🛢️ ENRG │ " + " │ ".join([fmt_micro(f) for f in en_list]))
        if me_list: header_out.append(" 🪙 METL │ " + " │ ".join([fmt_micro(f) for f in me_list]))
        if ag_list: header_out.append(" 🌾 AGRI │ " + " │ ".join([fmt_micro(f) for f in ag_list]))"""

if old_futures_block in p:
    p = p.replace(old_futures_block, new_futures_block)
    pathlib.Path("m82_institutional_matrix.py").write_text(p)
    print("FUTURES LAYOUT REFACTORED TO GRID v4.4.1")
else:
    print("WARNING: Exact match not found, checking alternative replacement...")
