import pandas as pd
import random
import os
import uuid

# Path to activities.csv
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "activities.csv")

def generate_plans(budget, region, lifestyle):
    df = pd.read_csv(DATA_PATH)

    # Normalize comparison
    lifestyle = lifestyle.replace('-', '_')
    region = region.lower()
    lifestyle = lifestyle.lower()

    # Debug
    print("Available lifestyles:", df['lifestyle'].unique())
    print("Available regions:", df['region'].unique())

    # Filter based on region and lifestyle
    filtered = df[
        (df['region'].str.lower() == region) &
        (df['lifestyle'].str.lower() == lifestyle)
    ]

    if filtered.empty:
        return {"plans": []}

    # Try to select a realistic accommodation activity
    accommodation_options = df[
        (df['region'].str.lower() == region) &
        (df['type'].isin(['relaxation', 'food'])) &
        (df['lifestyle'].str.lower() == lifestyle)
    ]

    if not accommodation_options.empty:
        selected_accommodation = accommodation_options.sample(1).iloc[0]
        accommodation = {
            "name": selected_accommodation["activity_name"],
            "type": selected_accommodation["type"].capitalize(),
            "cost": selected_accommodation["cost_mad"],
            "description": selected_accommodation["description"]
        }
    else:
        accommodation = {
            "name": "Local Guesthouse",
            "type": "Riad",
            "cost": random.randint(250, 400),
            "description": f"A comfortable traditional stay in {region.title()}."
        }

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
