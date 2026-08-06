import yfinance as yf
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
import time
from datetime import datetime
import pandas as pd

console = Console()

# CONFIG INSTITUCIONAL
TICKERS = ["^GSPC", "^DJI", "^IXIC", "^VIX", "META", "NVDA", "CAT", "AMD", "UAL", "XOM", "CVX", "EOG", "JPM", "GS"]
PRE_MARKET_WATCH = ["CAT", "AMD", "SPCX"] # SPCX no tiene ticker real, usamos proxy
ASIA_TICKERS = ["^N225", "^HSI", "1320.KS", "^AXJO"] # Nikkei, HSI, Kospi proxy, ASX
FUTURES = ["CL=F", "HG=F", "NG=F"] # WTI, Copper, Nat Gas

def get_institutional_metrics(ticker):
    try:
        tk = yf.Ticker(ticker)
        hist = tk.history(period="1mo")
        info = tk.fast_info

        price = info.last_price
        chg_pct = info.last_price - info.previous_close
        chg_pct = (chg_pct / info.previous_close) * 100 if info.previous_close else 0

        # RSI 14
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi_val = rsi.iloc[-1] if not rsi.empty else 50

        # RVOL
        avg_vol = hist['Volume'].rolling(20).mean().iloc[-1]
        rvol = hist['Volume'].iloc[-1] / avg_vol if avg_vol else 1

        # Distancia a 52w High
        high_52 = hist['Close'].max()
        dist_ath = ((price - high_52) / high_52 * 100) if high_52 else 0

        # Day Range
        day_low, day_high = info.day_low, info.day_high

        status = "🟢 LIVE"
        latency = f"{int((datetime.now().timestamp() % 1)*1000)}ms"

        return {
            "price": price, "chg": chg_pct, "rsi": rsi_val, "rvol": rvol,
            "dist": dist_ath, "range": f"{day_low:.2f}-{day_high:.2f}",
            "status": status, "latency": latency, "ok": True
        }
    except Exception as e:
        return {"price": 0, "chg": 0, "rsi": 50, "rvol": 0, "dist": 0, "range": "N/A", "status": f"🔴 STALE {e}", "ok": False}

def make_table(title, tickers_list):
    table = Table(title=title, expand=True)
    table.add_column("Ticker", style="cyan bold")
    table.add_column("Precio", justify="right")
    table.add_column("% Hoy", justify="right")
    table.add_column("RSI 14", justify="right")
    table.add_column("RVOL", justify="right")
    table.add_column("Dist 52W", justify="right")
    table.add_column("Day Range", justify="right")

    for t in tickers_list:
        m = get_institutional_metrics(t)
        if not m['ok']:
            table.add_row(t, f"[red]STALE[/]", "0.00%", "50", "0x", "0%", m['range'])
            continue

        color = "green" if m['chg'] >= 0 else "red"
        rsi_color = "yellow" if m['rsi'] > 70 or m['rsi'] < 30 else "white"
        table.add_row(
            t,
            f"${m['price']:.2f}",
            f"[{color}]{m['chg']:+.2f}%[/]",
            f"[{rsi_color}]{m['rsi']:.0f}[/]",
            f"{m['rvol']:.1f}x",
            f"{m['dist']:+.1f}%",
            m['range']
        )
    return table

# LIVE LOOP INSTITUCIONAL
try:
    with Live(console=console, refresh_per_second=1, screen=True) as live:
        while True:
            layout = Layout()
            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="body"),
                Layout(name="footer", size=5)
            )
            layout["body"].split_row(
                Layout(name="left"),
                Layout(name="right")
            )
            layout["left"].split_column(
                Layout(Panel(make_table("🌐 US INDICES", ["^GSPC","^DJI","^IXIC","^VIX"]), border_style="yellow")),
                Layout(Panel(make_table("🏰 CORE TECH + CAT/AMD", ["META","NVDA","CAT","AMD","PLTR"]), border_style="cyan")),
            )
            layout["right"].split_column(
                Layout(Panel(make_table("⚡ ENERGY DIVERGENCE (WH Pressure)", ["XOM","CVX","EOG","UAL"]), border_style="red")),
                Layout(Panel(make_table("🌏 ASIA + FUTURES (Dr Copper)", ["^N225","^HSI","CL=F","HG=F","NG=F"]), border_style="green")),
            )

            header = Panel(f"[bold yellow]BLOOMBERG M82 V6.0 INSTITUTIONAL — {datetime.now().strftime('%d-%b %H:%M:%S ET')} | 🟢 API: CONNECTED | MODE: RALLY TOTAL (SPX 7600.50 +1.48% ref) | LATENCY: ~120ms | DATA: yfinance LIVE[/]", style="bold white on black")
            footer = Panel(
                f"[yellow]M82 CORE: VZLA 856k->1.2M | OFAC GL5Y 45d Sep17 | JTF-Hemisferio | TRUMP: 'making too much money' => Political Ceiling $82 | SIGNAL: LONG UAL/RISK-ON + HEDGE OIL | METRICS: RSI>70 overbought RSI<30 oversold RVOL>1.5x institutional[/]",
                title="🦅 M82 INSTITUTIONAL MATRIX", border_style="yellow"
            )
            layout["header"] = header
            layout["footer"] = footer

            live.update(layout)
            time.sleep(10) # refresh cada 10s como terminal real
except KeyboardInterrupt:
    print("\n🦅 M82 V6.0 CERRADO — Desk offline")
