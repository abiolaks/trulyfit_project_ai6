# TrulyFitAI
# trulyfit_project_ai6


## Timeline
| Task | Duration | Deadline |
|------|----------|----------|
| EDA | 26th - 1st October | 2nd October |
| Data Enrichment | 4th - 9th October | 10th October |
| Preprocessing Pipeline | 10th October - 11th October | 12th October |
| Model Training | 13th - 18th October | 20th October |
| Front-end & Model Deployment | 21st - 25th October | 25th October |
| Documentation | Throughout the Project | End of project |




#  Fitness Recommendation AI — End-to-End Project Documentation

##  1. Problem Statement

Modern fitness journeys often fail due to one-size-fits-all meal and workout plans that ignore individual differences in body type, metabolism, goals, and adherence levels.  
People struggle to:
- Know *how many calories they need per day* to reach their goals.  
- Get *personalized meal and exercise plans* that fit their lifestyle.  
- Receive *adaptive recommendations* based on their real progress over time.  

This project aims to solve these problems using *Machine Learning (ML)* and *data-driven personalization*.

---

## 2. Project Objective

To build an *AI-powered fitness recommendation system* that:
1. Predicts a user’s *daily calorie requirement* based on personal attributes and goals.  
2. Generates a *personalized meal plan* and *workout routine* that align with the calorie target and goal.  
3. Tracks user progress over time (weight, adherence, energy level) to *adapt recommendations* dynamically.  

The end goal is to provide an intelligent, continuously learning fitness assistant.

---

## 3. Methodology Overview

The system will be developed in *phases*, evolving from a rule-based MVP to an adaptive ML system.

| Phase | Focus | Description |
|-------|--------|-------------|
| *Phase 1* | Data Setup | Gather and structure user profile, meal, and workout datasets. |
| *Phase 2* | Calorie Prediction | Build a regression model to predict daily calorie needs based on user profile. |
| *Phase 3* | Personalized Recommendation | Generate meals and workouts matching calorie goals and user preferences. |
| *Phase 4* | Progress Tracking | Collect feedback such as adherence, weight change, and energy level. |
| *Phase 5* | Adaptive Learning | Retrain model weekly using progress data to make adaptive calorie/workout recommendations. |
| *Phase 6* | Multi-User Intelligence | Use collaborative filtering to recommend meals/workouts based on similar users’ success. |
| *Phase 7* | Deployment | Build a Streamlit dashboard for real-time interaction and visualization. |

---

##  4. Data Requirements and Sources

### A. User Profile Dataset
*Purpose:* To predict calorie needs and personalize recommendations.

| Feature | Type | Description |
|----------|------|-------------|
| user_id | ID | Unique identifier |
| name | string | User name |
| age | numeric | User’s age |
| gender | categorical | Male/Female |
| height_cm | numeric | Height in cm |
| weight_kg | numeric | Weight in kg |
| goal | categorical | lose_weight / maintain / gain_muscle |
| bmi | numeric | Calculated as weight / (height²) |
| experience_level | categorical | beginner / intermediate / advanced |
| equipment | categorical | home / gym / none |
| calorie_target | numeric | (Label) Daily calorie target — predicted or derived |

 *Source:* Provided 20k user profile dataset (Final_data.csv)

---

### B. Meal Dataset
*Purpose:* To generate balanced, goal-aligned meal recommendations.

| Feature | Description |
|----------|-------------|
| meal_id | Unique meal identifier |
| meal_name | Meal name (e.g., "Grilled Chicken with Rice") |
| calories | Total calories per portion |
| protein | Protein content (g) |
| carbs | Carbohydrates (g) |
| fats | Fat content (g) |
| category | e.g., breakfast/lunch/dinner/snack |
| goal_tag | lose_weight / gain_muscle / maintain |
| source | e.g., USDA API / manually curated |

 *Source:* USDA FoodData Central API (for open-source nutrition data)

---

### C. Exercise Dataset
*Purpose:* To recommend workouts aligned with goal, equipment, and level.

| Feature | Description |
|----------|-------------|
| exercise_id | Unique ID |
| exercise_name | e.g., "Push-ups" |
| target_muscle | e.g., chest, legs |
| difficulty | beginner / intermediate / advanced |
| equipment | bodyweight / dumbbell / barbell / none |
| duration_min | Average duration |
| calories_burned | Estimated calories burned per session |

 *Source:* ExerciseDB API or curated GYM.csv dataset

---

## 5. System Architecture

```
flowchart TD
    A[User Profile Input] --> B[Calorie Prediction Model]
    B --> C[Calorie Target (kcal/day)]
    C --> D[Meal Plan Generator]
    C --> E[Workout Plan Generator]
    D & E --> F[Personalized Recommendation Output]
    F --> G[User Progress Logging]
    G --> H[Adaptive Learning Model]
    H --> D & E
```