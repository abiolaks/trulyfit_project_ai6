import streamlit as st
import pandas as pd
import mlflow.pyfunc
import os
from dotenv import load_dotenv
from generate_meal_plan import generate_meal_plan
from preprocess_user_input import (
    calculate_bmi,
    estimate_body_fat_percentage,
    estimate_lean_mass,
    calculate_protein_per_kg,
)
import joblib

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="TrulyFitAI", layout="wide")
st.title("TrulyFitAI — Personalized Fitness & Meal Recommendation")

# ---------------------------
# LOAD ENV AND MLflow MODEL
# ---------------------------
load_dotenv()

os.environ["MLFLOW_TRACKING_URI"] = os.getenv("MLFLOW_TRACKING_URI")
os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_TRACKING_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_TRACKING_PASSWORD")

# logged_model = "runs:/4bc4b3ab71bc43fc96adb9211e65cd58/RandomForest" : loading from dagshub run
# model = joblib.load("models/best_random_forest_pipeline.joblib")

try:
    # model = mlflow.pyfunc.load_model(logged_model)
    model = joblib.load("../models/best_random_forest_pipeline.joblib")
    st.sidebar.success(" Model loaded successfully from MLflow")
except Exception as e:
    model = None
    st.sidebar.error(f" Model failed to load: {e}")


# ---------------------------
# HELPER: Adjust Meal Calories
# ---------------------------
def adjust_meal_plan(
    plan, total_calories, target_calories, tolerance=0.05, max_iters=5
):
    """
    Iteratively scales portions up/down to bring total calories within ±5% of target.
    """
    plan = plan.copy()
    iteration = 0

    while iteration < max_iters:
        diff = target_calories - total_calories
        diff_ratio = diff / target_calories

        #  If within tolerance, stop adjusting
        if abs(diff_ratio) <= tolerance:
            break

        # Scale all nutrients proportionally
        scale_factor = target_calories / total_calories
        plan["calories"] = (plan["calories"] * scale_factor).round(1)
        plan["protein"] = (plan["protein"] * scale_factor).round(1)
        plan["carbs"] = (plan["carbs"] * scale_factor).round(1)
        plan["fat"] = (plan["fat"] * scale_factor).round(1)

        # Recalculate total
        total_calories = plan["calories"].sum()
        iteration += 1

    return plan, round(total_calories, 1)


# ---------------------------
# HELPER: Nutrition Summary Visualization
# ---------------------------
def show_nutrition_summary(plan_df, target_calories):
    st.markdown("###  Daily Nutrition Summary")

    total_calories = plan_df["calories"].sum()
    total_protein = plan_df["protein"].sum()
    total_carbs = plan_df["carbs"].sum()
    total_fat = plan_df["fat"].sum()

    # Rough calorie breakdown for macros
    protein_cal = total_protein * 4
    carb_cal = total_carbs * 4
    fat_cal = total_fat * 9

    total_macro_cal = protein_cal + carb_cal + fat_cal
    protein_pct = (protein_cal / total_macro_cal) * 100 if total_macro_cal > 0 else 0
    carb_pct = (carb_cal / total_macro_cal) * 100 if total_macro_cal > 0 else 0
    fat_pct = (fat_cal / total_macro_cal) * 100 if total_macro_cal > 0 else 0

    st.metric(" Target Calories", f"{target_calories:.0f} kcal")
    st.metric(" Planned Calories", f"{total_calories:.0f} kcal")
    st.write("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("####  Protein")
        st.write(f"**{total_protein:.1f} g** ({protein_pct:.1f}%)")
        st.progress(min(protein_pct / 100, 1.0))
    with col2:
        st.markdown("####  Carbs")
        st.write(f"**{total_carbs:.1f} g** ({carb_pct:.1f}%)")
        st.progress(min(carb_pct / 100, 1.0))
    with col3:
        st.markdown("####  Fat")
        st.write(f"**{total_fat:.1f} g** ({fat_pct:.1f}%)")
        st.progress(min(fat_pct / 100, 1.0))

    st.write("---")
    st.markdown(
        f"** Macro Split:** {protein_pct:.0f}% protein | {carb_pct:.0f}% carbs | {fat_pct:.0f}% fat"
    )


# ---------------------------
# USER INPUT FORM
# ---------------------------
with st.form("user_input"):
    col1, col2, col3 = st.columns(3)
    with col1:
        weight = st.number_input("Weight (kg)", 40.0, 180.0, 70.0)
        height = st.number_input("Height (cm)", 130.0, 220.0, 175.0)
    with col2:
        age = st.number_input("Age", 16, 80, 28)
        gender = st.selectbox("Gender", ["Male", "Female"])
    with col3:
        goal = st.selectbox("Goal", ["Lose Weight", "Maintain Weight", "Gain Weight"])
        activity = st.selectbox("Activity Level", ["Low", "Moderate", "High"])

    submitted = st.form_submit_button(" Generate Meal Plan")

# ---------------------------
# PREDICTION + MEAL PLAN
# ---------------------------
if submitted:
    if model is None:
        st.error(" Model not loaded properly.")
    else:
        # Compute user metrics
        bmi = calculate_bmi(weight, height)
        fat_percentage = estimate_body_fat_percentage(gender, bmi, age)
        lean_mass = estimate_lean_mass(weight, fat_percentage)
        protein_per_kg = calculate_protein_per_kg(weight, goal)

        features = pd.DataFrame(
            [
                {
                    "weight_(kg)": weight,
                    "lean_mass_kg": lean_mass,
                    "bmi": bmi,
                    "fat_percentage": fat_percentage,
                    "protein_per_kg": protein_per_kg,
                }
            ]
        )

        # Predict calorie target
        predicted_calories = int(model.predict(features)[0])
        st.subheader(" Predicted Daily Calorie Target")
        st.metric(label="Calories per Day", value=f"{predicted_calories:,} kcal")

        # Generate and adjust meal plan
        plan, total = generate_meal_plan(predicted_calories)
        plan, adjusted_total = adjust_meal_plan(plan, total, predicted_calories)
        diff = predicted_calories - adjusted_total

        # Display meal plan
        st.subheader(" Recommended Meal Plan")
        st.dataframe(
            plan[["food", "calories", "protein", "carbs", "fat", "category"]],
            use_container_width=True,
        )

        # Show totals and feedback
        st.write(f"**Total Calories:** {adjusted_total} kcal")
        st.write(f"**Difference from target:** {diff:+.0f} kcal")

        if abs(diff) > 0.15 * predicted_calories:
            st.warning(
                " The plan still differs notably from your target calories. "
                "Try adjusting portion sizes manually for better precision."
            )
        else:
            st.success(" Great! The plan closely matches your calorie target.")

        # Display nutrition summary
        show_nutrition_summary(plan, predicted_calories)
