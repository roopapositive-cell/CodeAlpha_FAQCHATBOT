import streamlit as st  # Import Streamlit so we can build the web app UI

from chatbot import get_answer, load_faq  # Import the FAQ loader and answer generator from the chatbot helper file

st.set_page_config(page_title="AI FAQ Assistant", page_icon="💬", layout="wide")  # Configure the browser tab title, icon, and page layout

st.markdown(  # Render custom HTML/CSS to style the chatbot interface
    """
    <style>
    :root {
        --bg: #0f172a;
        --panel: #111827;
        --accent: #60a5fa;
        --accent-2: #34d399;
        --text: #f8fafc;
        --muted: #94a3b8;
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #1e293b 100%);
    }
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }
    .title-box {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(96, 165, 250, 0.25);
        border-radius: 18px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.18);
    }
    .user-msg, .bot-msg {
        padding: 0.85rem 1rem;
        border-radius: 16px;
        margin: 0.35rem 0;
        max-width: 92%;
        line-height: 1.45;
    }
    .user-msg {
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 6px;
    }
    .bot-msg {
        background: rgba(255,255,255,0.09);
        color: #f8fafc;
        border: 1px solid rgba(52, 211, 153, 0.18);
        border-bottom-left-radius: 6px;
    }
    .sidebar-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(96, 165, 250, 0.18);
        border-radius: 14px;
        padding: 0.9rem;
        margin-bottom: 0.7rem;
    }
    .footer {
        text-align: center;
        color: var(--muted);
        font-size: 0.92rem;
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "faq_entries" not in st.session_state:  # Create a saved FAQ list in session state so it stays available across reruns
    st.session_state.faq_entries = load_faq()  # Load the FAQ data once and store it for reuse

if "messages" not in st.session_state:  # Create a chat history list if one does not already exist
    st.session_state.messages = [  # Store the initial welcome message so the chat starts with a friendly prompt
        {
            "role": "assistant",  # Mark this message as coming from the bot
            "content": "Hi! 👋 I’m your AI FAQ assistant. Ask me anything about this project or the support topics below.",  # The first greeting shown to the user
        }
    ]

with st.sidebar:  # Put the project information in the left sidebar
    st.markdown(  # Render the first sidebar card with project overview details
        """
        <div class="sidebar-card">
            <h3>📘 Project Overview</h3>
            <p>This Streamlit app delivers a polished FAQ experience with a clean chat interface and helpful responses.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(  # Render the second sidebar card with technology details
        """
        <div class="sidebar-card">
            <h3>🛠️ Built With</h3>
            <p>Python • Streamlit • CSV-based FAQ data</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(  # Render the third sidebar card with a helpful tip
        """
        <div class="sidebar-card">
            <h3>💡 Tip</h3>
            <p>Try questions like “What is this chatbot about?” or “How does it work?”</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(  # Show the main title section at the top of the page
    """
    <div class="title-box">
        <h1 style="text-align:center; margin:0; color:#f8fafc;">🤖 AI FAQ Chatbot</h1>
        <p style="text-align:center; margin:0.3rem 0 0; color:#94a3b8;">Professional, friendly, and ready to answer your questions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

for message in st.session_state.messages:  # Loop through every saved chat message
    if message["role"] == "user":  # Check whether the message was sent by the user
        st.markdown(f"<div class='user-msg'>🧑‍💻 {message['content']}</div>", unsafe_allow_html=True)  # Display the user message in a styled bubble
    else:  # Otherwise, treat it as a bot reply
        st.markdown(f"<div class='bot-msg'>🤖 {message['content']}</div>", unsafe_allow_html=True)  # Display the bot response in a styled bubble

user_input = st.text_input("Ask a question", placeholder="Type your question here...")  # Create the text box where the user can type a question

if st.button("Send Message", use_container_width=True):  # Show a button that triggers the chat response
    if user_input.strip():  # Only proceed if the user typed something meaningful
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})  # Save the new question in chat history
        answer = get_answer(user_input.strip(), st.session_state.faq_entries)  # Ask the FAQ logic for the matching answer
        st.session_state.messages.append({"role": "assistant", "content": answer})  # Save the bot reply in chat history
        st.rerun()  # Refresh the page so the newly saved messages appear immediately
    else:  # If the input is empty, show a warning instead of sending
        st.warning("Please enter a question before sending.")

st.markdown(  # Render the footer at the bottom of the page
    """
    <div class="footer">
        Developed by <strong>CodeAlpha</strong> • Crafted with Streamlit for a clean support experience
    </div>
    """,
    unsafe_allow_html=True,
)
