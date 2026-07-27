import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import os


from config.company_rules import (
    INDUSTRIES,
    INDUSTRY_WEIGHTS,
    COMPANY_SIZES,
    COMPANY_SIZE_WEIGHTS,
    CUSTOMER_SEGMENTS,
    CUSTOMER_SEGMENT_WEIGHTS,
    ACQUISITION_CHANNELS,
    ACQUISITION_CHANNEL_WEIGHTS
)


# Reproducibility
fake = Faker()

Faker.seed(42)
np.random.seed(42)



# Countries grouped by region

REGIONS = {

    "North America": [
        "United States",
        "Canada",
        "Mexico"
    ],

    "Europe": [
        "Germany",
        "France",
        "United Kingdom",
        "Spain"
    ],

    "Asia-Pacific": [
        "Japan",
        "Australia",
        "Singapore",
        "India"
    ],

    "Latin America": [
        "Brazil",
        "Argentina",
        "Chile"
    ],

    "Africa": [
        "South Africa",
        "Nigeria",
        "Kenya",
        "Tanzania"
    ]

}



# Create country-region mapping

COUNTRIES = []


for region, country_list in REGIONS.items():

    for country in country_list:

        COUNTRIES.append(
            {
                "country": country,
                "region": region
            }
        )





def generate_companies(n_companies=1000):


    companies = []


    start_date = datetime(2020, 1, 1)



    for i in range(n_companies):


        # Company ID

        company_id = f"CMP_{i+1:06d}"



        # Industry

        industry = np.random.choice(
            INDUSTRIES,
            p=INDUSTRY_WEIGHTS
        )



        # Company size

        company_size = np.random.choice(
            COMPANY_SIZES,
            p=COMPANY_SIZE_WEIGHTS
        )



        # Customer segment

        customer_segment = np.random.choice(
            CUSTOMER_SEGMENTS,
            p=CUSTOMER_SEGMENT_WEIGHTS
        )



        # Acquisition channel

        acquisition_channel = np.random.choice(
            ACQUISITION_CHANNELS,
            p=ACQUISITION_CHANNEL_WEIGHTS
        )



        # Employees based on company size

        if company_size == "Startup":

            employees = np.random.randint(
                1,
                20
            )


        elif company_size == "Small Business":

            employees = np.random.randint(
                20,
                100
            )


        elif company_size == "Mid-Market":

            employees = np.random.randint(
                100,
                500
            )


        else:

            employees = np.random.randint(
                500,
                5000
            )



        # Company creation date

        created_date = start_date + timedelta(
            days=np.random.randint(
                0,
                1800
            )
        )



        # Country and region

        location = np.random.choice(
            COUNTRIES
        )



        companies.append(

            {


                "company_id": company_id,


                "company_name": fake.company(),


                "industry": industry,


                "company_size": company_size,


                "customer_segment": customer_segment,


                "employees": employees,


                "country": location["country"],


                "region": location["region"],


                "acquisition_channel": acquisition_channel,


                "created_date": created_date.date()

            }

        )



    return pd.DataFrame(companies)





if __name__ == "__main__":


    df = generate_companies(1000)



    # Create output folder

    os.makedirs(
        "data/raw",
        exist_ok=True
    )



    # Save CSV

    df.to_csv(
        "data/raw/companies.csv",
        index=False
    )



    print("Generated companies:")

    print(df.head())



    print(
        f"\nTotal companies: {len(df)}"
    )



    print(
        "\nCompany size distribution:"
    )

    print(
        df["company_size"].value_counts()
    )



    print(
        "\nCustomer segment distribution:"
    )

    print(
        df["customer_segment"].value_counts()
    )



    print(
        "\nAcquisition channel distribution:"
    )

    print(
        df["acquisition_channel"].value_counts()
    )



    print(
        "\nRegion distribution:"
    )

    print(
        df["region"].value_counts()
    )