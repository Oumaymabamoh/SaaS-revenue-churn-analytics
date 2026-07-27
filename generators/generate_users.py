import pandas as pd
import numpy as np
from faker import Faker
from datetime import timedelta
import os


from config.user_rules import (
    ROLES,
    PERSONAS,
    USER_ROLE_WEIGHTS,
    PERSONA_WEIGHTS,
    USER_STATUS,
    USER_STATUS_WEIGHTS,
    ENGAGEMENT_LEVELS,
    ENGAGEMENT_LEVEL_WEIGHTS
)



fake = Faker()

Faker.seed(42)
np.random.seed(42)



def generate_number_of_users(company_size):


    if company_size == "Startup":

        return np.random.randint(
            1,
            6
        )


    elif company_size == "Small Business":

        return np.random.randint(
            3,
            21
        )


    elif company_size == "Mid-Market":

        return np.random.randint(
            20,
            101
        )


    else:

        return np.random.randint(
            100,
            501
        )





def generate_users():


    companies = pd.read_csv(
        "data/raw/companies.csv"
    )


    users = []


    user_counter = 1



    for _, company in companies.iterrows():


        number_of_users = generate_number_of_users(
            company["company_size"]
        )



        for _ in range(number_of_users):


            user_id = f"USR_{user_counter:07d}"



            role = np.random.choice(
                ROLES,
                p=USER_ROLE_WEIGHTS
            )



            persona = np.random.choice(
                PERSONAS,
                p=PERSONA_WEIGHTS
            )



            user_status = np.random.choice(
                USER_STATUS,
                p=USER_STATUS_WEIGHTS
            )



            engagement_level = np.random.choice(
                ENGAGEMENT_LEVELS,
                p=ENGAGEMENT_LEVEL_WEIGHTS
            )



            signup_date = pd.to_datetime(
                company["created_date"]
            ) + timedelta(
                days=np.random.randint(
                    0,
                    365
                )
            )



            # Last activity depends on engagement

            if engagement_level == "High":

                activity_days = np.random.randint(
                    0,
                    15
                )


            elif engagement_level == "Medium":

                activity_days = np.random.randint(
                    15,
                    60
                )


            else:

                activity_days = np.random.randint(
                    60,
                    180
                )



            last_activity_date = (
                pd.Timestamp.today()
                -
                pd.Timedelta(
                    days=activity_days
                )
            )



            users.append({

                "user_id": user_id,


                "company_id": company["company_id"],


                "role": role,


                "persona": persona,


                "user_status": user_status,


                "engagement_level": engagement_level,


                "country": company["country"],


                "region": company["region"],


                "signup_date": signup_date.date(),


                "last_activity_date": last_activity_date.date()

            })



            user_counter += 1



    return pd.DataFrame(users)





if __name__ == "__main__":


    df = generate_users()



    os.makedirs(
        "data/raw",
        exist_ok=True
    )



    df.to_csv(
        "data/raw/users.csv",
        index=False
    )



    print("Generated users:")

    print(df.head())



    print(
        f"\nTotal users: {len(df)}"
    )



    print(
        "\nRole distribution:"
    )

    print(
        df["role"].value_counts()
    )



    print(
        "\nEngagement distribution:"
    )

    print(
        df["engagement_level"].value_counts()
    )



    print(
        "\nUser status distribution:"
    )

    print(
        df["user_status"].value_counts()
    )