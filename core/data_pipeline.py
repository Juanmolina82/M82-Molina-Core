import yfinance as yf
import pandas as pd
import requests, time, random
from concurrent.futures import ThreadPoolExecutor

TICKERS_CORE = {'brent':'BZ=F','wti':'CL=F','us10y':'^TNX','btc':'BTC-USD','spx':'^GSPC'}

GROUPS_LIVE = {
    "🌐 INDICES US": {'spx':'^GSPC','dow':'^DJI','nasdaq':'^IXIC','russell':'^RUT','es':'ES=F','nq':'NQ=F','ym':'YM=F','rty':'RTY=F','vix':'^VIX'},
    "📈 ETFs US": {'spy':'SPY','qqq':'QQQ','dia':'DIA','iwm':'IWM'},
    "💰 FINANCIALS - DRIVING UPSIDE": {'jpm':'JPM','bac':'BAC','gs':'GS','ms':'MS','c':'C'},
    "⚡ ENERGY - DRIVING UPSIDE": {'xom':'XOM','cvx':'CVX','slb':'SLB','eog':'EOG'},
    "✈️ AIRLINES & LEISURE": {'ual':'UAL','iag':'IAG.L','tui':'TUI.L','rya':'RYA.L','lha':'LHA.DE'},
    "🏰 EUROPE CORE 6": {'novo':'NOVO-B.CO','lvmh':'MC.PA','rhein':'RHM.DE','asml':'ASML.AS','schneider':'SU.PA','nestle':'NESN.SW'},
    "🌍 GLOBAL MACRO & BONOS": {'dxy':'DX-Y.NYB','ust10y':'^TNX','jp10':'JP10YT=X','jp2':'JP2YT=X'},
    "🛢️ COMMODITIES": {'wti':'CL=F','brent':'BRENT_MANUAL','gold':'GC=F','silver':'SI=F','btc':'BTC-USD'},
    "🏦 CORE EQUITY & TECH": {'f':'F','meta':'META','nvda':'NVDA','aapl':'AAPL_MANUAL','pltr':'PLTR','shop':'SHOP','app':'APP','net':'NET'}
}

sess = requests.Session()
sess.headers.update({'User-Agent':'Mozilla/5.0'})

def fetch_yahoo(sym):
    for _ in range(3):
        try:
            r = sess.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1m&range=1d", timeout=5).json()
            m = r['chart']['result'][0]['meta']
            price = m.get('regularMarketPrice') or 0.0
            prev = m.get('chartPreviousClose') or 0.0
            if not price or not prev: raise Exception("no data")
            ret = (price - prev) / prev
            if abs(ret) > 0.20: return None
            return {'symbol': sym, 'price': price, 'ret': ret, 'prev': prev}
        except:
            time.sleep(random.random() * 0.3)
    return None

def load_market_data_mega():
    all_syms = []
    for g in GROUPS_LIVE.values():
        all_syms.extend(g.values())
    all_syms = [s for s in list(set(all_syms)) if 'MANUAL' not in s]
    
    with ThreadPoolExecutor(max_workers=15) as ex:
        results = list(ex.map(fetch_yahoo, all_syms))
    
    data = {r['symbol']: r for r in results if r}
    print(f"[+] M82 MEGA LIVE: {len(data)}/{len(all_syms)} activos procesados.")
    return data

def load_market_data(period="1mo"):
    data = {}
    for name, ticker in TICKERS_CORE.items():
        try:
            df = yf.download(ticker, period=period, progress=False)
            if df.empty: raise Exception("empty")
            close_col = 'Close' if 'Close' in df.columns else df.columns[0]
            df = df.rename(columns={close_col: 'close'}).reset_index()
            df['returns'] = df['close'].pct_change()
            data[name] = df
        except Exception as e:
            pass
    return data
