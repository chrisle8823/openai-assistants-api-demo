import time
import streamlit as st
from openai import OpenAI

st.title("OpenAI Assistant Query")
st.write("Ask a question to the assistant and get a response.")

# Enter your Assistant ID here.
ASSISTANT_ID = "asst_CtJTbk0SOObS3RR5spbRR8Mv"

# Ensure your API key is set as an environment variable.
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

query = st.text_input("Enter your query:", "What's the most livable city in the world?")

if st.button("Submit"):
    with st.spinner("Creating thread..."):
        # Create a thread with a message.
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": query,
                }
            ]
        )

    with st.spinner("Submitting thread..."):
        # Submit the thread to the assistant (as a new run).
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
        st.write(f"👉 Run Created: {run.id}")

    with st.spinner("Waiting for run to complete..."):
        # Wait for run to complete.
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            st.write(f"🏃 Run Status: {run.status}")
            time.sleep(1)
        else:
            st.write(f"🏁 Run Completed!")

    with st.spinner("Fetching the latest message..."):
        # Get the latest message from the thread.
        message_response = client.beta.threads.messages.list(thread_id=thread.id)
        messages = message_response.data

        # Print the latest message.
        if messages:
            latest_message = messages[0]
            st.success(f"💬 Response: {latest_message.content[0].text.value}")
        else:
            st.error("No messages found.")
