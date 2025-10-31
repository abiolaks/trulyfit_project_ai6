import pandas as pd
import random

# Load your meals.csv file
df = pd.read_csv("data/meals.csv")


def generate_meal_plan(calorie_target):
    categories = ["breakfast", "lunch", "dinner", "snack"]
    plan = pd.DataFrame(columns=df.columns)

    for cat in categories:
        meal_options = df[df["category"] == cat]
        if not meal_options.empty:
            meal = meal_options.sample(1)
            plan = pd.concat([plan, meal], ignore_index=True)

    total_cal = plan["calories"].sum()
    diff = calorie_target - total_cal

    # Adjust if difference > 10% of target
    if abs(diff) > 0.1 * calorie_target:
        cat_to_adjust = random.choice(categories)
        candidates = df[df["category"] == cat_to_adjust]
        close_meal = candidates.iloc[
            (candidates["calories"] - diff / 4).abs().argsort()[:1]
        ]
        plan.loc[plan["category"] == cat_to_adjust] = close_meal.values
        total_cal = plan["calories"].sum()

    return plan, total_cal
