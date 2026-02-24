FitPlan AI – Milestone Report

1️) Objective of the Milestone

The objective of this milestone was to develop an AI-powered fitness planning system called FitPlan AI, which generates a personalized 5-day workout plan based on user inputs such as:

Name

Age

Gender

Height & Weight

BMI category

Fitness goal

Fitness level

Available equipment

The system dynamically generates structured workout plans using a Large Language Model (LLM), ensuring:

Safe exercise recommendations

Intensity adjustment based on BMI and age

Beginner-friendly modifications

Progressive 5-day training structure

The goal was to integrate AI into a real-world fitness application with proper UI navigation and deployment.

2️) Model Name Used

The model used for workout generation is:

Mistral-7B-Instruct-v0.2

This model is accessed via the inference API from:

Hugging Face

Why This Model?

Instruction-tuned model

Strong structured text generation capability

Good reasoning ability

Suitable for personalized plan generation

Efficient for API-based deployment

3️) Prompt Design Explanation

The prompt is carefully structured to ensure:

* Role Assignment
You are a certified professional fitness trainer.

This forces the model to respond professionally.

* User Profile Embedding

The prompt dynamically inserts:

Age

BMI value and BMI category

Fitness level

Equipment availability

Example snippet:

User Profile:
- Name: Arumugaselvi
- Age: 22
- BMI: 23.4 (Normal Weight)
- Goal: Build Muscle
- Fitness Level: Beginner
  * Clear Instructions

The model is instructed to:

Divide clearly into Day 1 to Day 5

Include 4–6 exercises per day

Include:

Exercise name

Sets

Reps

Rest period

Adjust intensity based on:

Age

BMI category

Fitness level

Avoid unsafe exercises for beginners

* Output Restriction
Return only the workout plan.

This prevents unnecessary explanation and keeps output clean.

4️) Steps Performed
Step 1: Model Loading

The model is accessed using:

from huggingface_hub import InferenceClient

The client connects to:

Mistral-7B-Instruct-v0.2 via Hugging Face API.

Authentication is done using:

HF_TOKEN = os.getenv("HF_TOKEN")
Step 2: Prompt Creation

BMI is calculated using:
BMI= weight/(height/100)^2

BMI category is determined

Equipment list formatted

Prompt dynamically generated using f-string

Step 3: Inference Testing

The model is queried using:

response = client.chat_completion(
    messages=[
        {"role": "system", "content": "..."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=600,
    temperature=0.7
)

Temperature = 0.7 ensures:

Balanced creativity

Structured output

Reduced randomness

Step 4: Streamlit Integration

Landing Page

Profile Input Page

Result Page (5-Day Plan)

Session state used for navigation

Background styling applied

5️)  Sample Generated Output
Example Input:

Age: 25

BMI: 27.3 (Overweight)

Goal: Weight Loss

Fitness Level: Beginner

Equipment: Dumbbells

Example Generated Output:
Day 1 – Upper Body

1. Dumbbell Chest Press
   Sets: 3
   Reps: 12
   Rest: 60 seconds

2. Dumbbell Shoulder Press
   Sets: 3
   Reps: 10
   Rest: 60 seconds

3. Dumbbell Rows
   Sets: 3
   Reps: 12
   Rest: 60 seconds

4. Modified Push-ups
   Sets: 3
   Reps: 8–10
   Rest: 45 seconds

The model properly:

Avoided high-impact exercises

Maintained moderate intensity

Structured the output clearly

6️) Hugging Face Space Deployment Link

https://huggingface.co/spaces/ArumugaSelvi/FitPlan-AI-Milestone2
Streamlit app

Mistral API integration

🔗 Deployment Link:
