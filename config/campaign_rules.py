CHANNELS = [
    "Organic Search",
    "Google Ads",
    "LinkedIn Ads",
    "Referral",
    "Partner",
    "Content Marketing",
    "Email Marketing"
]


CHANNEL_WEIGHTS = [
    0.25,
    0.20,
    0.15,
    0.15,
    0.10,
    0.10,
    0.05
]


CAMPAIGN_TYPES = [
    "Brand Awareness",
    "Product Launch",
    "Lead Generation",
    "Retargeting",
    "Webinar"
]


CAMPAIGN_TYPE_WEIGHTS = [
    0.20,
    0.15,
    0.30,
    0.20,
    0.15
]


CAMPAIGN_STATUS = [
    "Active",
    "Completed",
    "Paused",
    "Cancelled"
]


CAMPAIGN_STATUS_WEIGHTS = [
    0.20,
    0.65,
    0.10,
    0.05
]


# Channel behavior to make SaaS marketing realistic

CHANNEL_PERFORMANCE = {

    "Organic Search": {
        "conversion_rate": 0.08,
        "customer_value_multiplier": 1.2
    },

    "Google Ads": {
        "conversion_rate": 0.05,
        "customer_value_multiplier": 1.0
    },

    "LinkedIn Ads": {
        "conversion_rate": 0.04,
        "customer_value_multiplier": 1.5
    },

    "Referral": {
        "conversion_rate": 0.12,
        "customer_value_multiplier": 1.8
    },

    "Partner": {
        "conversion_rate": 0.10,
        "customer_value_multiplier": 1.6
    },

    "Content Marketing": {
        "conversion_rate": 0.07,
        "customer_value_multiplier": 1.3
    },

    "Email Marketing": {
        "conversion_rate": 0.09,
        "customer_value_multiplier": 1.1
    }

}