import streamlit as st
import requests

st.title("Financial Chatbot")

BACKEND_URL = "http://localhost:8000"

if "token" not in st.session_state:
    st.session_state.token = None

username = st.text_input("Username", "demo")
password = st.text_input("Password", "demo123", type="password")

if st.button("Login"):
    try:
        response = requests.post(f"{BACKEND_URL}/token", data={"username": username, "password": password})
        if response.status_code == 200:
            st.session_state.token = response.json()["access_token"]
            st.success("Logged in successfully!")
        else:
            st.error("Login failed. Please try again.")
    except:
        st.error("Cannot connect to backend. Please check if backend is running.")

if st.session_state.token:
    question = st.text_area("Ask financial question", height=100)
    if st.button("Submit"):
        try:
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            response = requests.post(f"{BACKEND_URL}/chat", json={"question": question}, headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.success(f"**Source**: {data.get('source', 'Unknown')}")
                st.write(data.get("answer", "No answer"))
            else:
                st.error("Error getting answer. Please try again.")
        except:
            st.error("Connection error. Please check backend.")
