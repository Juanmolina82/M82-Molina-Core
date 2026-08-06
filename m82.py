from datetime import datetime
Y="\033[93m"; G="\033[92m"; R="\033[91m"; W="\033[97m"; C="\033[96m"; B="\033[1m"; D="\033[90m"; X="\033[0m"
def row(t, name, price, chg, note=""):
    col = G if chg >= 0 else R
    syn = "▲" if chg >= 0 else "▼"
    return f"{C}{t:<7}{W} {name:<12} {col}{price:>11} {syn} {abs(chg):>5.2f}%{X} {D}{note}{X}"

print(f"{Y}{B}📺 BLOOMBERG M82 V6.3 HYPERSCALER CAPEX — {datetime.now().strftime('%d-%b %H:%M ET')} | CITADEL GRADE{X}")
print(f"{D}──────────────────────────────────────────────────────────────────────────────{X}")

print(f"\n{C}{B}🚀 1. FUNDAMENTO MACRO: HYPERSCALER CAPEX 2026E (Moomoo/Bloomberg){X}")
print(f"{D}------------------------------------------------------------------------------{X}")
print(f"{Y}   • $745B Combined CapEx 2026E -> Monetización confirmada en Cloud Q2{X}")
print(f"{W}   • AMZN  $220B CapEx 2026E | AWS Q2 +37% YoY ($42.2B){X}")
print(f"{W}   • GOOGL $205B CapEx 2026E | GCP Q2 +82% YoY ($24.8B) [EXPLOSIVO]{X}")
print(f"{W}   • MSFT  $175B CapEx 2026E | Azure Q2 +43% YoY ($31.1B){X}")
print(f"{W}   • META  $145B CapEx 2026E | Justifica META +6.02% RTH{X}")
print(f"{G}   👉 Conclusión: CapEx NO es burbuja, es Revenue. Valida NVDA/SNDK pricing power.{X}")

print(f"\n{C}{B}💾 2. MEMORY TRADE: SNDK — LINK DIRECTO A CAPEX{X}")
print(f"{D}------------------------------------------------------------------------------{X}")
print(row("SNDK", "Sandisk Corp", "$1,288.32", 6.03, "RTH TOP +6.03% | AH -0.02% (KV-cache tier)"))
print(row("SNXX", "2x Long SNDK", "$10.47", 11.67, "2x ETF Long"))
print(row("NVDA", "NVIDIA Corp", "$206.64", 2.93, "GPU Compute beneficiary"))
print(row("MU", "Micron Tech", "$145.20", 2.10, "HBM Peer"))
print(f"{D}   Tesis: Hyperscaler gasta $745B en infra -> necesita Enterprise SSD para KV-cache.{X}")
print(f"{D}   SNDK ASP +41.3% vs BIT +14.5% = Pricing power por CapEx.{X}")

print(f"\n{C}{B}🎯 OPTIONS GAMMA MAP (SNDK){X}")
print(f"{W}   Last: $1,288 | Flip: $1,313.80 | Put: $1,370 | Call Wall: $1,400 | BELOW FLIP = NEG GAMMA{X}")
print(f"{R}   Dealers short gamma = Gap amplificado Aug 5 AMC{X}")

print(f"\n{C}{B}⏰ PRE-MARKET 04-AUG / POST-MARKET 03-AUG{X}")
print(f"{D}------------------------------------------------------------------------------{X}")
print(row("CAT", "Caterpillar", "$425.10", 1.85, "Pre-mkt est."))
print(row("AMD", "AMD Inc.", "$182.75", 3.45, "Pre-mkt continuation"))
print(row("SNDK", "Sandisk Corp", "$1,288.32", 0.02, "Pre-mkt flat"))
print(row("SPX", "S&P 500", "$7,600.50", 1.48, "RTH CLOSE - 9pts to ATH"))
print(row("DOW", "DOW JONES", "$53,178.41", 1.32, "RTH ATH CONFIRMED"))

print(f"\n{C}{B}🌐 INDICES US{X}")
print(f"{D}------------------------------------------------------------------------------{X}")
print(row("SPX", "S&P 500", "$7,600.50", 1.48, "9pts to ATH"))
print(row("DOW", "DOW JONES", "$53,178.41", 1.32, "ATH"))
print(row("NASDAQ", "NASDAQ", "$25,913.90", 2.13, "AI LEADER"))
print(row("VIX", "VIX Index", "$15.86", 0.81, "Complacency"))

print(f"\n{C}{B}📈 ETFs US{X}")
print(row("SPY", "SPDR S&P500", "$757.67", 1.42, ""))
print(row("QQQ", "NASDAQ 100", "$700.07", 1.76, ""))
print(row("IWM", "Russell 2K", "$296.22", 1.72, ""))

print(f"\n{C}{B}⚡ ENERGY HEDGE ACTIVE{X}")
print(row("XOM", "Exxon Mobil", "$155.06", -0.24, "WH Pressure"))
print(row("CVX", "Chevron", "$193.18", -1.85, "BOTTOM"))
print(row("EOG", "EOG Resources", "$145.68", -2.02, "BOTTOM"))

print(f"\n{C}{B}✈️ AIRLINES & LEISURE +2.81% TOP{X}")
print(row("UAL", "United Air", "$128.39", 5.82, "Fuel tailwind TOP"))
print(row("LHA", "Lufthansa", "$9.24", 2.24, ""))
print(row("IAG", "IAG Group", "$433.50", 0.37, ""))

print(f"\n{C}{B}🏦 CORE TECH{X}")
print(row("META", "Meta", "$590.24", 6.02, "TOP PERFORMER"))
print(row("NVDA", "NVIDIA", "$206.64", 2.93, ""))
print(row("AAPL", "Apple", "$333.25", 0.50, ""))
print(row("PLTR", "Palantir", "$125.65", 2.10, ""))

print(f"\n{D}──────────────────────────────────────────────────────────────────────────────{X}")
print(f"{G}{B}✅ STATUS: NORMAL | RALLY CONFIRMED | SNDK EARNINGS Aug5 AMC = MAIN EVENT{X}")
print(f"{Y}M82 CORE: VZLA 856k->1.2M GL5Y 45d Sep17 | JTF Hemisferio | $745B CapEx -> Cloud +37%/+43%/+82%{X}")
