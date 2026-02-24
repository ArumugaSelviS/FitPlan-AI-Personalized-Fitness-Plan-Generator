def calculate_bmi(weight, height):
    height_m = height / 100
    return weight / (height_m ** 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def build_prompt(name, age, gender, height, weight, goal, fitness_level, equipment):

    # ----------- BMI CALCULATION -----------
    bmi = calculate_bmi(weight, height)
    bmi_status = bmi_category(bmi)

    # ----------- EQUIPMENT FORMAT -----------
    equipment_list = ", ".join(equipment) if equipment else "No Equipment"

    # ----------- PROMPT BUILDING -----------
    prompt = f"""
You are a certified professional fitness trainer.

Create a structured 5-day personalized workout plan.

User Profile:
- Name: {name}
- Age: {age}
- Gender: {gender}
- Height: {height} cm
- Weight: {weight} kg
- BMI: {bmi:.2f} ({bmi_status})
- Goal: {goal}
- Fitness Level: {fitness_level}
- Available Equipment: {equipment_list}

Instructions:
1. Divide clearly into Day 1 to Day 5.
2. Under each day include 4-6 exercises.
3. For each exercise include:
   - Exercise Name
   - Sets
   - Reps
   - Rest Period
4. Adjust intensity based on:
   - Age
   - BMI category
   - Fitness level
5. Avoid unsafe exercises for beginners or higher age users.
6. Make the plan progressive across 5 days.
7. Keep it professional, realistic, and easy to follow.
8. Do NOT include explanations outside the workout plan.

Return only the workout plan.
"""

    return prompt, bmi, bmi_status
