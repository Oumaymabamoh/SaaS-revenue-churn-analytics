import pandas as pd
import numpy as np
from datetime import timedelta
import os

np.random.seed(42)


INTERACTION_TYPES = [
    "Impression",
    "Click",
    "Website Visit",
    "Form Submission",
    "Demo Request",
    "Webinar Attendance",
    "Email Open"
]

INTERACTION_WEIGHTS = [
    0.30,
    0.25,
    0.15,
    0.10,
    0.08,
    0.07,
    0.05
]

ATTRIBUTION_TYPES = [
    "First Touch",
    "Last Touch",
    "Multi Touch"
]

ATTRIBUTION_WEIGHTS = [
    0.50,
    0.30,
    0.20
]


def generate_campaign_touchpoints():

    companies = pd.read_csv(
        "data/raw/companies.csv"
    )

    campaigns = pd.read_csv(
        "data/raw/campaigns.csv"
    )

    subscriptions = pd.read_csv(
        "data/raw/subscriptions.csv"
    )

    touchpoints = []

    touchpoint_counter = 1

    for _, company in companies.iterrows():

        company_id = company["company_id"]

        subscription = subscriptions[
            subscriptions["company_id"] == company_id
        ]

        converted = not subscription.empty

        if converted:
            conversion_date = pd.to_datetime(
                subscription.iloc[0]["start_date"]
            )
        else:
            conversion_date = None

        number_of_touchpoints = np.random.choice(
            [1, 2, 3, 4],
            p=[0.35, 0.35, 0.20, 0.10]
        )

        selected_campaigns = campaigns.sample(
            n=number_of_touchpoints,
            replace=False
        )

        for _, campaign in selected_campaigns.iterrows():

            campaign_start = pd.to_datetime(
                campaign["start_date"]
            )

            campaign_end = pd.to_datetime(
                campaign["end_date"]
            )

            touch_date = campaign_start + timedelta(
                days=np.random.randint(
                    0,
                    max((campaign_end - campaign_start).days, 1)
                )
            )

            days_to_conversion = None

            if converted:

                if touch_date > conversion_date:
                    touch_date = conversion_date - timedelta(
                        days=np.random.randint(1, 30)
                    )

                days_to_conversion = (
                    conversion_date - touch_date
                ).days

            touchpoints.append({

                "touchpoint_id":
                    f"TP_{touchpoint_counter:07d}",

                "company_id":
                    company_id,

                "campaign_id":
                    campaign["campaign_id"],

                "channel":
                    campaign["channel"],

                "touch_date":
                    touch_date.date(),

                "interaction_type":
                    np.random.choice(
                        INTERACTION_TYPES,
                        p=INTERACTION_WEIGHTS
                    ),

                "attribution_type":
                    np.random.choice(
                        ATTRIBUTION_TYPES,
                        p=ATTRIBUTION_WEIGHTS
                    ),

                "converted":
                    converted,

                "days_to_conversion":
                    days_to_conversion

            })

            touchpoint_counter += 1

    return pd.DataFrame(touchpoints)


if __name__ == "__main__":

    df = generate_campaign_touchpoints()

    os.makedirs(
        "data/raw",
        exist_ok=True
    )

    df.to_csv(
        "data/raw/campaign_touchpoints.csv",
        index=False
    )

    print("Generated campaign touchpoints:")
    print(df.head())

    print(f"\nTotal touchpoints: {len(df)}")

    print("\nInteraction types:")
    print(df["interaction_type"].value_counts())

    print("\nConverted companies:")
    print(df["converted"].value_counts())

    print("\nAttribution types:")
    print(df["attribution_type"].value_counts())