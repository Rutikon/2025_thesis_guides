import requests, datetime

secids = [
    'SU26245RMFS9', 'SU26244RMFS2', 'SU26243RMFS4', 'SU26242RMFS6', 'SU26241RMFS8',
    'SU26240RMFS0', 'SU26239RMFS2', 'SU26238RMFS4', 'SU26237RMFS6', 'SU26236RMFS8',
    'SU26235RMFS0', 'SU26233RMFS5', 'SU26232RMFS7', 'SU26230RMFS1', 'SU26229RMFS3',
    'SU26228RMFS5', 'SU26226RMFS9', 'SU26225RMFS1', 'SU26224RMFS4', 'SU26221RMFS0',
    'SU26219RMFS4', 'SU26218RMFS6', 'SU26212RMFS9', 'SU26207RMFS9'
]

def fetch_row(secid, day, board):
    url = (f"https://iss.moex.com/iss/history/engines/stock/markets/bonds/"
           f"boards/{board}/securities/{secid}.json"
           f"?from={day}&till={day}&iss.meta=off")
    js = requests.get(url, timeout=10).json()
    rows = js.get("history", {}).get("data", [])
    return (rows[0], js["history"]["columns"]) if rows else (None, None)

def latest_ytm(secid, lookback=5):
    boards = ["TQOB", "TQOD"]
    for off in range(lookback):
        dstr = (datetime.date.today() - datetime.timedelta(days=off)).strftime("%Y-%m-%d")
        for bd in boards:
            row, cols = fetch_row(secid, dstr, bd)
            if row:
                for fld in ("YIELDCLOSE", "YIELD", "YIELDLASTCOUPON"):
                    if fld in cols and row[cols.index(fld)] is not None:
                        return float(row[cols.index(fld)])
    return None

def maturity_date(secid):
    js = requests.get(f"https://iss.moex.com/iss/securities/{secid}.json?iss.meta=off",
                      timeout=10).json()
    for item in js.get("description", {}).get("data", []):
        if item[0] == "MATDATE":
            return item[2]
    return None

# -------- build key-value dict --------
bond_info = {}
for sid in secids:
    bond_info[sid] = {
        "Maturity": maturity_date(sid),
        "YTM": latest_ytm(sid)          # None if not traded in lookback window
    }

# Pretty-print or use bond_info as needed
from pprint import pprint
pprint(bond_info)
