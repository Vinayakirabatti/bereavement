import streamlit as st

st.set_page_config(page_title="Bereavement Chatbot", layout="centered")
st.title("🤖 Bereavement Chatbot")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = "start"

st.write("Please be assured any joint accounts will continue to operate.")

# Step 1: Main options
if st.session_state.step == "start":
    st.write("What can I help with today?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Notify us of a death"):
            st.session_state.step = "notify_death"
    with col2:
        if st.button("An existing case"):
            st.session_state.step = "existing_case"

# Step 2: Notify us of a death
elif st.session_state.step == "notify_death":
    st.write("Thank you for notifying us. You can either:")

    st.subheader("Option 1: Complete the Online Form")
    st.write("The form is quick and simple to fill out. You don't need to visit one of our branches.")
    st.link_button("Bereavement (Online Form)", "https://example.com/bereavement-form")

    st.subheader("Option 2: Upload Documents")
    st.markdown("""
    Please upload any of the following documents you have:
    - Death certificate  
    - Will/Codicil (if applicable)  
    - Grant of Representation (England & Wales)  
    - Certificate of Confirmation (Scotland)  
    - Account number(s)
    """)
    uploaded_files = st.file_uploader("Upload documents", type=["pdf", "jpg", "png", "docx"], accept_multiple_files=True)

    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) uploaded.")
        for file in uploaded_files:
            st.write(f"📄 {file.name}")

    st.write("If the customer had accounts with other banks, you can use the free Death Notification Service:")
    st.link_button("Death Notification Service", "https://www.deathnotificationservice.co.uk/")

    st.write("For more information, visit our FAQ page:")
    st.link_button("FAQ Page", "https://example.com/faq")

    if st.button("⬅️ Back"):
        st.session_state.step = "start"

# Step 3: Existing case
elif st.session_state.step == "existing_case":
    st.write("What would you like to know?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("What happens after?"):
            st.session_state.step = "after"
    with col2:
        if st.button("What documents do I need?"):
            st.session_state.step = "documents"

    if st.button("⬅️ Back"):
        st.session_state.step = "start"

# Step 3a: What happens after
elif st.session_state.step == "after":
    st.write("We’ll protect all accounts held in the customer's sole name so no payments can come in or go out.")
    st.write("If it's a joint account, the account name will be updated to your name and you can continue using it as normal.")
    st.write("You may receive a text message about an address change—this is just a record update and no action is needed.")

    if st.button("⬅️ Back"):
        st.session_state.step = "existing_case"

# Step 3b: What documents do I need
elif st.session_state.step == "documents":
    st.write("We'll let you know what documents we need in the Condolence Letter.")
    st.write("If you don't have an account with us, we'll need to see your photo ID and proof of address.")
    
    st.write("Would you like help with something else?")
    if st.button("Funeral bills"):
        st.write("You can send us the funeral invoice. If there are enough funds, we’ll pay it directly from the account.")

    if st.button("⬅️ Back"):
        st.session_state.step = "existing_case"

# Reset
st.divider()
if st.button("🔁 Start Over"):
    st.session_state.step = "start"
