import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Methodology - IRAS Enforcement Officer Assistant",
    page_icon="🔬",
    layout="wide"
)

# Title
st.title("🔬 Methodology")

# Introduction
st.markdown("""
## Understanding the System Architecture & Use Cases

This section explains **how the IRAS Enforcement Officer Virtual Assistant works**,  
including:

- The **technology stack** used  
- The **data processing flow**  
- The **two main use cases** of the application  
- A **flowchart** illustrating all processes (flowchart.png)  

This methodology is based directly on the implemented code and functions.
""")

# Technology Overview
st.header("🤖 Technology Stack")

col1, col2 = st.columns(2)

with col1:
    st.subheader("OpenAI GPT Models")
    st.markdown("""
    The assistant uses OpenAI’s GPT-based models for:
    - Natural language understanding  
    - Extracting NRIC and Case IDs  
    - Following IRAS Standard Operating Procedures  
    - Deciding when to call tools (function-calling)  
    - Drafting email content  
    """)

with col2:
    st.subheader("Streamlit Framework")
    st.markdown("""
    Streamlit handles:
    - User interface (chat window)  
    - Multi-page navigation  
    - Session state for conversation & retrieved data  
    - Rendering of tax data and email previews  
    """)

# Use Case 1
st.header("📌 Use Case 1: AI Chatbot for Tax Queries & Record Retrieval")

st.markdown("""
This is the primary feature of the application. The AI simulates an **IRAS tax officer**  
who can:

1. Respond to general questions  
2. Follow strict IRAS SOP through a long system instruction  
3. Detect taxpayer NRIC and load tax data  
4. Extract Case IDs from casual text  
5. Conduct multi-step workflows such as **Bank Appointment Booking SOP**  
6. Guide the user to MyTax Portal when needed  

### 🔍 Functions Involved in Use Case 1

| Function Name | Purpose |
|---------------|---------|
| **get_tax_data(nric)** | Retrieves taxpayer data from the CSV file |
| **get_case_details(case_id)** | Gets details about the user's case |
| **open_mytax_portal()** | Provides step-by-step instructions to log in to MyTax Portal |
| **bank_appointment_flow()** | Multi-step IRAS workflow for bank appointments |

### 🧠 Process Flow for Use Case 1

1. **User sends a message**  
2. System checks message for:
   - NRIC  
   - Case ID  
   - Keywords indicating SOP workflow  
3. System creates full AI prompt including:
   - IRAS SOP  
   - Conversation history  
   - Function definitions  
4. AI responds OR calls a tool:
   - If NRIC → call `get_tax_data()`  
   - If case number → call `get_case_details()`  
   - If bank appointment → start SOP workflow  
5. Tool returns data → AI interprets it → AI replies to user  
6. Chat continues with updated context stored in session state  

This flow ensures the assistant behaves like a structured, rule-based IRAS officer.
""")

# Use Case 2
st.header("📧 Use Case 2: Automated Email Drafting & Sending")

st.markdown("""
The second major function of the system is **email automation**.

This feature activates during certain workflows, particularly the  
**Bank Appointment SOP**, where an IRAS officer must email a bank  
(e.g., UOB, DBS, OCBC, HSBC).

### 🔓 Trigger Conditions
Email preparation begins when:
- The user reaches the final step of the bank appointment SOP  
- The AI determines that a bank contact email is required  

### ✉️ Functions Involved in Use Case 2

| Function Name | Purpose |
|---------------|---------|
| **send_email(to, subject, message, sender, password)** | Sends email via SMTP |
| **AI-generated email content** | The assistant drafts the text before sending |
| **BANK_EMAILS mapping** | Automatically determines the correct bank mailbox |

### 📬 Process Flow for Use Case 2

1. AI gathers required information from the user:
   - Bank name  
   - Reason for appointment  
   - Case number or tax reference  
2. AI generates email content using the system prompt  
3. System displays:
   - Email preview  
   - Recipient address  
4. User confirms sending  
5. SMTP function `send_email()` is executed with:
   - Gmail SMTP server  
   - Environment-stored credentials  
   - Auto-mapped bank mailbox  
6. Confirmation is returned to the user  
""")

# Flowchart
st.header("🧩 System Flowcharts")

st.markdown("""
The full workflow for both use cases is illustrated in the flowchart below.

The file **flowchart.png** has been added to the GitHub repository and is displayed here:
""")

st.image("flowchart.png", caption="Process flow of both use cases", use_column_width=True)

# Data Handling
st.header("🔄 Data Flow Summary")

st.markdown("""
### Data Sources
- **tax_records.csv** — contains taxpayer details  
- **.env** — stores API keys, email passwords, bank email mappings  
- **System Prompt** — defines IRAS officer behavior and SOP  

### Internal Data Flow
1. User input →  
2. NRIC/Case detection →  
3. Data retrieval via tools →  
4. AI reasoning + response streaming →  
5. Optional email sending →  
6. Display to user via Streamlit  
""")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & OpenAI •")
