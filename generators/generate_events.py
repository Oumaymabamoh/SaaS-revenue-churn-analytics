import os
import pandas as pd
import numpy as np
from faker import Faker
from datetime import timedelta

from config.event_rules import (
    EVENTS,
    EVENT_WEIGHTS,
    FEATURES,
    EVENT_SCORES
)

fake = Faker()

Faker.seed(42)
np.random.seed(42)


def generate_events():

    users = pd.read_csv("data/raw/users.csv")

    events = []

    event_counter = 1

    for _, user in users.iterrows():

        signup_date = pd.to_datetime(user["signup_date"])
        last_activity = pd.to_datetime(user["last_activity_date"])

        engagement = user["engagement_level"]

        if engagement == "High":
            number_of_events = np.random.randint(80, 201)

        elif engagement == "Medium":
            number_of_events = np.random.randint(30, 80)

        else:
            number_of_events = np.random.randint(5, 30)

        if last_activity <= signup_date:
            last_activity = signup_date + timedelta(days=1)

        total_days = max((last_activity - signup_date).days, 1)

        for _ in range(number_of_events):

            event_name = np.random.choice(
                EVENTS,
                p=EVENT_WEIGHTS
            )

            feature = np.random.choice(FEATURES)

            event_date = signup_date + timedelta(
                days=np.random.randint(0, total_days + 1)
            )

            events.append({

                "event_id": f"EVT_{event_counter:09d}",

                "user_id": user["user_id"],

                "company_id": user["company_id"],

                "event_name": event_name,

                "feature": feature,

                "event_score": EVENT_SCORES[event_name],

                "event_date": event_date.date()

            })

            event_counter += 1

    return pd.DataFrame(events)


if __name__ == "__main__":

    df = generate_events()

    os.makedirs(
        "data/raw",
        exist_ok=True
    )

    df.to_csv(
        "data/raw/events.csv",
        index=False
    )

    print("Generated events:")
    print(df.head())

    print(f"\nTotal events: {len(df):,}")

    print("\nTop events:")
    print(df["event_name"].value_counts())

    print("\nTop features:")
    print(df["feature"].value_counts())