import requests, time, os

# Mapeo Institucional de ETFs Proxy para Asset Class, Sector y Region
ASSET_CLASSES = {
    "Alternatives": "QAI", "Multi Asset": "AOA", "Equities": "SPY",
    "Bonds": "AGG", "Volatility": "UVXY", "Preferred Stocks": "PFF",
    "Currency": "UUP", "Crypto": "IBIT", "Commodities": "DBC", "Real Estate": "VNQ"
}

SECTORS = {
    "Energy": "XLE", "Telecom": "XLC", "Technology": "XLK",
    "Utilities": "XLU", "Industrials": "XLI", "Healthcare": "XLV",
    "Consumer Discretionary": "XLY", "Consumer Staples": "XLP",
    "Financials": "XLF", "Materials": "XLB", "Real Estate": "XLRE"
}

REGIONS = {
    "Emerging Europe": "ESR", "Japan": "EWJ", "Developed Europe": "IEUR",
    "Global ex-U.S.": "ACWX", "Developed Markets": "EFA", "Frontier Markets": "FM",
    "North America": "IWB", "Latin America": "ILF", "Middle East": "GULF",
    "China": "MCHI", "Emerging Asia Pacific": "EEM"
}

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

def fetch_group_performance(mapping):
    symbols = list(mapping.values())
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={','.join(symbols)}"
    results = {}
    try:
        r = s.get(url, timeout=5).json()
        data = r.get('quoteResponse', {}).get('result', [])
        for item in data:
            sym = item.get('symbol')
            chg = item.get('regularMarketChangePercent', 0.0)
            # Encontrar el nombre correspondiente
            for name, ticker in mapping.items():
                if ticker == sym:
                    results[name] = chg
                    break
    except Exception as e:
        print(f"Error fetching HeatMap metrics: {e}", flush=True)
    return results

print("🌐 M82 MULTI-DIMENSIONAL HEATMAP ENGINE ONLINE...", flush=True)

while True:
    ac_data = fetch_group_performance(ASSET_CLASSES)
    sec_data = fetch_group_performance(SECTORS)
    reg_data = fetch_group_performance(REGIONS)

    os.system("clear")
    print("===================================================================", flush=True)
    print(f" 🌐 M82 CROSS-MARKET HEAT MAP MATRIX • {time.strftime('%H:%M:%S EST')}", flush=True)
    print("===================================================================", flush=True)

    print("\n📊 1. ASSET CLASS BREAKDOWN (1D Return)", flush=True)
    print("-" * 50, flush=True)
    for k, v in sorted(ac_data.items(), key=lambda x: x[1], reverse=True):
        sign = "+" if v > 0 else ""
        color = "🟩" if v > 0 else ("🔴" if v < 0 else "⚪")
        print(f"{color} {k:<20} | {sign}{v:.2f}%", flush=True)

    print("\n🏢 2. SECTOR PERFORMANCE (1D Return)", flush=True)
    print("-" * 50, flush=True)
    for k, v in sorted(sec_data.items(), key=lambda x: x[1], reverse=True):
        sign = "+" if v > 0 else ""
        color = "🟩" if v > 0 else ("🔴" if v < 0 else "⚪")
        print(f"{color} {k:<22} | {sign}{v:.2f}%", flush=True)

    print("\n🌍 3. REGIONAL FLOWS (1D Return)", flush=True)
    print("-" * 50, flush=True)
    for k, v in sorted(reg_data.items(), key=lambda x: x[1], reverse=True):
        sign = "+" if v > 0 else ""
        color = "🟩" if v > 0 else ("🔴" if v < 0 else "⚪")
        print(f"{color} {k:<22} | {sign}{v:.2f}%", flush=True)

    print("===================================================================", flush=True)
    time.sleep(15)
