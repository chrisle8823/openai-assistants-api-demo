from openai import OpenAI
import streamlit as st
import time

# Set page configuration
st.set_page_config(
    page_title="Assistant Chatbot",
    page_icon=":robot:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure responsive layout for mobile devices
st.markdown("""
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
""", unsafe_allow_html=True)

# Page title
st.title("Welcome to the AI Assistant Chatbot! Ask me anything, and I'll try my best to assist you.")

# Apply custom CSS for better mobile experience
st.markdown("""
<style>
@media (max-width: 768px) {
    .css-18e3th9 {
        padding: 0.5rem !important;
    }
    .stButton>button {
        width: 100%;
        height: 3rem;
    }
}
</style>
""", unsafe_allow_html=True)

# OpenAI client setup
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new message
if prompt := st.chat_input("What's on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Create a thread with the user's message
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

        # Submit the thread to the assistant (as a new run)
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id="asst_CtJTbk0SOObS3RR5spbRR8Mv")
        
        # Wait for run to complete
        while run.status not in ["completed", "failed"]:
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            time.sleep(1)
        
        # Get the latest message from the thread
        message_response = client.beta.threads.messages.list(thread_id=thread.id)
        messages = message_response.data
        
        # Display the assistant's response
        if messages and "content" in messages[-1] and messages[-1]["content"]:
            latest_message = messages[-1]
            response_content = latest_message["content"][0]["text"]["value"]
            st.markdown(response_content)
            st.session_state.messages.append({"role": "assistant", "content": response_content})
        else:
            st.error("No messages found or message content is missing.")
