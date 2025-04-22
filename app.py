import streamlit as st
import google.generativeai as genai
import PyPDF2
from io import BytesIO

# Configure API Key
api_key = "AIzaSyDZ7RfQVeokbqHyp9YE5odUL_bJMa4jVHA"
genai.configure(api_key=api_key)

# Streamlit Page Config
st.set_page_config(
    page_title="MediScan Pro - AI Health Diagnostics",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Premium Medical Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.stApp {
    background: linear-gradient(152deg, #0B0C13 0%, #161A28 50%, #0B0C13 100%);
    color: #FFFFFF;
}

.header-container {
    background: rgba(11, 12, 19, 0.9);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 3rem 2rem;
    margin: 2rem auto;
    border: 2px solid rgba(99, 102, 241, 0.2);
    box-shadow: 0 0 25px rgba(99, 102, 241, 0.15);
    position: relative;
    overflow: hidden;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    margin: 3rem 0;
}

.feature-card {
    background: rgba(17, 19, 28, 0.8);
    border: 2px solid rgba(99, 102, 241, 0.2);
    border-radius: 20px;
    padding: 2rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(8px);
}

.feature-card:hover {
    transform: translateY(-5px);
    background: rgba(22, 24, 35, 0.9);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.chat-container {
    background: rgba(17, 19, 28, 0.8);
    border-radius: 24px;
    padding: 2rem;
    margin: 2rem 0;
    border: 2px solid rgba(99, 102, 241, 0.2);
    backdrop-filter: blur(8px);
    min-height: 60vh;
}

.user-message {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    color: white;
    padding: 1.5rem;
    border-radius: 20px 20px 4px 20px;
    margin: 1rem 0 1rem auto;
    max-width: 75%;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.bot-message {
    background: linear-gradient(135deg, #6d28d9, #9333ea);
    color: white;
    padding: 1.5rem;
    border-radius: 20px 20px 20px 4px;
    margin: 1rem 0;
    max-width: 75%;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.stChatInput > div > div input {
    background: rgba(17, 19, 28, 0.9) !important;
    color: white !important;
    border: 2px solid rgba(99, 102, 241, 0.3) !important;
    border-radius: 1px !important;
    padding: 1rem 1.5rem !important;
    backdrop-filter: blur(8px) !important;
}

.stChatInput > div > div input::placeholder {
    color: #94A3B8 !important;
    opacity: 0.1 !important;
}

.typing-indicator {
    display: flex;
    align-items: center;
    padding: 1rem;
    color: #94A3B8;
    font-style: italic;
}

.dot-animation {
    display: inline-flex;
    margin-left: 8px;
}

.dot {
    width: 6px;
    height: 6px;
    background: #818CF8;
    border-radius: 50%;
    margin: 0 2px;
    animation: bounce 1.4s infinite ease-in-out;
}

@keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-8px); }
}

.gradient-text {
    background: linear-gradient(135deg, #818CF8 0%, #4F46E5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="header-container">
    <div style="text-align: center;">
        <h1 style="font-size: 2.8rem; margin-bottom: 0.5rem;">
            <span class="gradient-text">MediScan Pro</span> 🌡️
        </h1>
        <p style="color: #94A3B8; font-size: 1.1rem; letter-spacing: 0.5px;">
            Advanced AI-Powered Medical Diagnostics & Report Analysis
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Feature Grid
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div style="margin-bottom: 1rem; font-size: 2rem;">🩺</div>
        <h3>Clinical Analysis</h3>
        <p style="color: #94A3B8;">Advanced symptom pattern recognition</p>
    </div>
    <div class="feature-card">
        <div style="margin-bottom: 1rem; font-size: 2rem;">📄</div>
        <h3>Report Analysis</h3>
        <p style="color: #94A3B8;">Comprehensive medical report evaluation</p>
    </div>
    <div class="feature-card">
        <div style="margin-bottom: 1rem; font-size: 2rem;">📊</div>
        <h3>Health Insights</h3>
        <p style="color: #94A3B8;">Personalized health recommendations</p>
    </div>
    <div class="feature-card">
        <div style="margin-bottom: 1rem; font-size: 2rem;">🔒</div>
        <h3>Secure Platform</h3>
        <p style="color: #94A3B8;">Encrypted data protection</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat Container
chat_container = st.container()
with chat_container:
    st.markdown('', unsafe_allow_html=True)

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'''
            <div class="user-message">
                <div style="font-weight: 500; margin-bottom: 0.5rem;">👤 You</div>
                {msg["content"]}
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="bot-message">
                <div style="font-weight: 500; margin-bottom: 0.5rem;">🌡️ MediScan</div>
                {msg["content"]}
            
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# File Upload Section
uploaded_file = st.file_uploader("📁 Upload Medical Report (PDF/TXT)", type=["pdf", "txt"])

# Model Configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config
)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# File Processing Logic
if uploaded_file and not st.session_state.messages:
    try:
        # Extract text from file
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
            text = "\n".join([page.extract_text() for page in pdf_reader.pages])
        else:
            text = uploaded_file.read().decode("utf-8")

        # Create analysis prompt
        system_prompt = """You are a senior medical diagnostician. Analyze this report and provide:
1. 🩺 Primary Diagnosis
2. 🔍 Key Findings
3. ⚠️ Risk Factors
4. ✅ Recommended Actions

Medical Report:
"""
        full_prompt = system_prompt + text

        # Add to messages
        st.session_state.messages.append({
            "role": "user",
            "content": f"📄 Uploaded Report: {uploaded_file.name}\n{text}"
        })

        # Get analysis
        with st.spinner("🔍 Analyzing medical report..."):
            response = st.session_state.chat_session.send_message(full_prompt)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text
            })
            st.rerun()

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

# Chat Input Logic
if prompt := st.chat_input("Describe symptoms or ask about your report..."):
    if not st.session_state.messages:
        prompt = """You are a medical expert. Respond with:
1. 🔍 Possible Conditions
2. 📋 Diagnostic Suggestions
3. ⚠️ Red Flags
4. ✅ Next Steps
—""" + prompt

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner(""):
        with chat_container:
            # Show typing indicator
            st.markdown('''
            <div class="typing-indicator">
                Analyzing query
                <div class="dot-animation">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Get response
            response = st.session_state.chat_session.send_message(prompt)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text
            })
            st.rerun()


# import streamlit as st
# import google.generativeai as genai

# # Configure API Key
# api_key = "AIzaSyCDnbHdn81MxJF3N42dRzbcv5OjFEhSNds"  # Replace with your actual key
# genai.configure(api_key=api_key)

# # Streamlit Page Config
# st.set_page_config(
#     page_title="MediGenius Pro - AI Health Assistant",
#     page_icon="⚕️",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# # Premium Styling with #0B0C13 Background
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

# html, body, .stApp {
#     background-color: #0B0C13 !important;
#     color: #FFFFFF;
#     font-family: 'Inter', sans-serif;
# }

# /* Header Container */
# .header-container {
#     background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(165, 180, 252, 0.1));
#     backdrop-filter: blur(20px);
#     border-radius: 24px;
#     padding: 2.5rem;
#     margin: 2rem auto;
#     border: 2px solid rgba(255, 255, 255, 0.05);
#     box-shadow: 0 0 15px rgba(99, 102, 241, 0.25);
# }

# /* Features Grid */
# .feature-grid {
#     display: grid;
#     grid-template-columns: repeat(4, 1fr);
#     gap: 1.5rem;
#     margin: 3rem 0;
# }

# .feature-card {
#     background: #11131C;
#     border: 2px solid rgba(99, 102, 241, 0.2);
#     border-radius: 20px;
#     padding: 2rem;
#     transition: all 0.3s ease-in-out;
#     box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
# }

# .feature-card:hover {
#     background: #161821;
#     transform: scale(1.03);
# }

# /* Chat container */
# .chat-container {
#     background: #11131C;
#     border-radius: 24px;
#     padding: 2rem;
#     margin: 2rem 0;
#     border: 2px solid rgba(255, 255, 255, 0.05);
#     box-shadow: inset 0 0 15px rgba(255,255,255,0.02);
# }

# /* Messages */
# .user-message, .bot-message {
#     padding: 1.5rem;
#     border-radius: 20px;
#     margin: 1rem 0;
#     max-width: 75%;
#     box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
# }

# .user-message {
#     background: linear-gradient(135deg, #1d4ed8, #3b82f6);
#     margin-left: auto;
#     color: white;
# }

# .bot-message {
#     background: linear-gradient(135deg, #6d28d9, #9333ea);
#     color: white;
# }

# /* Typing indicator */
# .typing-indicator {
#     display: flex;
#     align-items: center;
#     padding: 1rem;
#     color: #94A3B8;
# }

# .dot-animation {
#     display: inline-flex;
#     margin-left: 8px;
# }

# .dot {
#     width: 6px;
#     height: 6px;
#     background: #818CF8;
#     border-radius: 50%;
#     margin: 0 2px;
#     animation: bounce 1.4s infinite ease-in-out;
# }
# .dot:nth-child(2) { animation-delay: 0.2s; }
# .dot:nth-child(3) { animation-delay: 0.4s; }

# @keyframes bounce {
#     0%, 80%, 100% { transform: translateY(0); }
#     40% { transform: translateY(-8px); }
# }
# </style>
# """, unsafe_allow_html=True)

# # Header
# st.markdown("""
# <div class="header-container">
#     <div style="text-align: center;">
#         <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">
#             <span style="background: linear-gradient(135deg, #818CF8 0%, #4F46E5 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
#                 MediGenius Pro
#             </span>
#         </h1>
#         <p style="color: #94A3B8; font-size: 1.1rem;">
#             Advanced AI-Powered Healthcare Diagnostics Platform
#         </p>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Feature Cards
# st.markdown("""
# <div class="feature-grid">
#     <div class="feature-card">
#         <div style="margin-bottom: 1rem; font-size: 2rem;">🩺</div>
#         <h3>Symptom Analysis</h3>
#         <p>Advanced neural network processing for accurate symptom interpretation</p>
#     </div>
#     <div class="feature-card">
#         <div style="margin-bottom: 1rem; font-size: 2rem;">🧠</div>
#         <h3>AI Diagnosis</h3>
#         <p>Deep learning models trained on medical literature</p>
#     </div>
#     <div class="feature-card">
#         <div style="margin-bottom: 1rem; font-size: 2rem;">📊</div>
#         <h3>Health Insights</h3>
#         <p>Personalized health recommendations and risk assessment</p>
#     </div>
#     <div class="feature-card">
#         <div style="margin-bottom: 1rem; font-size: 2rem;">🔒</div>
#         <h3>Secure Chat</h3>
#         <p>End-to-end encrypted conversations</p>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Chat UI
# chat_container = st.container()
# with chat_container:
#     st.markdown('<div class="chat-container">', unsafe_allow_html=True)

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     for msg in st.session_state.messages:
#         if msg["role"] == "user":
#             st.markdown(f'''
#             <div class="user-message">
#                 <strong>👤 You</strong><br>{msg["content"]}
#             </div>
#             ''', unsafe_allow_html=True)
#         else:
#             st.markdown(f'''
#             <div class="bot-message">
#                 <strong>⚕️ MediGenius</strong><br>{msg["content"]}
            
#             ''', unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)

# # Gemini Config
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 64,
#     "max_output_tokens": 8192,
# }

# model = genai.GenerativeModel(
#     model_name="gemini-1.5-pro",
#     generation_config=generation_config
# )

# if "chat_session" not in st.session_state:
#     st.session_state.chat_session = model.start_chat(history=[])

# # Chat Input Logic
# if prompt := st.chat_input("Describe your symptoms in detail..."):
#     if not st.session_state.messages:
#         prompt = """You are a premium healthcare assistant. Respond in this structure:
# 1. 🧪 Potential Causes: (list 3-5 possibilities)
# 2. 📌 Key Indicators: (highlight important symptoms)
# 3. ⚠️ Risk Assessment: (mention urgent signs to watch for)
# 4. ✅ Recommended Actions: (create a step-by-step plan)
# —
# """ + prompt

#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.spinner("Analyzing..."):
#         with chat_container:
#             st.markdown(f'''
#             <div class="typing-indicator">
#                 MediGenius is preparing your diagnosis
#                 <div class="dot-animation">
#                     <div class="dot"></div><div class="dot"></div><div class="dot"></div>
#                 </div>
#             </div>
#             ''', unsafe_allow_html=True)

#             response = st.session_state.chat_session.send_message(prompt)
#             st.session_state.messages.append({"role": "assistant", "content": response.text})
#             st.rerun()


# import streamlit as st
# import os
# import google.generativeai as genai

# # Paste your Gemini API Key directly here
# api_key = "AIzaSyCDnbHdn81MxJF3N42dRzbcv5OjFEhSNds"

# # Configure Gemini API
# genai.configure(api_key=api_key)

# # Streamlit page settings
# st.set_page_config(
#     page_title="Healthcare ChatBot - Powered by Gemini!",
#     page_icon="🏥",
#     layout="wide",
# )

# # Styling
# st.markdown(
#     """
#     <style>
#     .stButton > button {
#         width: 100%;
#         padding: 10px 0;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Banner and info
# st.markdown("<h1 style='text-align: center;'>🏥 Healthcare ChatBot!</h1>", unsafe_allow_html=True)

# col1, col2 = st.columns(2)
# with col1:
#     st.success("📊 Analyze symptoms and suggest possible conditions.")
#     st.info("📈 Provide insights for your next steps.")
# with col2:
#     st.warning("📄 Helps identify trends and make informed choices.")
#     st.error("💡 Gives tailored health tips based on your symptoms.")

# # Setup model (without system_instruction for version 0.8.5)
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 64,
#     "max_output_tokens": 8192,
# }

# model = genai.GenerativeModel(
#     model_name="gemini-1.5-pro",
#     generation_config=generation_config
# )

# # Initialize session
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "chat_session" not in st.session_state:
#     st.session_state.chat_session = model.start_chat(history=[])

# # Display history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # Input field
# if prompt := st.chat_input("What is your question?"):
#     # System prompt (added only for the first user input)
#     if not st.session_state.messages:
#         prompt = """
# You are a healthcare chatbot. When the user reports symptoms, respond in the following structure:
# 1. Explain possible causes.
# 2. Describe why those causes may occur.
# 3. Cross-check with common conditions.
# 4. Provide recommendations or next steps for medical help.
# —
# """ + prompt

#     # Show user message
#     st.chat_message("user").markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.spinner("Analyzing..."):
#         response = st.session_state.chat_session.send_message(prompt)

#     # Show assistant response
#     st.chat_message("assistant").markdown(response.text)
#     st.session_state.messages.append({"role": "assistant", "content": response.text})
