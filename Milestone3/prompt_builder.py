%%writefile prompt_builder.py
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
    bmi = calculate_bmi(weight, height)
    bmi_status = bmi_category(bmi)
    equipment_list = ", ".join(equipment) if equipment else "No Equipment"

    prompt = f"""
Create a highly structured, 5-day personalized workout plan.

User Profile:
Name: {name}
Age: {age}
Gender: {gender}
BMI: {bmi:.2f} ({bmi_status})
Goal: {goal}
Fitness Level: {fitness_level}
Available Equipment: {equipment_list}

Strict Output Formatting Instructions:
- Use Markdown headers for days: "### Day 1 (Focus Area)"
- List 4-6 exercises per day as a numbered list.
- Format each exercise exactly like this with bolding: "Exercise Name – [Sets] sets – [Reps] reps – [Rest] sec rest"
- Adjust the intensity safely for their BMI ({bmi_status}), age ({age}), and fitness level. If BMI is Obese, prioritize safe, low-impact movements.
- At the bottom, include a "### Notes:" section with bullet points for: Progressive Adjustments, Intensity, Cardio, Core, and Hydration & Warm-Up.

DO NOT output any introductory or concluding conversational text. Output ONLY the workout plan and the Notes.
"""
    return prompt, bmi, bmi_status
