import pandas as pd
import random
import os

# Define the path to your activities.csv
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "activities.csv")

# Optional currency rates (customize as needed)
CURRENCY_RATES = {
    "MAD": 1.0,
    "USD": 0.10,
    "EUR": 0.095,
    "JPY": 0.072
}

import pandas as pd
import random
import os
import uuid

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "activities.csv")

def generate_plans(budget, region, lifestyle):
    df = pd.read_csv(DATA_PATH)

    # Debug
    print("Available lifestyles:", df['lifestyle'].unique())
    print("Available regions:", df['region'].unique())

    lifestyle = lifestyle.replace('-', '_')
    filtered = df[(df['region'] == region) & (df['lifestyle'] == lifestyle)]

    if filtered.empty:
        return {"plans": []}

    plans = []

    for i in range(3):
        remaining_budget = budget
        day_plan = []
        used_indices = set()
        flat_activities = []

        for day in range(1, 4):
            day_activities = []
            for _ in range(random.randint(1, 2)):
                options = filtered[~filtered.index.isin(used_indices)]
                if options.empty:
                    break
                activity = options.sample(1).iloc[0]
                if remaining_budget - activity["cost_mad"] >= 0:
                    used_indices.add(activity.name)
                    remaining_budget -= activity["cost_mad"]
                    act_obj = {
                        "name": activity["activity_name"],
                        "cost": activity["cost_mad"],
                        "duration": f"{activity['duration_hrs']} hrs",
                        "description": activity["type"],
                        "day": day
                    }
                    day_activities.append(act_obj)
                    flat_activities.append(act_obj)
            day_plan.append(day_activities)

        # Fake accommodation (or pull randomly from dataset if you want)
        accommodation = {
            "name": "Riad Zayna",
            "type": "Riad",
            "cost": random.randint(200, 400),
            "description": "A traditional Moroccan guesthouse in the medina."
        }

        total_cost = sum(a["cost"] for a in flat_activities) + accommodation["cost"]

        plan = {
            "id": str(uuid.uuid4()),
            "title": f"{lifestyle.replace('_', ' ').title()} Plan {i+1}",
            "description": f"A custom {lifestyle.replace('_', ' ')} travel experience in {region.title()}",
            "activities": flat_activities,
            "totalCost": total_cost,
            "duration": "3 days",
            "accommodation": accommodation
        }

        plans.append(plan)

    return {"plans": plans}
