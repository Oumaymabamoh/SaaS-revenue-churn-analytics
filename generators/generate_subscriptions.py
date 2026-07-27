import pandas as pd
import numpy as np
from datetime import timedelta
import os

from config.subscription_rules import (
    PLANS,
    PLAN_WEIGHTS,
    PLAN_PRICES,
    PLAN_COSTS,
    STATUS,
    STATUS_WEIGHTS,
    BILLING_CYCLES,
    BILLING_CYCLE_WEIGHTS,
    CHURN_REASONS,
    CHURN_REASON_WEIGHTS
)

np.random.seed(42)


def generate_subscriptions():

    companies = pd.read_csv(
        "data/raw/companies.csv"
    )

    subscriptions = []

    subscription_counter = 1

    for _, company in companies.iterrows():

        became_customer = np.random.choice(
            [True, False],
            p=[0.65, 0.35]
        )

        if not became_customer:
            continue

        plan = np.random.choice(
            PLANS,
            p=PLAN_WEIGHTS
        )

        status = np.random.choice(
            STATUS,
            p=STATUS_WEIGHTS
        )

        billing_cycle = np.random.choice(
            BILLING_CYCLES,
            p=BILLING_CYCLE_WEIGHTS
        )

        start_date = pd.to_datetime(
            company["created_date"]
        ) + timedelta(
            days=np.random.randint(7, 120)
        )

        trial_days = np.random.choice(
            [14, 30],
            p=[0.7, 0.3]
        )

        auto_renew = np.random.choice(
            [True, False],
            p=[0.85, 0.15]
        )

        monthly_price = PLAN_PRICES[plan]

        if billing_cycle == "Annual":
            monthly_price = round(
                monthly_price * 12 * 0.90,
                2
            )

        churn_reason = None

        if status == "Cancelled":

            end_date = start_date + timedelta(
                days=np.random.randint(30, 400)
            )

            churn_reason = np.random.choice(
                CHURN_REASONS,
                p=CHURN_REASON_WEIGHTS
            )

        else:

            end_date = None

        subscriptions.append({

            "subscription_id":
                f"SUB_{subscription_counter:07d}",

            "company_id":
                company["company_id"],

            "plan":
                plan,

            "billing_cycle":
                billing_cycle,

            "monthly_price":
                monthly_price,

            "plan_cost":
                PLAN_COSTS[plan],

            "trial_days":
                trial_days,

            "auto_renew":
                auto_renew,

            "start_date":
                start_date.date(),

            "end_date":
                end_date.date()
                if end_date
                else None,

            "status":
                status,

            "churn_reason":
                churn_reason

        })

        subscription_counter += 1

    return pd.DataFrame(subscriptions)


if __name__ == "__main__":

    df = generate_subscriptions()

    os.makedirs(
        "data/raw",
        exist_ok=True
    )

    df.to_csv(
        "data/raw/subscriptions.csv",
        index=False
    )

    print("Generated subscriptions:")
    print(df.head())

    print(f"\nTotal subscriptions: {len(df)}")

    print("\nPlan distribution:")
    print(df["plan"].value_counts())

    print("\nBilling cycle distribution:")
    print(df["billing_cycle"].value_counts())

    print("\nSubscription status:")
    print(df["status"].value_counts())