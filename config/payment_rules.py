PAYMENT_STATUS = [
    "Paid",
    "Failed",
    "Refunded"
]


PAYMENT_STATUS_WEIGHTS = [
    0.90,
    0.08,
    0.02
]


# Processing fee (% of payment)

PROCESSING_FEE_RATE = 0.03


# Estimated operating cost by subscription plan

PLAN_OPERATING_COST = {
    "Basic": 15,
    "Professional": 50,
    "Enterprise": 150
}