import pandas as pd
import numpy as np
from datetime import datetime
import os

from config.payment_rules import (
    PAYMENT_STATUS,
    PAYMENT_STATUS_WEIGHTS,
    PROCESSING_FEE_RATE,
    PLAN_OPERATING_COST
)

np.random.seed(42)


def generate_payments():

    subscriptions = pd.read_csv(
        "data/raw/subscriptions.csv"
    )

    payments = []

    payment_counter = 1

    simulation_start = datetime(2025, 1, 1)
    simulation_end = datetime(2025, 12, 31)

    for _, subscription in subscriptions.iterrows():

        start_date = pd.to_datetime(
            subscription["start_date"]
        )

        if start_date > simulation_end:
            continue

        if pd.notna(subscription["end_date"]):
            end_date = pd.to_datetime(
                subscription["end_date"]
            )
        else:
            end_date = simulation_end

        current_date = max(
            start_date,
            simulation_start
        )

        while (
            current_date <= end_date
            and current_date <= simulation_end
        ):

            status = np.random.choice(
                PAYMENT_STATUS,
                p=PAYMENT_STATUS_WEIGHTS
            )

            monthly_price = subscription["monthly_price"]

            if status == "Paid":
                revenue = monthly_price

            elif status == "Refunded":
                revenue = -monthly_price

            else:
                revenue = 0

            processing_fee = (
                abs(revenue)
                * PROCESSING_FEE_RATE
            )

            operating_cost = PLAN_OPERATING_COST.get(
                subscription["plan"],
                25
            )

            total_cost = (
                processing_fee
                + operating_cost
            )

            profit = revenue - total_cost

            profit_margin = (
                profit / revenue
                if revenue > 0
                else 0
            )

            payments.append({

                "payment_id":
                    f"PAY_{payment_counter:08d}",

                "subscription_id":
                    subscription["subscription_id"],

                "company_id":
                    subscription["company_id"],

                "payment_date":
                    current_date.date(),

                "amount":
                    revenue,

                "payment_status":
                    status,

                "processing_fee":
                    round(processing_fee, 2),

                "operating_cost":
                    round(operating_cost, 2),

                "total_cost":
                    round(total_cost, 2),

                "profit":
                    round(profit, 2),

                "profit_margin":
                    round(profit_margin, 4)

            })

            payment_counter += 1

            current_date += pd.DateOffset(
                months=1
            )

    return pd.DataFrame(payments)


if __name__ == "__main__":

    df = generate_payments()

    os.makedirs(
        "data/raw",
        exist_ok=True
    )

    df.to_csv(
        "data/raw/payments.csv",
        index=False
    )

    print("Generated payments:")
    print(df.head())

    print(
        f"\nTotal payments: {len(df)}"
    )

    print(
        "\nPayment status distribution:"
    )
    print(
        df["payment_status"].value_counts()
    )

    print(
        "\nTotal revenue:"
    )
    print(
        df["amount"].sum()
    )

    print(
        "\nTotal profit:"
    )
    print(
        df["profit"].sum()
    )

    print(
        "\nAverage profit margin:"
    )
    print(
        round(
            df["profit_margin"].mean() * 100,
            2
        ),
        "%"
    )