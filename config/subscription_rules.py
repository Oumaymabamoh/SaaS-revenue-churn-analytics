PLANS = [
    "Starter",
    "Professional",
    "Business",
    "Enterprise"
]


PLAN_WEIGHTS = [
    0.40,
    0.35,
    0.20,
    0.05
]


PLAN_PRICES = {
    "Starter": 49,
    "Professional": 199,
    "Business": 499,
    "Enterprise": 1500
}


# Estimated monthly servicing cost
PLAN_COSTS = {
    "Starter": 15,
    "Professional": 50,
    "Business": 120,
    "Enterprise": 350
}


STATUS = [
    "Active",
    "Cancelled"
]


STATUS_WEIGHTS = [
    0.85,
    0.15
]


BILLING_CYCLES = [
    "Monthly",
    "Annual"
]


BILLING_CYCLE_WEIGHTS = [
    0.80,
    0.20
]


CHURN_REASONS = [
    "Price",
    "Low Usage",
    "Switched Competitor",
    "Business Closed",
    "Missing Features"
]


CHURN_REASON_WEIGHTS = [
    0.30,
    0.25,
    0.20,
    0.10,
    0.15
]