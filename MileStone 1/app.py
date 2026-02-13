import streamlit as st
import matplotlib.pyplot as plt
st.set_page_config(page_title="FitPlan AI", page_icon="💪", layout="centered")
if "page" not in st.session_state:
    st.session_state.page = "landing"
if st.session_state.page == "landing":

    landing_style = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1483721310020-03333e577078");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    .center-box {
        text-align: center;
        margin-top: 220px;
        color: black;
        font-size: 48px;
        font-weight: bold;
    }
    </style>
    """
    st.markdown(landing_style, unsafe_allow_html=True)

    st.markdown('<div class="center-box">💪 Welcome to FitPlan AI</div>', unsafe_allow_html=True)
    st.write("")
    st.write("")

    if st.button("🚀 Get Started"):
        st.session_state.page = "main"
        st.rerun()
elif st.session_state.page == "main":

    page_style = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1558611848-73f7eb4001a1");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        padding-top: 40px;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
        height: 20px;
    }

    .main-title {
        color: white;
        text-align: center;
        font-size: 52px;
        font-weight: 800;
        margin-top: 20px;
    }

    .sub-title {
        color: #e6e6e6;
        text-align: center;
        font-size: 22px;
    }

    .block-container {
        background-color: rgba(0, 0, 0, 0.55);
        padding: 2rem;
        border-radius: 18px;
        margin-top: 20px;
    }
    </style>
    """
    st.markdown(page_style, unsafe_allow_html=True)
    st.sidebar.title("🏋 FitPlan AI")

    st.sidebar.markdown("### About")
    st.sidebar.write(
        "FitPlan AI helps users understand their **Body Mass Index (BMI)** "
        "and will later generate personalized workout plans."
    )

    st.sidebar.markdown("### BMI Categories")
    st.sidebar.write("""
    - Underweight < 18.5  
    - Normal 18.5 – 24.9  
    - Overweight 25 – 29.9  
    - Obese ≥ 30
    """)

    st.sidebar.markdown("### Tips")
    st.sidebar.write("""
    - Stay hydrated 💧  
    - Exercise regularly 🏃  
    - Maintain balanced diet 🥗
    """)
    st.markdown('<p class="main-title">💪 FitPlan AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Personalized Fitness Plan Generator</p>', unsafe_allow_html=True)
    st.markdown("---")
    name = st.text_input("Name *")
    height_cm = st.number_input("Height (cm) *", min_value=0.0, step=0.1)
    weight_kg = st.number_input("Weight (kg) *", min_value=0.0, step=0.1)

    goal = st.selectbox("Fitness Goal",
        ["Build Muscle", "Weight Loss", "Strength Gain", "Abs Building", "Flexible"])

    equipment = st.multiselect("Equipment",
        ["Dumbbells", "Resistance Band", "Yoga Mat", "No Equipment"])

    level = st.radio("Fitness Level",
        ["Beginner", "Intermediate", "Advanced"])

    st.markdown("---")
    def calculate_bmi(h, w):
        m = h / 100
        return round(w / (m ** 2), 2)

    def bmi_category(b):
        if b < 18.5: return "Underweight"
        elif b < 25: return "Normal"
        elif b < 30: return "Overweight"
        else: return "Obese"

    def bmi_plot(user_bmi):
        categories = ["Under", "Normal", "Over", "Obese"]
        ranges = [18.5, 25, 30, 35]

        plt.figure()
        plt.bar(categories, ranges)
        plt.axhline(user_bmi)
        plt.title("BMI Analytics")
        plt.ylabel("BMI Value")
        st.pyplot(plt)
    col1, col2 = st.columns(2)

    with col1:
        calc_btn = st.button("Generate BMI")

    with col2:
        analytics_btn = st.button("Show Analytics")
    if calc_btn:
        if name.strip() == "" or height_cm <= 0 or weight_kg <= 0:
            st.error("Enter valid details.")
        else:
            bmi_val = calculate_bmi(height_cm, weight_kg)
            cat = bmi_category(bmi_val)
            st.session_state["bmi"] = bmi_val

            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ff512f, #dd2476);
            padding:22px;
            border-radius:18px;
            color:white;
            text-align:center;
            font-size:24px;'>
            Hello <b>{name}</b><br>
            BMI: <b>{bmi_val}</b><br>
            Category: <b>{cat}</b>
            </div>
            """, unsafe_allow_html=True)

    if analytics_btn:
        if "bmi" in st.session_state:
            bmi_plot(st.session_state["bmi"])
        else:
            st.warning("Please generate BMI first.")
