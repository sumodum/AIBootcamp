import streamlit as st

# Page configuration
st.set_page_config(
    page_title="About Us - IRAS Tax Officer Assistant",
    page_icon="👥",
    layout="wide"
)

# Title
st.title("👥 About Us")

# Introduction
st.markdown("""
## Welcome to the IRAS Enforcement Officer Virtual Assistant

This project was developed as part of the **AI Bootcamp**, with the goal of building  
a practical, workflow-enhancing AI system that simulates how IRAS enforcement tax officers  
interact with taxpayers through structured conversation, SOP-driven guidance,  
and automated processes.

The app combines:
- AI-driven conversation flows  
- Email automation  
- Tax record lookup  
- MyTax Portal navigation guidance  
- Bank appointment SOP flows  

All within a single guided interface designed to mimic a CRM environment.
""")

# Mission & Vision
col1, col2 = st.columns(2)

with col1:
    st.header("🎯 Project Mission")
    st.markdown("""
    To create an AI-powered tool that:
    - Assists IRAS enforcement officers in responding to taxpayer queries  
    - Automates SOP-driven tasks (e.g., bank appointment process)  
    - Improves accuracy by referencing real working instructions  
    - Reduces officer load by automating email drafting & information retrieval  
    """)

with col2:
    st.header("🔭 Project Scope & Vision")
    st.markdown("""
    This project focuses on simulating **real IRAS workflows**, including:

    - Loading structured taxpayer data  
    - Searching tax records by NRIC  
    - Handling case ID extraction from natural text  
    - Executing multi-step SOP dialogs for bank appointments  
    - Drafting emails to banks based on predefined formats  
    - Showing relevant IRAS information succinctly  

    The long-term vision is to show how AI can assist public service officers  
    while remaining compliant, structured, and safe.
    """)

# What We Offer
st.header("💡 Features Implemented")

st.markdown("""
### 🧠 AI-Powered Chat Layer
- Structured system prompt based on IRAS SOPs  
- Strict persona and rule enforcement  
- Multi-step guided flows (e.g., bank appointments)  
- Automatic detection of NRIC → loads tax records  
- Case number extraction logic  
- No hallucination enforced through system message constraints  

### 📨 Email Automation
- Auto-generated email drafts to banks  
- Send via SMTP through preset credentials  
- Predefined mappings for bank names → email addresses  

### 📁 Data Handling
- CSV lookup for taxpayer records  
- Session state for conversation memory  
- PDF/website links for MyTax Portal instructions  

### 🖥️ Streamlit Interface
- Custom layout for a chatbot window  
- Conversation history tracking  
- Tool functions that AI can call to:  
  - get_tax_data  
  - get_case_details  
  - send_email  
  - open_mytax_portal  
""")

# Team Section
st.header("👨‍👩‍👧‍👦 The Team")
st.markdown("""
This project was created IRAS enforcement officers, dedicated to demonstrating  
how AI can enhance operational processes within government agencies.

*(Lee Sumi, Eugene Wong, He Jinming)*
""")

# Contact
st.header("📧 Contact")
st.markdown("""
If you have questions or would like to learn more about this project, feel free  
to reach out to the AI Bootcamp instructors or your project team lead.
""")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & OpenAI • IRAS Tax Officer Simulation Project")
