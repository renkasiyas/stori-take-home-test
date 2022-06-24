import datetime

from dateutil import parser as dateparser
import numpy as np
import pandas as pd

from stori.config import DAYS_IN_A_MONTH, csv_filepath, settings

TXS_SINCE = dateparser.parse(settings["txs_since"])
delta = max(
    abs((TXS_SINCE - (TXS_SINCE + datetime.timedelta(days=365))).days),
    abs((TXS_SINCE - dateparser.parse(f"12/31/{TXS_SINCE.year}")).days),
)
TXS_UNTIL = TXS_SINCE + datetime.timedelta(days=delta)


def gen_dates() -> list:
    """Generate random list of dates for transactions"""
    txs_per_month = settings["simulated_txs_per_month"] * np.random.randint(75, 110) / 100
    total_dates = int(txs_per_month * ((TXS_UNTIL - TXS_SINCE).days / DAYS_IN_A_MONTH))
    start = int(TXS_SINCE.timestamp())
    stop = int(TXS_UNTIL.timestamp())
    time_span = int(stop - start)
    step = int((time_span / total_dates) / 2)
    all_timestamps = [t for t in range(start, stop + step, step)]
    dates = np.random.choice(all_timestamps, total_dates)
    dates.sort()
    return dates


def gen_tx(date: datetime) -> dict:
    """Generate transactions with weighted random amounts using dates"""
    weigths = [50, -3, -5, -10, -25]
    amount = np.round(np.random.rand() ** 2 * 100 * np.random.choice(weigths), 2)
    if settings["amount_as_string"]:
        amount = f"+{amount}" if amount >= 0 else f"{amount}"
    return {
        "date": datetime.datetime.fromtimestamp(date),
        "amount": amount,
    }


def generate_txs(write_csv: bool = False) -> pd.DataFrame:
    """Generate full df of transactions. Used to populate db or create the csv"""
    dates = gen_dates()
    txs = pd.DataFrame(columns=["date", "amount"], data=[gen_tx(date) for date in dates])
    if write_csv:
        txs.to_csv(csv_filepath, mode="w", index=False)
    return txs


if __name__ == "__main__":
    txs = generate_txs(write_csv=True)
