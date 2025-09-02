import requests
import datetime
from pprint import pprint

secids = [
    'SU26207RMFS9', 'SU26212RMFS9', 'SU26218RMFS6', 'SU26219RMFS4',
    'SU26221RMFS0', 'SU26224RMFS4', 'SU26225RMFS1', 'SU26226RMFS9',
    'SU26228RMFS5', 'SU26229RMFS3', 'SU26230RMFS1', 'SU26232RMFS7',
    'SU26233RMFS5', 'SU26235RMFS0', 'SU26236RMFS8', 'SU26237RMFS6',
    'SU26238RMFS4', 'SU26239RMFS2', 'SU26240RMFS0', 'SU26241RMFS8',
    'SU26242RMFS6', 'SU26243RMFS4', 'SU26244RMFS2', 'SU26245RMFS9'
]

def fetch_history_rows(session, secid, day):
    """
    Fetch all history rows for a given secid and date,
    without specifying board, so that 'from'/'till' actually filter.
    """
    url = f"https://iss.moex.com/iss/history/engines/stock/markets/bonds/securities/{secid}.json"
    params = {
        'from': day,
        'till': day,
        'iss.meta': 'off'
    }
    r = session.get(url, params=params, timeout=10)
    js = r.json()
    data = js.get("history", {}).get("data", [])
    cols = js.get("history", {}).get("columns", [])
    return data, cols

def latest_ytm(session, secid, target_date, lookback=5):
    """
    Look back up to `lookback` days (including target_date) to find a non-null YTM.
    Returns (YTM, date) or (None, None).
    """
    for delta in range(lookback + 1):
        day = (target_date - datetime.timedelta(days=delta)).strftime("%Y-%m-%d")
        rows, cols = fetch_history_rows(session, secid, day)
        if not rows:
            continue
        # Try fields in priority order
        for fld in ("YIELDCLOSE", "YIELD", "YIELDLASTCOUPON"):
            if fld in cols:
                idx = cols.index(fld)
                val = rows[0][idx]
                if val is not None:
                    return float(val), day
    return None, None

def maturity_date(session, secid):
    """
    Fetch the MATDATE field from description.
    """
    url = f"https://iss.moex.com/iss/securities/{secid}.json"
    r = session.get(url, params={'iss.meta': 'off'}, timeout=10)
    js = r.json()
    for row in js.get("description", {}).get("data", []):
        if row[0] == "MATDATE":
            return row[2]
    return None

def build_bond_data(target_date):
    session = requests.Session()
    bond_info = {}
    for sid in secids:
        mat = maturity_date(session, sid)
        ytm, obs = latest_ytm(session, sid, target_date)
        bond_info[sid] = {
            "Maturity": mat,
            "YTM": ytm
        }
    return bond_info

if __name__ == "__main__":
    target_date = datetime.date(2025, 6, 18)
    bond_data = build_bond_data(target_date)
    print(f"Bond data as of {target_date}:")
    pprint(bond_data)