import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import os


from config.campaign_rules import (
    CHANNELS,
    CHANNEL_WEIGHTS,
    CAMPAIGN_TYPES,
    CAMPAIGN_TYPE_WEIGHTS,
    CAMPAIGN_STATUS,
    CAMPAIGN_STATUS_WEIGHTS,
    CHANNEL_PERFORMANCE
)


fake = Faker()

Faker.seed(42)
np.random.seed(42)



def generate_campaigns(n_campaigns=200):

    campaigns = []

    start_date = datetime(2024, 1, 1)


    for i in range(n_campaigns):

        campaign_id = f"CAM_{i+1:06d}"


        channel = np.random.choice(
            CHANNELS,
            p=CHANNEL_WEIGHTS
        )


        campaign_type = np.random.choice(
            CAMPAIGN_TYPES,
            p=CAMPAIGN_TYPE_WEIGHTS
        )


        status = np.random.choice(
            CAMPAIGN_STATUS,
            p=CAMPAIGN_STATUS_WEIGHTS
        )


        # Marketing budget based on campaign type

        if campaign_type == "Product Launch":

            budget = np.random.randint(
                20000,
                100000
            )


        elif campaign_type == "Webinar":

            budget = np.random.randint(
                5000,
                30000
            )


        elif campaign_type == "Lead Generation":

            budget = np.random.randint(
                10000,
                50000
            )


        elif campaign_type == "Retargeting":

            budget = np.random.randint(
                3000,
                20000
            )


        else:

            budget = np.random.randint(
                5000,
                40000
            )


        # Actual spend can be different from budget

        actual_spend = round(
            budget * np.random.uniform(
                0.70,
                1.10
            ),
            2
        )


        # Marketing funnel

        impressions = np.random.randint(
            10000,
            500000
        )


        clicks = int(
            impressions *
            np.random.uniform(
                0.01,
                0.08
            )
        )


        leads = int(
            clicks *
            np.random.uniform(
                0.05,
                0.30
            )
        )


        conversion_rate = CHANNEL_PERFORMANCE[channel][
            "conversion_rate"
        ]


        paying_customers = int(
            leads *
            conversion_rate
        )


        campaign_revenue = round(
            paying_customers *
            np.random.randint(
                500,
                5000
            ) *
            CHANNEL_PERFORMANCE[channel][
                "customer_value_multiplier"
            ],
            2
        )


        campaign_start = start_date + timedelta(
            days=np.random.randint(
                0,
                700
            )
        )


        duration_days = np.random.randint(
            14,
            90
        )


        campaign_end = campaign_start + timedelta(
            days=duration_days
        )


        campaigns.append({

            "campaign_id": campaign_id,

            "campaign_name": fake.catch_phrase(),

            "channel": channel,

            "campaign_type": campaign_type,

            "campaign_status": status,

            "budget": budget,

            "actual_spend": actual_spend,

            "impressions": impressions,

            "clicks": clicks,

            "leads_generated": leads,

            "paying_customers": paying_customers,

            "conversion_rate": round(
                paying_customers / leads,
                4
            ) if leads > 0 else 0,

            "total_revenue": campaign_revenue,

            "start_date": campaign_start.date(),

            "end_date": campaign_end.date()

        })


    return pd.DataFrame(campaigns)




if __name__ == "__main__":


    df = generate_campaigns(200)


    os.makedirs(
        "data/raw",
        exist_ok=True
    )


    df.to_csv(
        "data/raw/campaigns.csv",
        index=False
    )


    print("Generated campaigns:")
    print(df.head())


    print(
        f"\nTotal campaigns: {len(df)}"
    )


    print(
        "\nChannel distribution:"
    )

    print(
        df["channel"].value_counts()
    )