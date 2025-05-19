import streamlit as st
import pandas as pd
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# ---------------- Configuration ----------------
DATA_PATH = "./bereavement_train.csv"
CHAT_LOGS_DIR = "chat_logs"

# ---------------- Load Model ----------------
@st.cache_resource
def load_model():
    df = pd.read_csv(DATA_PATH)
    X = df['Query'].str.lower().str.strip()
    y = df['Response']
    
    vec = TfidfVectorizer(
        stop_words='english',
        max_features=1000,
        ngram_range=(1, 2)
    )
    X_vec = vec.fit_transform(X)
    
    model = NearestNeighbors(n_neighbors=3, metric='cosine').fit(X_vec)
    return vec, model, X, y

vec, model, X, y = load_model()

# ---------------- Bot Logic ----------------
def get_bot_response(user_query):
    query_vec = vec.transform([user_query.lower().strip()])
    distances, indices = model.kneighbors(query_vec)
    best_match_idx = indices[0][0]
    confidence = 1 - distances[0][0]
    if confidence >= 0.5:
        return y.iloc[best_match_idx]
    else:
        return "I'm sorry, I don't understand. Could you rephrase?"

# ---------------- Streamlit UI ----------------
st.title("Bereavement Support Chatbot 🤖")
st.write("How can I assist you today? Type your question below.")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat container
chat_container = st.container()

# Input form with clear-on-submit behavior
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:", key="user_input")
    col1, col2 = st.columns([1, 1])
    with col1:
        submitted = st.form_submit_button("Send")
    with col2:
        end_chat = st.form_submit_button("End Chat")

# Handle message submission
if submitted and user_input.strip():
    # Add user message
    st.session_state.chat_history.append({
        "sender": "You",
        "message": user_input,
        "time": datetime.now().strftime("%H:%M:%S")
    })
    
    # Get and add bot response
    bot_response = get_bot_response(user_input)
    st.session_state.chat_history.append({
        "sender": "Bot",
        "message": bot_response,
        "time": datetime.now().strftime("%H:%M:%S")
    })

# Handle End Chat
if end_chat:
    if st.session_state.chat_history:
        os.makedirs(CHAT_LOGS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"{CHAT_LOGS_DIR}/chatlog_{timestamp}.txt"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=== Chat Session ===\n")
            for msg in st.session_state.chat_history:
                f.write(f"[{msg['time']}] {msg['sender']}: {msg['message']}\n")
            f.write("=== End of Session ===\n")
        st.success(f"Chat ended. Saved to `{filepath}`.")
    else:
        st.info("No chat to save.")
    st.session_state.chat_history = []

# Display chat history
with chat_container:
    for msg in st.session_state.chat_history:
        cols = st.columns([1, 4, 1])
        if msg['sender'] == "You":
            cols[0].write("👤")
            cols[1].info(f"{msg['message']}")
            cols[2].caption(msg['time'])
        else:
            cols[0].write("🤖")
            cols[1].success(f"{msg['message']}")
            cols[2].caption(msg['time'])