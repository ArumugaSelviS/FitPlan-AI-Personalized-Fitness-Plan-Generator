%%writefile app.py
import streamlit as st
import smtplib
import random
import jwt
import sqlite3
from datetime import datetime, timedelta

try:
    from model_api import query_model
    from prompt_builder import build_prompt
except ImportError:
    def query_model(prompt): return "Sample Workout Plan Generated!"
    def build_prompt(*args): return "Prompt", 22.5, "Normal Weight"

# --- SQL DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('fitplan_users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def create_user(name, email, password):
    try:
        conn = sqlite3.connect('fitplan_users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False # Email already exists

def verify_user(email, password):
    conn = sqlite3.connect('fitplan_users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# Initialize the Database
init_db()

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="FitPlan AI", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALIZE SESSION STATE ---
form_defaults = {
    "user_name": "", "age": 0, "gender": "Male",
    "height": 0.0, "weight": 0.0,
    "goal": "Build Muscle", "equipment": ["None"],
    "fitness_level": "Beginner", "step": 1
}
for k, v in form_defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if "page" not in st.session_state: st.session_state.page = "signup"
if "otp" not in st.session_state: st.session_state.otp = None
if "email" not in st.session_state: st.session_state.email = None
if "token" not in st.session_state: st.session_state.token = None

# --- DYNAMIC BACKGROUND COLOR ---
if st.session_state.page in ["login", "signup"]:
    bg_color = "#FFFFFF"
else:
    bg_color = "#F4F7FA"

# --- CUSTOM CSS ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@300;400;600;700&display=swap');
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stApp {{ background-color: #E2E8F0 !important; }}
    .block-container {{
        padding: 0 !important;
        max-width: 950px !important;
        margin-top: 4vh !important;
        margin-bottom: 8vh !important;
        background: {bg_color} !important;
        border-radius: 15px !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.1) !important;
    }}
    .stMarkdown, p, label, div[data-testid="stMarkdownContainer"] {{
        color: #1E293B !important; font-family: 'Poppins', sans-serif;
    }}
    h1, h2, h3, h4 {{ color: #0F172A !important; font-family: 'Poppins', sans-serif; }}
    .left-panel {{
        background: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.85)),
                    url('https://images.unsplash.com/photo-1517836357463-d25dfeac3438?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80');
        background-size: cover; background-position: center;
        height: 100%; min-height: 600px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; text-align: center;
        padding: 40px; border-top-left-radius: 15px; border-bottom-left-radius: 15px;
    }}
    .left-panel .brand-title {{
        font-family: 'Great Vibes', cursive; font-size: 4.5rem; margin-bottom: 25px;
        color: #38BDF8 !important; -webkit-text-fill-color: #38BDF8 !important;
        text-shadow: 2px 4px 10px rgba(0,0,0,0.4); line-height: 1.2;
    }}
    .left-panel .quote-text {{
        font-family: 'Poppins', sans-serif; font-size: 1.1rem; font-weight: 300;
        line-height: 1.8; font-style: italic; color: #F8FAFC !important;
        -webkit-text-fill-color: #F8FAFC !important;
    }}
    .form-container {{ padding: 40px 50px; width: 100%; }}
    .sub-text {{ text-align: center; color: #64748B !important; font-size: 0.95rem; margin-bottom: 30px; }}
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important; box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }}
    input, div[data-baseweb="select"] {{
        color: #1E293B !important; -webkit-text-fill-color: #1E293B !important;
        font-family: 'Poppins', sans-serif; caret-color: #0284C7 !important;
    }}
    input::placeholder {{ color: #94A3B8 !important; -webkit-text-fill-color: #94A3B8 !important; opacity: 1 !important; }}
    div[data-baseweb="input"] > div:focus-within, div[data-baseweb="select"] > div:focus-within {{
        border-color: #0284C7 !important; box-shadow: 0 0 0 1px #0284C7 !important;
    }}
    span[data-baseweb="tag"] {{ background-color: #0284C7 !important; color: white !important; }}
    .form-container label {{ display: none !important; }}
    div.stButton > button {{ width: 100% !important; }}
    div.stButton > button[kind="primary"] {{
        background: #0284C7 !important; color: white !important; border: none !important;
        border-radius: 25px !important; padding: 12px 20px !important; font-weight: 600 !important;
        font-size: 15px !important; margin-top: 10px; box-shadow: 0 6px 15px rgba(2, 132, 199, 0.3) !important;
        transition: all 0.2s !important;
    }}
    div.stButton > button[kind="primary"]:hover {{ background: #0369A1 !important; transform: translateY(-2px); }}
    div.stButton > button[kind="secondary"] {{
        background-color: transparent !important; color: #0284C7 !important;
        border: 1px solid #0284C7 !important; border-radius: 25px !important;
        font-weight: 600 !important; margin-top: 10px;
    }}
    div.stButton > button[kind="secondary"]:hover {{ background-color: #E0F2FE !important; }}
    .or-divider {{ text-align: center; color: #94A3B8 !important; font-size: 13px; margin: 20px 0; }}
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def send_otp(email):
    otp = str(random.randint(100000, 999999))
    st.session_state.otp = otp
    st.session_state.email = email
    message = f"Subject:FitPlan AI OTP\n\nYour OTP is {otp}"
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("arumugaselvis61@gmail.com", "ihym srou otgr vtfm")
        server.sendmail("arumugaselvis61@gmail.com", email, message)
        server.quit()
        return True
    except Exception as e:
        st.error("Failed to send email.")
        return False

def generate_token(email):
    payload = {"email": email, "exp": datetime.utcnow() + timedelta(hours=2)}
    return jwt.encode(payload, "SECRET_KEY_HERE", algorithm="HS256")

def verify_token(token):
    try:
        data = jwt.decode(token, "SECRET_KEY_HERE", algorithms=["HS256"])
        return data["email"]
    except: return None

def render_left_panel():
    st.markdown("""
    <div class="left-panel">
        <div class="brand-title">FitPlan AI</div>
        <div class="quote-text">
            "Transform your body, elevate your mind.<br><br>
            Your journey to a stronger, healthier you begins the moment you decide to start."
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- APP LAYOUT ---
if st.session_state.page == "signup":
    col1, col2 = st.columns([1, 1], gap="small")
    with col1: render_left_panel()
    with col2:
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.markdown("<h2>Create Account</h2><div class='sub-text'>Join FitPlan to start your journey</div>", unsafe_allow_html=True)

        name = st.text_input("Name", placeholder="👤  Full Name")
        email = st.text_input("Email", placeholder="✉️  Email address")

        c1, c2 = st.columns([2, 1])
        with c1: otp_input = st.text_input("OTP", placeholder="🔢  OTP Code")
        with c2:
            st.write("<div style='margin-top:2px;'></div>", unsafe_allow_html=True)
            if st.button("Get OTP", type="secondary"):
                if send_otp(email): st.success("OTP Sent!")

        password = st.text_input("Password", type="password", placeholder="🗝️  Password")
        repeat_password = st.text_input("Repeat Password", type="password", placeholder="🗝️  Repeat Password")

        if st.button("SIGN UP", type="primary"):
            if not name or not email or not password:
                st.error("Please fill all details.")
            elif password != repeat_password:
                st.error("Passwords do not match!")
            elif otp_input != st.session_state.otp or not st.session_state.otp:
                st.error("Invalid OTP!")
            else:
                # INSERT USER INTO SQL DATABASE
                if create_user(name, email, password):
                    st.success("Account created successfully!")
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error("Account with this email already exists!")

        st.markdown("<div class='or-divider'>— OR —</div>", unsafe_allow_html=True)
        if st.button("Already have an account? Login Here", type="secondary"):
            st.session_state.page = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "login":
    col1, col2 = st.columns([1, 1], gap="small")
    with col1: render_left_panel()
    with col2:
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.markdown("<h2>Welcome Back</h2><div class='sub-text'>Login to your account</div>", unsafe_allow_html=True)

        email = st.text_input("Email", placeholder="✉️  Email address")
        password = st.text_input("Password", type="password", placeholder="🗝️  Password")

        st.write("<br>", unsafe_allow_html=True)
        if st.button("LOGIN", type="primary"):
            # CHECK SQL DATABASE FOR LOGIN
            if verify_user(email, password):
                st.session_state.token = generate_token(email)
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Invalid email or password")

        st.markdown("<div class='or-divider'>— OR —</div>", unsafe_allow_html=True)
        if st.button("Create new account", type="secondary"):
            st.session_state.page = "signup"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    email = verify_token(st.session_state.token)
    if not email:
        st.session_state.page = "login"
        st.rerun()

    st.markdown("<div style='padding: 40px 60px;'>", unsafe_allow_html=True)

    head_left, head_center, head_right = st.columns([1, 3, 1])
    with head_center:
        st.markdown("<h2 style='text-align: center; margin-bottom: 5px;'>🏋️ FitPlan Dashboard</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #64748B; margin-top: 0px;'>Logged in as: <b>{email}</b></p>", unsafe_allow_html=True)

    with head_right:
        st.write("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        if st.button("Logout", type="secondary"):
            st.session_state.token = None
            st.session_state.page = "login"
            st.session_state.step = 1
            st.rerun()

    st.markdown("---")
    st.progress(st.session_state.step * 0.25)
    st.write("<br>", unsafe_allow_html=True)

    _, center_form, _ = st.columns([1, 2, 1])
    with center_form:
        if st.session_state.step == 1:
            st.markdown("<h3 style='text-align: center;'>1️⃣ Personal Details</h3><br>", unsafe_allow_html=True)
            name_in = st.text_input("Full Name", value=st.session_state.user_name, placeholder="Enter your full name")
            age_in = st.number_input("Age", min_value=0, max_value=120, value=st.session_state.age)
            gender_in = st.selectbox("Gender",["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(st.session_state.gender))

            st.write("<br>", unsafe_allow_html=True)
            if st.button("Next ➡️", type="primary"):
                st.session_state.user_name = name_in
                st.session_state.age = age_in
                st.session_state.gender = gender_in
                st.session_state.step = 2
                st.rerun()

        elif st.session_state.step == 2:
            st.markdown("<h3 style='text-align: center;'>2️⃣ Body Metrics</h3><br>", unsafe_allow_html=True)
            height_in = st.number_input("Height (cm)", min_value=0.0, value=float(st.session_state.height), format="%.1f")
            weight_in = st.number_input("Weight (kg)", min_value=0.0, value=float(st.session_state.weight), format="%.1f")

            st.write("<br>", unsafe_allow_html=True)
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("⬅️ Back", type="secondary"):
                    st.session_state.height, st.session_state.weight = height_in, weight_in
                    st.session_state.step = 1
                    st.rerun()
            with btn_col2:
                if st.button("Next ➡️", type="primary"):
                    if height_in <= 0 or weight_in <= 0:
                        st.error("⚠️ Please enter a valid height and weight greater than 0.")
                    else:
                        st.session_state.height, st.session_state.weight = height_in, weight_in
                        st.session_state.step = 3
                        st.rerun()

        elif st.session_state.step == 3:
            st.markdown("<h3 style='text-align: center;'>3️⃣ Fitness Goals</h3><br>", unsafe_allow_html=True)
            goal_in = st.selectbox("Goal",["Build Muscle", "Weight Loss", "Strength Gain", "Abs"], index=["Build Muscle", "Weight Loss", "Strength Gain", "Abs"].index(st.session_state.goal))
            equip_in = st.multiselect("Equipment available", ["Dumbbells", "Resistance Band", "Yoga Mat", "None"], default=st.session_state.equipment)
            level_in = st.radio("Current Fitness Level",["Beginner", "Intermediate", "Advanced"], index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.fitness_level))

            st.write("<br>", unsafe_allow_html=True)
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("⬅️ Back", type="secondary"):
                    st.session_state.goal, st.session_state.equipment, st.session_state.fitness_level = goal_in, equip_in, level_in
                    st.session_state.step = 2
                    st.rerun()
            with btn_col2:
                if st.button("Generate FitPlan ✨", type="primary"):
                    st.session_state.goal, st.session_state.equipment, st.session_state.fitness_level = goal_in, equip_in, level_in
                    st.session_state.step = 4
                    st.rerun()

        elif st.session_state.step == 4:
            st.markdown("<h3 style='text-align: center;'>🎯 Your Custom FitPlan</h3><br>", unsafe_allow_html=True)

            prompt, bmi, status = build_prompt(
                st.session_state.user_name, st.session_state.age, st.session_state.gender,
                st.session_state.height, st.session_state.weight, st.session_state.goal,
                st.session_state.fitness_level, st.session_state.equipment
            )

            with st.spinner("Generating your personalized plan..."):
                result = query_model(prompt)

            st.success("Plan Generated Successfully!")
            st.info(f"Your BMI: **{bmi:.2f}** ({status})")
            st.write(result)

            st.write("<br>", unsafe_allow_html=True)
            if st.button("⬅️ Start Over", type="secondary"):
                st.session_state.age = 0
                st.session_state.height = 0.0
                st.session_state.weight = 0.0
                st.session_state.step = 1
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
