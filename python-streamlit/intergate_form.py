import streamlit as st
import pandas as pd
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# ---------------- Page Setup ----------------
st.set_page_config(page_title="Bereavement Support", layout="centered")
st.subheader("Team Empathy Engine")

# ---------------- Constants ----------------
DATA_PATH = "./bereavement_train.csv"
CHAT_LOGS_DIR = "chat_logs"

# ---------------- Load Model ----------------
@st.cache_resource
def load_model():
    df = pd.read_csv(DATA_PATH)
    X = df['Query'].str.lower().str.strip()
    y = df['Response']

    vec = TfidfVectorizer(stop_words='english', max_features=1000, ngram_range=(1, 2))
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

# ---------------- Session Initialization ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "chat_log_df" not in st.session_state:
    st.session_state.chat_log_df = None

# ---------------- UI Flow Control ----------------
st.title("Bereavement Support Assistant 🤖")

# Initial Options
if not st.session_state.show_form and not st.session_state.form_submitted and not st.session_state.start_chat:
    st.write("What can I help with today?")
    col1, col2 = st.columns(2)
    if col1.button("Notify us of a death"):
        st.session_state.show_form = True
    if col2.button("If already notified and have any queries?"):
        st.session_state.start_chat = True


# ---------------- Form Section ----------------
if st.session_state.show_form and not st.session_state.form_submitted:
    st.subheader("Bereavement Notification Form")
    with st.form("bereavement_form"):
        deceased_name = st.text_input("Full Name of the deceased")
        date_of_death = st.date_input("Date of Death")
        account_number = st.text_input("Account Number")
        relation = st.selectbox("Your relationship to deceased", ["Spouse", "Child", "Parent", "Other"])
        contact_phone = st.text_input("Your Phone Number")
        uploaded_file = st.file_uploader("Upload death certificate")

        submitted = st.form_submit_button("Submit Notification")

    if submitted:
        st.session_state.form_submitted = True
        st.session_state.show_form = False

# Handle post-submission display and navigation
if st.session_state.form_submitted:
    st.success("✅ Thank you! Your Notification has been received.")
    st.write("Our support team will contact you within 3 business days.")
    st.markdown("### Submission Summary:")
    # Add your actual submission data handling here
    
    if st.button("Back to chatbot"):
        # Reset all relevant states
        st.session_state.start_chat = True
        st.session_state.form_submitted = False
        st.session_state.show_form = False
        # Optional: Clear chat history if needed
        st.session_state.chat_history = []
        st.rerun()

# ---------------- Chatbot Section ----------------
if st.session_state.start_chat:
    st.markdown("---")
    st.subheader("Chat with our Assistant")

    chat_container = st.container()

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask a question about bereavement support:", key="user_input")
        col1, col2 = st.columns([1, 1])
        with col1:
            submitted = st.form_submit_button("Send")
        with col2:
            end_chat = st.form_submit_button("End Chat")

    if submitted and user_input.strip():
        st.session_state.chat_history.append({
            "sender": "You",
            "message": user_input,
            "time": datetime.now().strftime("%H:%M:%S")
        })

        bot_response = get_bot_response(user_input)
        st.session_state.chat_history.append({
            "sender": "Bot",
            "message": bot_response,
            "time": datetime.now().strftime("%H:%M:%S")
        })

    if end_chat:
        if st.session_state.chat_history:
            # Convert chat history to DataFrame
            chat_df = pd.DataFrame(st.session_state.chat_history)
            chat_df.rename(columns={
                'sender': 'Sender',
                'message': 'Message',
                'time': 'Time'
            }, inplace=True)
            
            # Save to CSV
            os.makedirs(CHAT_LOGS_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"{CHAT_LOGS_DIR}/chatlog_{timestamp}.csv"
            chat_df.to_csv(filepath, index=False)
            
            # Store for display and download
            st.session_state.chat_log_df = chat_df
            st.session_state.chat_history = []
            
            st.success(f"Chat ended. Log saved to '{filepath}'.")
        else:
            st.info("No chat to save.")

    # Chat display
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

# ---------------- Chat Log Display & Download ----------------
if st.session_state.chat_log_df is not None:
    st.markdown("---")
    st.subheader("Chat History")
    
    # Display DataFrame
    st.dataframe(st.session_state.chat_log_df)
    
    # Download button
    csv_data = st.session_state.chat_log_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Chat History as CSV",
        data=csv_data,
        file_name=f"bereavement_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    # Clear log display
    if st.button("Close"):
        st.session_state.chat_log_df = None