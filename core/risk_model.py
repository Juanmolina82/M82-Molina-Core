import numpy as np
import pandas as pd

def evaluate_macro_risk(data_yf):
    risks = {}
    for asset, df in data_yf.items():
        if len(df) < 5: continue
        ret = df['returns'].dropna()
        if ret.empty: continue
        last_ret = ret.iloc[-1]
        vol = ret.std()
        z = last_ret / vol if vol != 0 else 0
        if z < -2.5 or last_ret < -0.04:
            regime = "SHOCK EVENT"
        elif vol > 0.02:
            regime = "HIGH VOLATILITY"
        else:
            regime = "STABLE"
        risks[asset] = {"return": last_ret, "vol": vol, "z": z, "regime": regime}
    return risks

def evaluate_mega_risk(mega_data):
    shocks = []
    for sym, info in mega_data.items():
        if info['ret'] <= -0.04:
            shocks.append((sym, info['ret']))
    return len(shocks) > 0, shocks
