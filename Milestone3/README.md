🏋️ FitPlan AI – Personalized Workout Generator
📌 Project Overview

FitPlan AI is an AI-powered web application that generates personalized workout plans based on user fitness data.

The system collects user information such as:

Name

Age

Gender

Height

Weight

Fitness goal

Fitness level

Available equipment

Using this information, the system calculates BMI and generates a structured 5-day workout plan using Google Gemini AI.

The application also includes secure authentication features such as:

Email OTP verification

Login system

SQLite database storage

JWT token authentication

🎯 Objective of the Project

The objective of this project is to develop an AI-based fitness assistant that provides customized workout plans tailored to each user's body metrics and fitness goals.

The system aims to:

Generate safe and personalized workouts

Adjust exercise intensity based on BMI and fitness level

Provide structured weekly workout routines

Demonstrate integration of AI models with a real-world application

This project combines Artificial Intelligence, Web Development, and Database Systems.

🤖 AI Model Used

The model used in this project is:

Google Gemini (Gemini API)

Accessed through:

Google AI Studio / Gemini API

The model is called using an API key inside the Python application.

Why Gemini?

Gemini was selected because it provides:

Strong natural language understanding

High-quality structured text generation

Fast API response

Easy integration with Python applications

Gemini is used to generate personalized workout plans based on user input data.

🧠 Prompt Design

The prompt sent to the AI model is carefully designed to ensure structured and safe workout generation.

1️⃣ Role Definition

The AI model is instructed to act as:

You are a certified professional fitness trainer.

This ensures the response is professional and structured.

2️⃣ User Profile Injection

User information is dynamically inserted into the prompt.

Example:

User Profile:
Name: Arumugaselvi
Age: 22
BMI: 23.4 (Normal Weight)
Goal: Build Muscle
Fitness Level: Beginner
Equipment: Dumbbells

This allows the AI to generate fully personalized workout routines.

3️⃣ Output Structure

The AI is instructed to generate:

5-Day workout plan

4–6 exercises per day

Each exercise includes:

Exercise name

Number of sets

Repetitions

Rest time

4️⃣ Safety Instructions

The prompt ensures the model:

Avoids dangerous exercises for beginners

Adjusts intensity based on BMI

Provides safe training routines

⚙️ System Architecture

The system contains the following main components.

1️⃣ Frontend – Streamlit

The user interface is built using Streamlit.

Features include:

Interactive fitness input form

Multi-step user data collection

Dashboard view for workout generation

Custom CSS styling for a modern UI

2️⃣ Authentication System

The system includes a secure login and signup system.

Features:

User signup with email verification

OTP verification using SMTP

Login authentication

JWT token-based session management

3️⃣ Database – SQLite

User information is stored in a SQLite database.

The database stores:

Field	Description
id	User ID
name	User name
email	Email address
password	Password
created_at	Account creation timestamp
4️⃣ Email OTP Verification

During signup:

User enters email address

System sends OTP to email

User enters OTP in the application

Account is created after verification

This prevents fake registrations.

5️⃣ AI Workout Generator

After login, the user enters fitness details.

The system:

1️⃣ Collects fitness data
2️⃣ Calculates BMI
3️⃣ Builds a prompt dynamically
4️⃣ Sends prompt to Gemini API
5️⃣ Receives a generated workout plan
6️⃣ Displays the result on the dashboard

📊 BMI Calculation

BMI is calculated using the formula:

𝐵
𝑀
𝐼
=
𝑤
𝑒
𝑖
𝑔
ℎ
𝑡
(
ℎ
𝑒
𝑖
𝑔
ℎ
𝑡
/
100
)
2
BMI=
(height/100)
2
weight
	​


Example:

Height = 170 cm
Weight = 70 kg

BMI = 70 / (1.7²) = 24.22

BMI category is determined as:

BMI Range	Category
< 18.5	Underweight
18.5 – 24.9	Normal
25 – 29.9	Overweight
≥ 30	Obese

This helps adjust workout difficulty.

🖥️ Application Workflow
Step 1 – Signup Page

User enters:

Name

Email

Password

OTP verification

User data is stored in SQLite database.

Step 2 – Login Page

User logs in using:

Email

Password

A JWT token is generated for secure session management.

Step 3 – Dashboard

User enters fitness information in three steps:

1️⃣ Personal Details
2️⃣ Body Metrics
3️⃣ Fitness Goals

Step 4 – Workout Generation

The system:

Calculates BMI

Sends prompt to Gemini AI

Generates a personalized 5-day workout plan

📋 Sample Generated Output

Example Input:

Age: 25
BMI: 27.3 (Overweight)
Goal: Weight Loss
Fitness Level: Beginner
Equipment: Dumbbells

Example Output:

Day 1 – Upper Body

Dumbbell Chest Press
Sets: 3
Reps: 12
Rest: 60 seconds

Dumbbell Shoulder Press
Sets: 3
Reps: 10
Rest: 60 seconds

Dumbbell Rows
Sets: 3
Reps: 12
Rest: 60 seconds

Modified Push-ups
Sets: 3
Reps: 8–10
Rest: 45 seconds

The AI generates a structured, safe, and personalized workout routine.

🛠️ Technologies Used
Technology	Purpose
Python	Programming language
Streamlit	Web application UI
SQLite	Database
Google Gemini API	AI workout generation
SMTP	Email OTP verification
JWT	Secure authentication
Google Colab	Development environment
