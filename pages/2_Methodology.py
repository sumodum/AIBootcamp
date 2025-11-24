import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Methodology - IRAS Tax Buddy",
    page_icon="🔬",
    layout="wide"
)

# Title
st.title("🔬 Methodology")

# Introduction
st.markdown("""
## Understanding the System Architecture & Use Cases

This section explains **how the IRAS Tax Buddy works**, including:
- The **technology stack** used
- The **data processing flow**
- The **two main use cases** with detailed flowcharts
- **Implementation details** for each use case

This methodology is based directly on the implemented code and functions.
""")

# Technology Overview
st.header("🤖 Technology Stack")

col1, col2 = st.columns(2)

with col1:
    st.subheader("OpenAI GPT-3.5 Turbo")
    st.markdown("""
    The assistant uses OpenAI's GPT-3.5 Turbo for:
    - Natural language understanding
    - Extracting NRIC and Case Numbers via regex
    - Following IRAS Standard Operating Procedures (SOP)
    - Making approval/rejection decisions
    - Generating structured summaries
    """)

with col2:
    st.subheader("Streamlit Framework")
    st.markdown("""
    Streamlit handles:
    - User interface (chat window + tax portal display)
    - Multi-page navigation
    - Session state for conversation & tax records
    - Real-time data display
    - Password protection
    """)

st.subheader("Other Technologies")
col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    **Data Storage:**
    - Pandas for CSV data manipulation
    - tax_records.csv for taxpayer records
    - Session state for runtime data
    """)

with col4:
    st.markdown("""
    **Email Integration:**
    - SMTP for Gmail integration
    - Environment variables for credentials
    - Automated email-sending to upate the banks
    """)

st.markdown("---")
st.header("📌 Use Case 1: General Tax Information Chat & Tax Record Retrieval")

st.markdown("""
This use case covers the basic chatbot functionality where users can:
1. Provide their NRIC and Case Number to retrieve tax records
2. View their tax assessment records in the My Tax Portal section

### Key Features:
- **NRIC & Case Number Extraction**: Automatic detection using regex patterns
- **Tax Record Loading**: Real-time CSV data retrieval and display
- **Conversational Interface**: Natural language Q&A with the AI
- **Tax Portal Integration**: Auto-population of user tax information (to be connected to the actual IRAS system in future)
""")

st.subheader("🔄 Use Case 1 Flowchart")
mermaid_code_uc1 = """
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#2D7BB9','primaryTextColor':'#fff','primaryBorderColor':'#1a5490','lineColor':'#1a5490','secondaryColor':'#f0f0f0','tertiaryColor':'#fff','edgeLabelBackground':'#ffffff'}}}%%
graph LR
    A([User Opens App]) --> B{Password OK?}
    B -->|No| B
    B -->|Yes| C[Chat Interface]
    C --> D[User Message]
    D --> E{NRIC/Case<br/>Detected?}
    E -->|Yes| F[Load Tax Records<br/>from CSV]
    E -->|No| G[AI Response]
    F --> H[Display in<br/>Tax Portal]
    H --> G[AI Processes<br/>& Responds]
    G --> I[Update Chat]
    I --> D

    style A fill:#2D7BB9,stroke:#1a5490,color:#fff
    style C fill:#4CAF50,stroke:#388E3C,color:#fff
    style F fill:#FF9800,stroke:#F57C00,color:#fff
    style H fill:#9C27B0,stroke:#7B1FA2,color:#fff
    style G fill:#2196F3,stroke:#1976D2,color:#fff

    linkStyle default stroke:#1a5490,stroke-width:2px,color:#000
"""

st.components.v1.html(f"""
<div style="background-color: white; padding: 20px; border-radius: 10px; border: 2px solid #2D7BB9; overflow-x: auto;">
    <pre class="mermaid">
{mermaid_code_uc1}
    </pre>
    <style>
        .edgeLabel {{ color: #000 !important; background-color: #fff !important; }}
        .edgeLabel span {{ color: #000 !important; }}
    </style>
</div>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({{ startOnLoad: true }});
</script>
""", height=400)

st.subheader("🔍 Technical Implementation Details")

st.markdown("""
### NRIC & Case Number Detection
- **Regex Pattern for NRIC**: `\b[STFG]\d{7}[A-Z]\b` (e.g., S1111111A)
- **Regex Pattern for Case Number**: `\bTX\d{3}\b'` (case-insensitive, e.g., tx001, TX001)
- Extraction happens in real-time as user types

### Tax Records Loading
```python
def load_tax_records(nric, case_number):
    df = pd.read_csv("data/tax_records.csv")
    filtered_df = df[(df['NRIC'] == nric) &
                     (df['Case_Number'] == case_number)]
    return filtered_df
```

### Session State Management
- `st.session_state.messages`: Stores chat history
- `st.session_state.nric`: Current user NRIC
- `st.session_state.case_number`: Current case number
- `st.session_state.tax_records`: Loaded tax data (DataFrame)

### AI Context Enhancement
When tax records are loaded, the AI receives:
- Total Payable, Total Paid, Current Balance
- Bank Appointment Details (if exists)
- Instructions to use actual values (not placeholders)
""")

st.markdown("---")

st.header("📧 Use Case 2: Bank Appointment Release Process")

st.markdown("""
This use case represents the core workflow of the application - the complete bank appointment release process following IRAS Standard Operating Procedures (SOP).

The system guides the user through a structured 4-step process:
1. **Taxpayer Verification & Information Disclosure** - Extract NRIC/Case Number, retrieve and disclose tax information
2. **Fund Availability Assessment** - Verify full appointment amount is available in appointed bank
3. **Bank Account Confirmation** - Verify bank details and last 4 digits of account number
4. **Release Determination & Summary** - Generate structured summary, make approval/rejection decision, send automated email if approved

### Key Features:
- **4-Step SOP Workflow**: Structured process following IRAS procedures
- **Approval Criteria Validation**: AI evaluates all conditions before approving
- **Automated Email Notification**: Sends release notice to appointed bank
- **Real-time Portal Updates**: Displays "In Progress" status when approved
""")

st.subheader("🔄 Use Case 2 Flowchart")

mermaid_code_uc2_main = """
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#2D7BB9','primaryTextColor':'#fff','primaryBorderColor':'#1a5490','lineColor':'#1a5490','secondaryColor':'#f0f0f0','tertiaryColor':'#fff','edgeLabelBackground':'#ffffff'}}}%%
graph LR
    A([NRIC & Case]) --> B[Load Records]
    B --> C{Appt Exists?}
    C -->|No| X1[End]
    C -->|Yes| D[Step 1: Disclose Info]
    D --> E[Step 2: Check Funds]
    E --> F{Funds OK?}
    F -->|No| X2[❌ Reject]
    F -->|Yes| G[Step 3: Verify Bank]
    G --> H{Bank Match?}
    H -->|No| X3[❌ Reject]
    H -->|Yes| I[Step 4: Summary]
    I --> J{Approve?}
    J -->|No| X4[❌ Reject]
    J -->|Yes| K[✅ Approve]
    K --> L[Email Bank]
    L --> M[Portal: In Progress ✓]

    style A fill:#2D7BB9,stroke:#1a5490,color:#fff
    style D fill:#4CAF50,stroke:#388E3C,color:#fff
    style E fill:#2196F3,stroke:#1976D2,color:#fff
    style G fill:#9C27B0,stroke:#7B1FA2,color:#fff
    style I fill:#FF9800,stroke:#F57C00,color:#fff
    style K fill:#4CAF50,stroke:#388E3C,color:#fff
    style X2 fill:#F44336,stroke:#D32F2F,color:#fff
    style X3 fill:#F44336,stroke:#D32F2F,color:#fff
    style X4 fill:#F44336,stroke:#D32F2F,color:#fff
    style L fill:#00BCD4,stroke:#0097A7,color:#fff
    style M fill:#4CAF50,stroke:#388E3C,color:#fff

    linkStyle default stroke:#1a5490,stroke-width:2px,color:#000
"""

st.components.v1.html(f"""
<div style="background-color: white; padding: 20px; border-radius: 10px; border: 2px solid #2D7BB9; overflow-x: auto;">
    <pre class="mermaid">
{mermaid_code_uc2_main}
    </pre>
    <style>
        .edgeLabel {{ color: #000 !important; background-color: #fff !important; }}
        .edgeLabel span {{ color: #000 !important; }}
    </style>
</div>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({{ startOnLoad: true }});
</script>
""", height=400)

st.subheader("🔍 Technical Implementation Details")

st.markdown("""
### Approval Criteria (ALL must be met)
1. ✓ Tax liability is fully settled OR full payment confirmed
2. ✓ User confirms full appointment amount is available
3. ✓ Bank matches appointed bank
4. ✓ All required information provided (NRIC, Case Number, Bank Details, Account Number)

### AI Summary Generation
The AI generates a structured summary in this format:
```
Your request for bank appointment release is [APPROVED/REJECTED]
REASON: [Explanation]

CASE DETAILS:
- NRIC: [value]
- Case Number: [value]
- Year of Assessment: [value]

BANK APPOINTMENT INFORMATION:
- Appointed Bank: [value]
- Appointment Amount: S$[value]
- Appointment Date: [value]

TAX LIABILITY STATUS:
- Total Payable: S$[value]
- Total Paid: S$[value]
- Current Balance: S$[value]

FUND AVAILABILITY:
- User confirmed: [YES/NO]

VERIFICATION:
- Bank Account Confirmed: [value]
- Account Details: [last 4 digits]

BANK_APPOINTMENT_RELEASE_APPROVED
[If approved, includes this exact keyword]
```

### Approval Detection
```python
if "BANK_APPOINTMENT_RELEASE_APPROVED" in full_response:
    st.session_state.bank_appointment_release_approved = True
    # Trigger email sending
    send_bank_release_email(...)
```

### Email Automation
When approved, the system:
1. Extracts Bank Appointment Information, Fund Availability, and Verification sections from summary
2. Generates professional email to appointed bank
3. Sends via Gmail SMTP with App Password
4. Maps bank name to email address using BANK_EMAIL_MAPPING
5. Confirms delivery to user

### Email Template Structure
- **Document Information**: Reference number, date, time
- **Case Summary**: Extracted sections from AI summary
- **Authorisation**: Official release statement
- **Action Required**: Steps for bank to follow
- **Contact Information**: IRAS contact details
""")

st.markdown("---")

# Data Flow
st.header("🔄 Complete Data Flow Architecture")

st.markdown("""
### Data Sources
1. **tax_records.csv** — Contains taxpayer records with columns:
   - NRIC, Case_Number, Date, Description, Year_of_Assessment
   - Payable, Paid, Balance
   - Bank_Appointment_Date, Appointed_Bank, Appointment_Amount

2. **.env / Streamlit Secrets** — Stores sensitive configuration:
   - OPENAI_API_KEY: OpenAI API authentication
   - APP_PASSWORD: Application password protection
   - SMTP credentials: Email sending configuration
   - BANK_EMAILS: Bank name to email address mappings
   - IRAS_CONTACT_*: Contact information for emails

3. **SOP.txt** — Standard Operating Procedures document defining:
   - Process flow requirements
   - Question formats
   - Approval criteria
   - Rejection scenarios

### Internal Data Flow
```
1. User Input (Chat Message)
   ↓
2. Regex Extraction (NRIC/Case Number)
   ↓
3. Session State Update
   ↓
4. CSV Data Loading (if NRIC/Case found)
   ↓
5. AI Context Preparation (System Prompt + Tax Data)
   ↓
6. OpenAI API Call (GPT-3.5 Turbo)
   ↓
7. AI Response Processing
   ↓
8. Approval Detection (keyword search)
   ↓
9. Email Sending (if approved)
   ↓
10. UI Update (Chat + Tax Portal + Status)
```

### Session State Variables
- `messages`: List of chat messages (role + content)
- `nric`: Current user NRIC
- `case_number`: Current case number
- `tax_records`: Pandas DataFrame of loaded records
- `bank_name`: Extracted bank name from conversation
- `bank_appointment_release_approved`: Boolean approval flag
- `email_sent`: Boolean to prevent duplicate emails
- `release_summary`: Stored AI summary for email
- `password_correct`: Password authentication status
- `input_key`: Counter for clearing input field
""")

st.markdown("---")

# Security & Best Practices
st.header("🔒 Security & Best Practices")

col_sec1, col_sec2 = st.columns(2)

with col_sec1:
    st.subheader("Security Measures")
    st.markdown("""
    ✅ **Password Protection**
    - All users must authenticate before accessing app
    - Password stored in environment variables

    ✅ **API Key Security**
    - OpenAI API key stored in secrets
    - Environment variable loading with python-dotenv

    ✅ **Email Security**
    - Gmail App Password
    - SMTP authentication required
    - Credentials never displayed to user

    ✅ **Data Privacy**
    - Tax data loaded per session
    - No logging of sensitive information
    - Session state cleared on browser refresh
    """)

with col_sec2:
    st.subheader("Best Practices Implemented")
    st.markdown("""
    ✅ **Error Handling**
    - Try-catch blocks for API calls
    - Graceful degradation on failures
    - User-friendly error messages

    ✅ **Data Validation**
    - Regex validation for NRIC/Case patterns
    - Bank name verification
    - Appointment amount checks

    ✅ **AI Safety**
    - Structured system prompts
    - Step-by-step conversation flow
    - Explicit approval criteria
    - Keyword-based approval detection

    ✅ **Code Organization**
    - Modular functions
    - Clear separation of concerns
    - Comprehensive debug logging
    """)

st.markdown("---")


st.markdown("""
## 📚 Additional Resources

- **SOP.txt**: Complete Standard Operating Procedures
- **tax_records.csv**: Sample tax data structure
- **DEPLOYMENT.md**: Deployment guide for Streamlit Community Cloud
- **.env.example**: Environment variable template

---

Built using Streamlit & OpenAI • IRAS Enforcement Officer Assistant Prototype (AI Bootcamp)
""")
