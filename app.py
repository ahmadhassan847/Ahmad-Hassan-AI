import streamlit as st
import google.generativeai as genai

# Basic web page configuration
st.set_page_config(page_title="Ahmad Hassan AI", page_icon="🤖", layout="centered")

# Styling (CSS) to make the interface beautiful and user-friendly
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    h1 { color: #1E3A8A; text-align: center; font-family: 'Arial', sans-serif; }
    p { text-align: center; color: #4B5563; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Ahmad Hassan AI")
st.write("Your personal AI assistant: Ready to help with web design, app design, coding, post design, and graphic sketches.")

# Specific system instructions provided for the AI
SYSTEM_INSTRUCTION = """
You are the user's personal AI, and your name is "Ahmad Hassan AI". 
You can create web designs, app designs, generate code, design social media posts, and even create visual/graphic sketches for the user. You are capable of handling all these tasks.
You always provide detailed answers in a highly helpful, professional, and friendly manner, using clear English.
"""

# Securely retrieving the API Key from the live server secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    api_key = None

if api_key:
    genai.configure(api_key=api_key)
    
    # Setting up the Gemini model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION
    )

    # Session state to store and remember chat history (conversation records)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Displaying previous chat history on the screen
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Taking new message or request from the user
    if prompt := st.chat_input("Ask Ahmad Hassan AI anything or request a design..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generating the AI's response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                # Passing the conversation history so the model maintains context
                chat = model.start_chat(history=[
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ])
                response = chat.send_message(prompt)
                full_response = response.text
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                message_placeholder.markdown("Sorry, a technical error occurred. Please try again.")
else:
    st.error("Please set up your GEMINI_API_KEY in the Streamlit Advanced Settings first.")
