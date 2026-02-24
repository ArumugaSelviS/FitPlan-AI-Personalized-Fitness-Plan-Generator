import streamlit as st
from model_api import query_model
from prompt_builder import build_prompt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="FitPlan AI", page_icon="💪", layout="centered")

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

# ---------------- LANDING PAGE ----------------
if st.session_state.page == "landing":

    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-image: url("https://images.unsplash.com/photo-1483721310020-03333e577078");
            background-size: cover;
            background-position: center;
        }
        .center-box {
            text-align:center;
            margin-top:200px;
            font-size:48px;
            font-weight:bold;
            color:black;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="center-box">💪 Welcome to FitPlan AI</div>', unsafe_allow_html=True)

    if st.button("🚀 Get Started"):
        st.session_state.page = "main"
        st.rerun()

# ---------------- MAIN PAGE (PROFILE FORM) ----------------
elif st.session_state.page == "main":

    st.title("💪 FitPlan AI")

    # ---------------- INPUTS ----------------
    name = st.text_input("Name *")
    age = st.number_input("Age *", min_value=10, max_value=100, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    height_cm = st.number_input("Height (cm) *", min_value=0.0)
    weight_kg = st.number_input("Weight (kg) *", min_value=0.0)

    goal = st.selectbox(
        "Fitness Goal",
        ["Build Muscle", "Weight Loss", "Strength Gain", "Abs Building", "Flexible"]
    )

    equipment = st.multiselect(
        "Equipment",
        ["Dumbbells", "Resistance Band", "Yoga Mat", "No Equipment"]
    )

    fitness_level = st.radio(
        "Fitness Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    # ---------------- SUBMIT PROFILE ----------------
    if st.button("Submit Profile"):

        # ----------- VALIDATION -----------
        if not name:
            st.error("Enter your name.")
        elif age <= 0:
            st.error("Enter valid age.")
        elif height_cm <= 0 or weight_kg <= 0:
            st.error("Enter valid height & weight.")
        elif not equipment:
            st.error("Select equipment.")
        else:
            # ----------- BUILD PROMPT -----------
            prompt, bmi, bmi_status = build_prompt(
                name,
                age,
                gender,
                height_cm,
                weight_kg,
                goal,
                fitness_level,
                equipment
            )

            # ----------- CALL MODEL API -----------
            with st.spinner("Generating Workout Plan..."):
                result = query_model(prompt)

            # ----------- STORE IN SESSION STATE -----------
            st.session_state.workout_plan = result
            st.session_state.bmi = bmi
            st.session_state.bmi_status = bmi_status

            # ----------- REDIRECT TO RESULT PAGE -----------
            st.session_state.page = "result"
            st.rerun()

# ---------------- RESULT PAGE ----------------
elif st.session_state.page == "result":

    st.title("🏋️ Your 5-Day Workout Plan")

    if "workout_plan" in st.session_state:
        st.markdown(st.session_state.workout_plan)
        st.info(f"BMI: {st.session_state.bmi:.2f} ({st.session_state.bmi_status})")
    else:
        st.warning("No workout plan found. Please submit your profile again.")

    if st.button("🔙 Back to Profile"):
        st.session_state.page = "main"
        st.rerun()
