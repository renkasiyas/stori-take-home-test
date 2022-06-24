import base64
import json

import pandas as pd
import requests

from stori.config import secrets
from stori.database import SessionLocal


def get_static_from_kaleido_server(fig, format)-> str:
    jdump = json.dumps(fig.to_json())
    b64fig = base64.b64encode(jdump.encode('utf-8'))
    payload = {
        "fig": b64fig.decode('utf-8')
    }
    r = requests.post(f"http://{secrets['DIXIT_IP']}:8030/{format}/600/350", json=payload)
    if r.json():
        return r.json()[format]
    else:
        return ""

def thousand_separator(value, dollar_sign=False):
    """Thousands separator with 2 decimal places for Jinja Template"""
    return f"{('$' if dollar_sign else '')}{float(value):,.2f}"


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def from_db_to_df(db_results: list) -> pd.DataFrame:
    """Convert database objects to Pandas DataFrame"""
    results = []
    to_remove = ["_sa_instance_state", "owner"]
    for r in db_results:
        d = r.__dict__
        for k in list(d.keys()):
            if k in to_remove:
                d.pop(k)
                results.append(d)
    df = pd.DataFrame(results)
    return df
