def get_allocation(risks, mega_shock):
    if mega_shock or any(r.get('regime') == 'SHOCK EVENT' for r in risks.values()):
        return {"HEDGE": 0.25, "EQUITY": 0.50, "BONDS": 0.15, "CASH": 0.10, "status": "SHOCK -> HEDGE 25%"}
    return {"HEDGE": 0.05, "EQUITY": 0.70, "BONDS": 0.15, "CASH": 0.10, "status": "NORMAL - RISK ON"}
