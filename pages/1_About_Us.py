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

This project was developed as part of the **AI Bootcamp** to demonstrate a practical,  
workflow-enhancing AI system that simulates how IRAS Enforcement Officers interact  
with taxpayers using SOP-driven guidance, structured dialogs, and automated processes.

The app combines:
- AI-driven conversation flows  
- Email automation  
- Tax record lookup  
- MyTax Portal navigation guidance  
- Bank appointment SOP flows  

All within a single guided interface designed to mimic a CRM environment.
""")

# Objectives & Scope
st.header("🎯 Project Objectives")
st.markdown("""
The primary goals of this project are to:

- Build an AI assistant that helps Enforcement Officers respond to taxpayer queries  
- Automate SOP-driven tasks (e.g., Bank Appointment Release workflow)  
- Improve accuracy by referencing structured IRAS working instructions  
- Reduce officer workload by automating email drafting and lookup processes (for taxpayer information in the internal system)   
""")

st.header("🔭 Project Scope")
st.markdown("""
This prototype focuses on simulating key **IRAS Enforcement workflows**, including:

- Searching taxpayer records by NRIC  
- Extracting case IDs from natural text  
- Executing step-by-step SOP dialogs  
- Drafting emails to banks for appointment releases  
- Following strict system rules to reduce hallucination  

This project is a proof-of-concept to showcase how generative AI can be embedded  
into structured government workflows.
""")

# Data Sources
st.header("📚 Data Sources")
st.markdown("""
This application uses structured datasets and reference materials to simulate IRAS operations:

### **Internal-style Reference Data (Demo)**
- **Taxpayer Records CSV**  
  Contains simulated taxpayer information (NRIC, name, tax types, balances, etc.).
  Includes mock enforcement case information used for lookup and validation.

- **Bank Email Directory**  
  A predefined mapping of bank names to contact emails for appointment release requests.

### **Procedure & SOP Resources**
- **IRAS Bank Appointment Release SOP** (fabricated for demo)   
- **Email Draft Templates**  
- **Mock-up of My Tax Portal Navigation**

> *All datasets and instructions used in this project are mock/demo versions  
and do not contain actual taxpayer information.*
""")

# Section: Features
st.header("💡 Key Features")

st.markdown("""
### 🧠 AI-Powered Conversation Engine
- Structured persona based on IRAS enforcement roles  
- Multi-step guided SOP flows  
- NRIC detection → auto-load taxpayer data  
- Case number extraction logic  
- Hallucination minimised using strict prompting rules

### 📨 Email Automation
- Auto-generated draft emails to banks  
- SMTP sending enabled through preset credentials  
- Predefined bank → email routing logic

### 📁 Data & Workflow Handling
- CSV-based taxpayer data lookup  
- Case detail retrieval  
- Session state for conversation memory   

### 🖥️ Streamlit Interface
- Chat-style interaction window  
- Tool call simulation (get_tax_data, get_case_details, send_email, etc.)  
- Clean, wide-layout experience for officer workflows  
""")

# Section: Team
st.header("👨‍👩‍👧‍👦 Project Team")
st.markdown("""
Developed as part of the **AI Bootcamp Capstone Project** by:
- **Lee Sumi**  
- **Eugene Wong**  
- **He Jinming**

The project demonstrates how AI can enhance operational processes  
within public sector enforcement environments.
""")

# # Section: Contact
# st.header("📧 Contact")
# st.markdown("""
# If you have questions or would like to know more about this project,  
# please reach out to your AI Bootcamp instructor or project team lead.
# """)

# Footer
st.markdown("---")
st.markdown("Built using Streamlit & OpenAI • IRAS Enforcement Officer Assistant Prototype (AI Bootcamp)")