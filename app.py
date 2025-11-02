import streamlit as st
import pyrebase
import json

# --- LOAD FIREBASE CONFIG ---
with open("firebase_config.json") as f:
    firebase_config = json.load(f)

# --- INITIALIZE FIREBASE ---
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

# --- APP HEADER ---
st.set_page_config(page_title="Gloval Talent", page_icon="🌍", layout="wide")

st.image("thumbnail.png", use_container_width=True)
st.title("🌍 Welcome to Gloval Talent")
st.write("Share your creativity and connect with global opportunities!")

# --- SIDEBAR AUTHENTICATION ---
st.sidebar.title("🔐 User Authentication")
menu = st.sidebar.selectbox("Choose Action", ["Login", "Signup"])

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

# --- SIGNUP ---
if menu == "Signup":
    if st.sidebar.button("Create Account"):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.sidebar.success("✅ Account created successfully! Please login now.")
        except Exception as e:
            st.sidebar.error(f"❌ Error: {e}")

# --- LOGIN ---
elif menu == "Login":
    if st.sidebar.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state["user"] = email
            st.sidebar.success(f"Welcome {email} 👋")
        except Exception as e:
            st.sidebar.error(f"❌ Login failed: {e}")

# --- MAIN APP (AFTER LOGIN) ---
if "user" in st.session_state:
    st.success(f"🎉 Logged in as {st.session_state['user']}")

    st.subheader("🧠 Post Your Talent")
    skill = st.text_input("Skill Title:")
    desc = st.text_area("Describe your skill or project:")
    uploaded_file = st.file_uploader("Upload an image or video:", type=["jpg", "jpeg", "png", "mp4", "mov"])

    if uploaded_file:
        # Save file to Firebase Storage
        path = f"uploads/{st.session_state['user']}/{uploaded_file.name}"
        storage.child(path).put(uploaded_file)
        file_url = storage.child(path).get_url(None)
        st.success("✅ File uploaded successfully!")

        if uploaded_file.type.startswith("image"):
            st.image(file_url)
        elif uploaded_file.type.startswith("video"):
            st.video(file_url)

    if st.button("🚀 Post Talent"):
        if skill and desc:
            post_data = {
                "user": st.session_state["user"],
                "skill": skill,
                "desc": desc,
                "file_url": file_url if uploaded_file else ""
            }
            db.child("posts").push(post_data)
            st.success("✨ Talent posted successfully!")
        else:
            st.error("Please fill in all fields before posting.")
