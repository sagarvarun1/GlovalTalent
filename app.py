import streamlit as st
import sqlite3
from datetime import datetime

# --- DATABASE SETUP ---
conn = sqlite3.connect('talent.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        skill TEXT,
        description TEXT,
        rating INTEGER,
        date TEXT
    )
''')
conn.commit()

# --- APP TITLE ---
st.set_page_config(page_title="Gloval Talent 🌍", page_icon="🌟")
st.title("🌍 Gloval Talent")
st.subheader("Connecting Skills, Creating Opportunities — Across the Globe!")

# --- SIDEBAR MENU ---
menu = ["Home", "Post Your Talent", "Rate Talents", "Leaderboard"]
choice = st.sidebar.selectbox("Navigate", menu)

# --- HOME PAGE ---
if choice == "Home":
    st.write("Welcome to **Gloval Talent** — a platform to showcase your skills and creativity!")
    st.image("thumbnail.png", caption="Gloval Talent - Global Skills Platform", use_container_width=True)

# --- POST TALENT PAGE ---
elif choice == "Post Your Talent":
    st.header("🧠 Share Your Talent")
    username = st.text_input("Enter your name:")
    skill = st.text_input("Skill Title:")
    desc = st.text_area("Describe your skill or project:")
        # --- FILE UPLOAD SECTION ---
    uploaded_file = st.file_uploader(
        "Upload an Image or Video of your Talent:",
        type=["jpg", "jpeg", "png", "mp4", "mov"],
        help="Upload a photo or short video (Max size: 200MB)"
    )

    # --- SHOW PREVIEW IF FILE UPLOADED ---
    if uploaded_file is not None:
        file_ext = uploaded_file.name.split(".")[-1].lower()
        if file_ext in ["jpg", "jpeg", "png"]:
            st.image(uploaded_file, caption="Your uploaded image", use_container_width=True)
        elif file_ext in ["mp4", "mov"]:
            st.video(uploaded_file)
        else:
            st.warning("⚠️ Please upload only image or video files!")

    # --- SUBMIT BUTTON ---
    if st.button("Submit Talent"):
        if username.strip() and skill.strip() and desc.strip():
            st.success(f"✅ Thanks {username}! Your talent '{skill}' has been posted successfully.")
            if uploaded_file is not None:
                st.info("Your photo/video preview is shown above (temporary).")
        else:
            st.error("Please fill in all fields before submitting.")

    
    if st.button("Post"):
        if username and skill:
            c.execute("INSERT INTO posts (username, skill, description, rating, date) VALUES (?, ?, ?, ?, ?)", 
                      (username, skill, desc, 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            st.success("✅ Your skill has been posted successfully!")
        else:
            st.warning("Please enter both name and skill title!")

# --- RATE TALENTS PAGE ---
elif choice == "Rate Talents":
    st.header("⭐ Rate Talents")
    c.execute("SELECT * FROM posts")
    data = c.fetchall()
    if data:
        for row in data:
            st.markdown(f"**{row[2]}** by *{row[1]}*")
            st.write(row[3])
            rating = st.slider(f"Rate {row[1]}'s talent:", 0, 5, key=row[0])
            if st.button(f"Submit Rating {row[0]}", key=f"btn_{row[0]}"):
                c.execute("UPDATE posts SET rating = ? WHERE id = ?", (rating, row[0]))
                conn.commit()
                st.success("⭐ Rating submitted!")
    else:
        st.info("No posts yet! Be the first to share your skill.")

# --- LEADERBOARD PAGE ---
elif choice == "Leaderboard":
    st.header("🏆 Top Rated Talents")
    c.execute("SELECT username, skill, rating FROM posts ORDER BY rating DESC LIMIT 5")
    top = c.fetchall()
    if top:
        for row in top:
            st.markdown(f"**{row[1]}** by *{row[0]}* — ⭐ {row[2]}")
    else:
        st.info("No ratings yet! Start posting and rating talents.")


