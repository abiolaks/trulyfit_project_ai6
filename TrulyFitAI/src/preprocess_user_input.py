import numpy as np

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return round(weight / (height_m ** 2), 2)

def estimate_body_fat_percentage(gender, bmi, age):
    """
    Deurenberg formula for adults:
    BF% = 1.20 * BMI + 0.23 * Age - 10.8 * Sex - 5.4
    Sex = 1 (male), 0 (female)
    """
    sex = 1 if gender.lower() == "male" else 0
    bf = 1.20 * bmi + 0.23 * age - 10.8 * sex - 5.4
    return round(max(bf, 0), 2)

def estimate_lean_mass(weight, fat_percentage):
    return round(weight * (1 - fat_percentage / 100), 2)

def calculate_protein_per_kg(weight, goal):
    goal = goal.lower()
    if "lose" in goal:
        ppk = np.random.uniform(1.6, 2.2)
    elif "gain" in goal:
        ppk = np.random.uniform(1.8, 2.4)
    else:
        ppk = np.random.uniform(1.2, 1.8)
    return round(ppk, 2)
