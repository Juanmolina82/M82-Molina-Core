import os, sys, requests, time, random
from concurrent.futures import ThreadPoolExecutor

# Ajuste de PATH para importar desde core/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.data_pipeline import load_market_data, GROUPS_LIVE
from core.risk_model import evaluate_macro_risk, evaluate_mega_risk
from core.investment_matrix import get_allocation

def load_env():
    for p in ['~/M82-Command/.env', '.env', 'M82-Command/.env']:
        p = os.path.expanduser(p)
        if os.path.exists(p):
            with open(p) as f:
                for l in f:
                    l = l.strip()
                    if l and '=' in l and not l.startswith('#'):
                        k, v = l.split('=', 1)
                        os.environ[k.strip()] = v.strip().strip("'").strip('"')
            break

load_env()
TOKEN = os.getenv("M82_TELEGRAM_TOKEN") or os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("M82_CHAT_ID") or os.getenv("CHAT_ID")

FIXED = {
    'aapl': (0.0050, 333.25),
    'jp10': (0.0015, 2.83),
    'jp2': (0.0010, 1.56),
}

sess = requests.Session()
sess.headers.update({'User-Agent': 'Mozilla/5.0'})

def fetch_asset(item):
    k, sym = item
    if k in FIXED: 
        return k, FIXED[k]
    if 'MANUAL' in sym: 
        return k, (None, None)
    for _ in range(3):
        try:
            r = sess.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1m&range=1d", timeout=5).json()
            m = r['chart']['result'][0]['meta']
            price = m.get('regularMarketPrice') or 0.0
            prev = m.get('chartPreviousClose') or 0.0
            if not price or not prev: raise Exception("no data")
            ret = (price - prev) / prev
            if abs(ret) > 0.15: return k, (None, None)
            return k, (ret, price)
        except:
            time.sleep(random.random() * 0.3)
    return k, (None, None)

def run():
    all_t = {}
    for g in GROUPS_LIVE.values(): 
        all_t.update(g)
        
    with ThreadPoolExecutor(max_workers=15) as ex:
        data = dict(ex.map(fetch_asset, all_t.items()))

    # Fallback/Manual Brent
    wti_ret, wti_pr = data.get('wti', (None, None))
    if wti_ret is not None and wti_pr:
        data['brent'] = (wti_ret, 86.00)
    else:
        data['brent'] = (-0.0595, 86.00)

    # RIESGO Y ALOCACIÓN M82 CORE INTEGRADO
    yf_macro = load_market_data(period="1mo")
    macro_risks = evaluate_macro_risk(yf_macro)
    
    # Adaptar data para evaluate_mega_risk
    mega_dict = {sym: {'ret': val[0]} for sym, val in data.items() if val[0] is not None}
    is_shock, shocks = evaluate_mega_risk(mega_dict)
    alloc = get_allocation(macro_risks, is_shock)

    msg = "📺 **BLOOMBERG MARKET DASHBOARD**\n"
    msg += "───────────────────────────────\n\n"
    
    all_valid = []
    sector_avgs = []

    for cat_name, items in GROUPS_LIVE.items():
        cat_rets = []
        msg += f"**{cat_name}**\n"

        for k in items.keys():
            ret, pr = data.get(k, (None, None))
            if ret is None or pr is None: 
                continue
            
            if k in ['jp10', 'jp2']:
                msg += f"🟢 `{k.upper():<7}` {pr:.2f}% | YIELD\n"
                continue
            
            disp = -ret if k == 'vix' else ret
            emoji = "🟢" if disp >= 0 else "🔴"
            arrow = "▲" if disp >= 0 else "▼"
            msg += f"{emoji} `{k.upper():<7}` ${pr:<8.2f} {arrow} {disp*100:+.2f}%\n"
            
            all_valid.append((k, disp, pr))
            cat_rets.append(disp)

        msg += "\n"
        if cat_rets:
            avg = sum(cat_rets) / len(cat_rets)
            sector_avgs.append((cat_name, avg))

    # 1. SECTOR DRIVERS
    sector_avgs = sorted(sector_avgs, key=lambda x: x[1], reverse=True)
    msg += "───────────────────────────────\n"
    msg += "📊 **SECTOR DRIVERS**\n"
    for sec_name, avg in sector_avgs:
        emoji = "🟢" if avg >= 0 else "🔴"
        clean = sec_name.split('-')[0].strip()
        msg += f"{emoji} {clean}: `{avg*100:+.2f}%`\n"

    # 2. TOP & BOTTOM PERFORMERS
    all_valid = sorted(all_valid, key=lambda x: x[1], reverse=True)
    
    msg += "\n🟢 **TOP PERFORMERS**\n"
    for k, ret, pr in all_valid[:5]: 
        msg += f" • `{k.upper():<9}` ${pr:<8.2f} ▲ `{ret*100:+.2f}%`\n"
        
    msg += "\n🔴 **BOTTOM PERFORMERS**\n"
    for k, ret, pr in all_valid[-5:]: 
        msg += f" • `{k.upper():<9}` ${pr:<8.2f} ▼ `{ret*100:+.2f}%`\n"
        
    # 3. ALERTA Y MATRIZ BROOKFIELD INTEGRADA
    msg += "───────────────────────────────\n"
    msg += f"🚨 **ALERT**: {alloc['status']}"

    print(msg)
    if TOKEN and CHAT_ID:
        try:
            r = sess.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=5)
            print("\n[+] Dashboard V8.0 SOVEREIGN enviado con éxito a Telegram.")
        except Exception as e:
            print(f"\n[!] Error enviando a Telegram: {e}")

if __name__ == "__main__": 
    run()
