import calendar
from pprint import pprint as pp
import plotly.graph_objects as go
import pandas as pd

from stori.config import DAYS_IN_A_MONTH, settings, email_chart_filepath, email_images_title
from stori.helpers import get_static_from_kaleido_server



def plot(df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df.values,
            mode="lines",
            line_color="rgb(219, 129, 188)",
            connectgaps=True,
        )
    )
    fig.update_layout(
        overwrite=True,
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=True,
            ticks="",
        ),
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            ticks="",
            tickfont=dict(
                family="Helvetica",
                size=12,
                color="rgb(0, 104, 128)",
            ),
        ),
    )
    fig.update_layout(
        autosize=True,
        margin=dict(
            autoexpand=True,
            l=0,
            r=0,
            t=0,
            b=0,
        ),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
    )
    max_record = df[df == df.max()]
    fig.add_annotation(
        showarrow=True,
        arrowhead=1,
        align="right",
        x=max_record.index.values[0].astype(str),
        y=max_record[0],
        text="Your 2022 High",
        opacity=0.7,
    )
    image = get_static_from_kaleido_server(fig, "jpg")
    return image


def calculate_stats(df: pd.DataFrame) -> dict:
    df.date = pd.to_datetime(df.date)
    df.set_index("date", inplace=True)
    timespan = (df.iloc[-1].name - df.iloc[0].name).days
    txs_count = df.amount.count()
    df.amount = df.amount.apply(lambda x: x[1:] if x.startswith("+") else x).astype(float)
    credit_txs = df[df.amount > 0]
    debit_txs = df[df.amount < 0]
    total_balance = df.amount.sum()
    daily_balance = df.amount.expanding().sum()
    six_hours = debit_txs.groupby(pd.Grouper(freq="6H")).sum()
    six_hours_avg = six_hours.groupby(six_hours.index.hour).mean()
    data = {
        "transactions_count": txs_count,
        "transactions_per_month": txs_count / (timespan / DAYS_IN_A_MONTH),
        "avg_credit_amount": credit_txs.amount.mean(),
        "avg_debit_amount": debit_txs.amount.mean(),
        "total_balance": total_balance,
        f"last_{settings['months_to_show_in_email']}_months": {
            "transactions": df.groupby(df.index.month)["amount"].count()[-settings["months_to_show_in_email"] :],
            "credit_amount": credit_txs.groupby(credit_txs.index.month)["amount"].sum()[
                -settings["months_to_show_in_email"] :
            ],
            "largest_debit_transaction": debit_txs.groupby(debit_txs.index.month)["amount"].min()[
                -settings["months_to_show_in_email"] :
            ],
        },
        "daily_balance": daily_balance,  # Plot
        "expenses_intraday": six_hours_avg / six_hours_avg.sum(),
    }
    return data


def make_content(stats: dict) -> dict:
    content = {"cells": [], "tables": []}
    for key in stats.keys():
        if key == "total_balance":
            content["cells"].append(
                {
                    "value": f"${round(stats[key], 2):,}",
                    "top_label": "current balance",
                    "bottom_label": "in your account",
                }
            )
        elif key == "transactions_count":
            content["cells"].append(
                {
                    "value": f"{stats[key]}",
                    "top_label": "transactions",
                    "bottom_label": "along the year",
                }
            )
        elif key == "transactions_per_month":
            content["cells"].append(
                {
                    "value": f"{int(stats[key])}",
                    "top_label": "transactions",
                    "bottom_label": "per month",
                }
            )
        elif key == "avg_credit_amount":
            content["cells"].append(
                {
                    "value": f"${round(stats[key], 2):,}",
                    "top_label": "credit amount",
                    "bottom_label": "on average",
                }
            )
        elif key == "avg_debit_amount":
            content["cells"].append(
                {
                    "value": f"${round(stats[key], 2):,}",
                    "top_label": "debit amount",
                    "bottom_label": "on average",
                }
            )
        elif key == f"last_{settings['months_to_show_in_email']}_months":
            month_nums = set(z for y in [i for i in [item.keys().to_list() for item in stats[key].values()]] for z in y)
            content["tables"].append(
                {
                    "table_title": f"Your last {settings['months_to_show_in_email']} months",
                    "columns": list(map(lambda x: calendar.month_name[x], month_nums)),
                    "rows": map(lambda x: x.replace("_", " "), [item for item in stats[key].keys()]),
                    "cells": [item.to_list() for item in stats[key].values()],
                }
            )
        elif key == "daily_balance":
            content["images"] = [{"title": email_images_title, "source": plot(stats["daily_balance"])}]
    return content
