import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Bereavement Notification", layout="centered")
st.title("Bank Bereavement Support")

st.markdown("We are here to help. Please notify us of a bereavement or ask any question using chatbox below")

if "show_form" not in st.session_state:
    st.session_state.show_form = False

if not st.session_state.show_form:
    if st.button("Notify a bereavement"):
        st.session_state.show_form = True

if st.session_state.show_form:
    st.markdown("**Bereavement Notification Form**")

    with st.form("bereavement_form"):
        deceased_name = st.text_input("Full Name of the deceased")
        date_of_death = st.date_input("Date of Death")
        account_number = st.text_input("Account Number")
        relation = st.selectbox("Your relationship to deceased", ["Spouse", "Child", "Parent", "Other"])
        contact_phone = st.text_input("Your Phone Number")
        uploaded_file = st.file_uploader("Upload death certificate")
        
        submitted = st.form_submit_button("Submit Notification")

    if submitted:
        st.success("Thank You your Notification has been received")
        st.write("Our support team will contact you, expect a response in 3 business days")

# Chatbot
st.markdown("----")
st.header("Chat with our VCare")

faq_knowledge = {
    "how long does it take": "3-5 business days to process a notification.",
    "what documents are needed": "Death Certificate and proof of identity",
    "can I access the account": "Only after verification is completed.",
    "how to contact": "you can reach our helpline at 18888 for any urgent support"
}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_faq_response(user_input):
    input_lower = user_input.lower()
    for keyword, answer in faq_knowledge.items():
        if keyword in input_lower:
            return answer
    return "I am sorry, don't have an answer for that. Please call our helpline at 12222"

user_query = st.text_input("Ask a question about bereavement support", key="chat_input")

if user_query:
    response = get_faq_response(user_query)
    st.session_state.chat_history.append(("You", user_query))
    st.session_state.chat_history.append(("Bot", response))

for speaker, msg in st.session_state.chat_history:
    with st.chat_message("assistant" if speaker == "Bot" else "user"):
        st.write(msg)