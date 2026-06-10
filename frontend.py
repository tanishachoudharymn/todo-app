import streamlit as st
import requests
from datetime import date

API = "http://localhost:5000"

st.set_page_config(page_title="My To-Do List", page_icon="✨")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
        min-height: 100vh;
    }
    .main .block-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 2rem;
        border: 1px solid rgba(255,255,255,0.3);
    }
    h1, h2, h3, p, label {
        color: white !important;
    }
    .stTextInput input {
        background: rgba(255,255,255,0.2) !important;
        border: 2px solid rgba(255,255,255,0.4) !important;
        border-radius: 10px !important;
        color: white !important;
        font-size: 16px !important;
    }
    .stButton button {
        background: linear-gradient(90deg, #a855f7, #ec4899) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        padding: 0.5rem 1rem !important;
        transition: transform 0.2s !important;
    }
    .stButton button:hover {
        transform: scale(1.05) !important;
    }
    .task-card {
        background: rgba(255,255,255,0.2);
        border-radius: 15px;
        padding: 15px 20px;
        margin: 10px 0;
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        font-size: 16px;
        font-weight: 500;
    }
    .completed-card {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 15px 20px;
        margin: 10px 0;
        border: 1px solid rgba(255,255,255,0.2);
        color: rgba(255,255,255,0.5);
        text-decoration: line-through;
        font-size: 16px;
    }
    .stAlert {
        background: rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    div[data-testid="stDateInput"] input {
        background: rgba(255,255,255,0.2) !important;
        border: 2px solid rgba(255,255,255,0.4) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✨ My To-Do List")

st.subheader("➕ Add a New Task")
col1, col2 = st.columns([3, 1])
new_task = col1.text_input("What do you need to do?")
due_date = col2.date_input("Due date", min_value=date.today())

if st.button("Add Task ✨"):
    if new_task:
        requests.post(
            f"{API}/tasks",
            json={"task": new_task, "due_date": str(due_date)}
        )
        st.success("✅ Task added!")
        st.rerun()

st.divider()

response = requests.get(f"{API}/tasks")
tasks = response.json()

pending = [t for t in tasks if not t["done"]]
completed = [t for t in tasks if t["done"]]

st.subheader(f"📋 Pending Tasks ({len(pending)})")

if not pending:
    st.info("No pending tasks! Great job! 🎉")

for t in pending:
    col1, col2, col3 = st.columns([3, 1, 1])
    col1.markdown(
        f"<div class='task-card'>• {t['task']}</div>",
        unsafe_allow_html=True
    )
    if t["due_date"]:
        today = str(date.today())
        if t["due_date"] < today:
            col1.error(f"⚠️ Overdue: {t['due_date']}")
        elif t["due_date"] == today:
            col1.warning("⏰ Due today!")
        else:
            col1.success(f"📅 Due: {t['due_date']}")
    if col2.button("✅ Done", key=f"done_{t['id']}"):
        requests.put(f"{API}/tasks/{t['id']}/toggle")
        st.rerun()
    if col3.button("🗑️ Delete", key=f"del_{t['id']}"):
        requests.delete(f"{API}/tasks/{t['id']}")
        st.rerun()

if completed:
    st.divider()
    st.subheader(f"✅ Completed ({len(completed)})")
    for t in completed:
        col1, col2 = st.columns([4, 1])
        col1.markdown(
            f"<div class='completed-card'>{t['task']}</div>",
            unsafe_allow_html=True
        )
        if col2.button("↩️ Undo", key=f"undo_{t['id']}"):
            requests.put(f"{API}/tasks/{t['id']}/toggle")
            st.rerun()