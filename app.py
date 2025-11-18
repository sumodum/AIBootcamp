import streamlit as st
import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialise OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Bank email mapping dictionary
BANK_EMAIL_MAPPING = {
    "UOB": "yumgiraffeyum@gmail.com",
    "DBS": "yumgiraffeyum@gmail.com",
    "OCBC": "yumgiraffeyum@gmail.com",
    "HSBC": "yumgiraffeyum@gmail.com"
}

# Page configuration
st.set_page_config(
    page_title="IRAS Tax Buddy",
    page_icon="🤖",
    layout="wide"
)

# Title with custom background color (compact version)
st.markdown("""
    <div style="background-color: #2D7BB9; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
        <h2 style="color: white; margin: 0;">🤖 IRAS Tax Buddy</h2>
        <p style="color: white; margin: 5px 0 0 0; font-size: 0.9em;">Welcome! Mention your NRIC and Case Number to auto-fill My Tax Portal below.</p>
    </div>
    """, unsafe_allow_html=True)



# Initialise session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "tax_records" not in st.session_state:
    st.session_state.tax_records = None
if "nric" not in st.session_state:
    st.session_state.nric = ""
if "case_number" not in st.session_state:
    st.session_state.case_number = ""
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "bank_appointment_info" not in st.session_state:
    st.session_state.bank_appointment_info = {
        "identification": {},
        "bank_account": {},
        "payment_evidence": {},
        "authorization": {},
        "multiple_accounts": {}
    }
if "bank_appointment_release_approved" not in st.session_state:
    st.session_state.bank_appointment_release_approved = False
if "release_summary" not in st.session_state:
    st.session_state.release_summary = ""
if "email_sent" not in st.session_state:
    st.session_state.email_sent = False
if "bank_name" not in st.session_state:
    st.session_state.bank_name = ""

# Function to extract NRIC and Case Number from text
def extract_nric_case(text):
    nric_pattern = r'\b[STFG]\d{7}[A-Z]\b'
    case_pattern = r'\bTX\d{3}\b'

    nric_match = re.search(nric_pattern, text, re.IGNORECASE)
    case_match = re.search(case_pattern, text, re.IGNORECASE)

    return nric_match.group(0).upper() if nric_match else None, case_match.group(0).upper() if case_match else None

# Function to extract bank name from text
def extract_bank_name(text):
    # Check for bank names in the text
    text_upper = text.upper()
    for bank in BANK_EMAIL_MAPPING.keys():
        if bank in text_upper:
            return bank
    return None

# Function to load tax records
def load_tax_records(nric, case_number):
    try:
        # Read the CSV file
        df = pd.read_csv("data/tax_records.csv")

        # Filter by NRIC and Case Number
        filtered_df = df[(df['NRIC'] == nric) & (df['Case_Number'] == case_number)]

        if not filtered_df.empty:
            # Drop NRIC, Case_Number, and Bank_Appointment_Date columns from display
            columns_to_drop = ['NRIC', 'Case_Number']
            if 'Bank_Appointment_Date' in filtered_df.columns:
                columns_to_drop.append('Bank_Appointment_Date')
            display_df = filtered_df.drop(columns_to_drop, axis=1)
            return display_df
        else:
            return None
    except FileNotFoundError:
        st.error("Tax records database not found.")
        return None
    except Exception as e:
        st.error(f"Error loading records: {str(e)}")
        return None

# Function to send bank appointment release email
def send_bank_release_email(summary, nric, case_number, bank_name=None):
    try:
        # Get email configuration from environment variables
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        sender_email = os.getenv("SENDER_EMAIL", "nomgiraffenom@gmail.com")
        sender_password = os.getenv("SENDER_PASSWORD")

        # Determine bank email based on bank name
        if bank_name and bank_name in BANK_EMAIL_MAPPING:
            bank_email = BANK_EMAIL_MAPPING[bank_name]
        else:
            # Default email if bank name not found
            bank_email = "yumgiraffeyum@gmail.com"

        # Check if email is configured
        if not sender_email or not sender_password:
            st.warning("⚠️ Email configuration not found. Please configure SMTP settings in .env file to send notifications.")
            return False, None

        # Create email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = bank_email
        msg['Subject'] = f"IRAS Bank Appointment Release Notice - {nric} ({case_number})"

        # Email body
        email_body = f"""
Dear Bank Officer,

This is an official notification from the Inland Revenue Authority of Singapore (IRAS) regarding a Bank Appointment Release request.

BANK APPOINTMENT RELEASE NOTICE
================================

Date of Issue: {datetime.now().strftime("%d %B %Y")}
Time of Issue: {datetime.now().strftime("%H:%M:%S")}

CASE DETAILS:
{summary}

AUTHORIZATION:
This release notice authorizes the bank to proceed with releasing the affected account(s). The taxpayer's outstanding tax liabilities have been verified as settled.

Please process this release at your earliest convenience and notify the account holder once the account has been restored to normal operation.

For any queries regarding this notice, please contact IRAS through our official channels.

---
This is an automated notification from IRAS Tax Buddy System.
Generated on: {datetime.now().strftime("%d %B %Y at %H:%M:%S")}
"""

        msg.attach(MIMEText(email_body, 'plain'))

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return True, bank_email

    except Exception as e:
        st.error(f"Failed to send email notification: {str(e)}")
        return False, None

# Display chat history in a scrollable container with fixed height
with st.container(height=400, border=True):
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input section with form for Enter key submission
with st.form(key=f"chat_form_{st.session_state.input_key}", clear_on_submit=True):
    input_col1, input_col2 = st.columns([0.92, 0.08])

    with input_col1:
        user_input = st.text_input("Your message:", placeholder="What would you like to know?", label_visibility="collapsed", key=f"chat_input_{st.session_state.input_key}")

    with input_col2:
        send_button = st.form_submit_button("▶", use_container_width=True)

if send_button and user_input:
    # Extract NRIC and Case Number from user input
    extracted_nric, extracted_case = extract_nric_case(user_input)
    if extracted_nric:
        st.session_state.nric = extracted_nric
    if extracted_case:
        st.session_state.case_number = extracted_case

    # Extract bank name from user input
    extracted_bank = extract_bank_name(user_input)
    if extracted_bank:
        st.session_state.bank_name = extracted_bank

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate assistant response
    try:
        # Load SOP content for bank appointment release process
        sop_content = ""
        try:
            with open("SOP.txt", "r") as f:
                sop_content = f.read()
        except:
            pass

        # Prepare system message with tax context if available
        system_message = """You are IRAS Tax Buddy, a helpful assistant for tax-related questions in Singapore.

You can help users with:
- General tax questions and information
- Understanding tax assessments and payments
- IRAS procedures and requirements
- Tax filing guidance
- Bank Appointment Release Process

When users mention their NRIC or Case Number, acknowledge it naturally and let them know their details will be auto-filled in the My Tax Portal section below.

IMPORTANT - Bank Appointment Release Process:
If a user inquires about releasing a bank appointment or mentions having a bank appointment/account freeze by IRAS, you should PROACTIVELY gather information to process their release request.

Required information categories:
1. Identification: NRIC/FIN/UEN, case/appointment reference number, contact info
2. Bank Account: Bank name and branch, last 3-4 digits of account, account type
3. Payment Evidence: Receipt number, date and amount paid, payment confirmation
4. Authorization (if applicable): Letter of authorization, company documents
5. Multiple Accounts: Whether multiple appointments exist, which accounts affected

CRITICAL - Conversational Approach (MIMIC HUMAN INTERACTION):
- Ask for information ONE question at a time, like a human would
- NEVER list multiple questions in a single response
- Keep your questions natural and conversational
- Wait for the user's answer before asking the next question
- Acknowledge their answer before moving to the next question

Example flow:
❌ BAD: "Could you please provide: 1) Your NRIC 2) Bank name 3) Payment date 4) Amount paid?"
✅ GOOD: "To help you with the bank appointment release, may I start by confirming your NRIC?"
[User provides NRIC]
✅ GOOD: "Thank you! Now, could you tell me which bank the appointment was applied to?"
[User provides bank name]
✅ GOOD: "Got it. What are the last 4 digits of your bank account number?"

Track what information has been provided in the conversation context. Don't ask for information they've already given you.

CRITICAL - Making the Release Determination:
Once you have gathered sufficient information, you MUST:
1. Check if the tax liability has been fully settled (Balance = 0 in their tax records)
2. Verify that payment evidence has been provided
3. Confirm all essential details (NRIC, bank info, payment info) are collected

Then provide a comprehensive summary including:
- Case details (NRIC, Case Number, Bank Account info)
- Payment confirmation details
- Tax liability status from their records

If ALL conditions are met (tax fully paid + all required info collected):
- Include this EXACT phrase in your response: "BANK_APPOINTMENT_RELEASE_APPROVED"
- Inform the user that their bank appointment release process will be initiated
- Explain the next steps (IRAS will notify the bank, account will be released)

If conditions are NOT met:
- Clearly explain what is missing or why the release cannot proceed yet
- Do NOT include the approval phrase
- Guide them on what they need to do next"""

        # Add tax record context if available
        if st.session_state.tax_records is not None and not st.session_state.tax_records.empty:
            tax_summary = f"\n\nThe user has loaded their tax records for NRIC {st.session_state.nric} (Case {st.session_state.case_number}). You can reference their tax information if relevant to their questions."
            system_message += tax_summary

        # Build messages with system context
        messages = [{"role": "system", "content": system_message}]
        messages.extend([
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ])

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )

        full_response = response.choices[0].message.content

        # Check if AI approved the bank appointment release
        if "BANK_APPOINTMENT_RELEASE_APPROVED" in full_response:
            st.session_state.bank_appointment_release_approved = True
            # Store the summary for email
            st.session_state.release_summary = full_response.replace("BANK_APPOINTMENT_RELEASE_APPROVED", "").strip()
            # Remove the keyword from the response shown to user
            full_response = full_response.replace("BANK_APPOINTMENT_RELEASE_APPROVED", "").strip()

            # Send email to bank if not already sent
            if not st.session_state.email_sent and st.session_state.nric and st.session_state.case_number:
                email_sent, bank_email = send_bank_release_email(
                    st.session_state.release_summary,
                    st.session_state.nric,
                    st.session_state.case_number,
                    st.session_state.bank_name
                )
                if email_sent:
                    st.session_state.email_sent = True
                    bank_display = f"{st.session_state.bank_name} ({bank_email})" if st.session_state.bank_name else bank_email
                    st.success(f"✉️ Bank appointment release notice sent to {bank_display}")

        # Extract NRIC and Case Number from assistant response
        extracted_nric, extracted_case = extract_nric_case(full_response)
        if extracted_nric:
            st.session_state.nric = extracted_nric
        if extracted_case:
            st.session_state.case_number = extracted_case

        # Extract bank name from assistant response
        extracted_bank = extract_bank_name(full_response)
        if extracted_bank:
            st.session_state.bank_name = extracted_bank

    except Exception as e:
        error_message = f"Error: {str(e)}"
        if "api_key" in str(e).lower():
            error_message = "⚠️ OpenAI API key not found or invalid. Please check your .env file."
        full_response = error_message

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Increment input key to clear the input field
    st.session_state.input_key += 1

    # Rerun to show the new messages and clear input
    st.rerun()

# My Tax Portal Section
st.markdown("---")
st.markdown("""
    <div style="background-color: #2D7BB9; padding: 20px; border-radius: 10px; margin-top: 10px;">
        <h2 style="color: white; margin-top: 0;">My Tax Portal</h2>
    </div>
    """, unsafe_allow_html=True)

# Auto-fetch when both NRIC and Case Number are extracted from chat
if st.session_state.nric and st.session_state.case_number and st.session_state.tax_records is None:
    st.session_state.tax_records = load_tax_records(st.session_state.nric, st.session_state.case_number)

# Display NRIC and Case Number
if st.session_state.nric and st.session_state.case_number:
    # Check if there's a bank appointment date
    bank_appointment_date = None
    if st.session_state.tax_records is not None:
        try:
            df = pd.read_csv("data/tax_records.csv")
            filtered_df = df[(df['NRIC'] == st.session_state.nric) & (df['Case_Number'] == st.session_state.case_number)]
            if not filtered_df.empty and 'Bank_Appointment_Date' in filtered_df.columns:
                # Get the most recent bank appointment date (non-empty)
                appointments = filtered_df[filtered_df['Bank_Appointment_Date'].notna() & (filtered_df['Bank_Appointment_Date'] != '')]
                if not appointments.empty:
                    bank_appointment_date = appointments.iloc[-1]['Bank_Appointment_Date']
        except:
            pass

    # Show actual values when NRIC and Case Number are provided
    bank_appointment_html = ""
    if st.session_state.bank_appointment_release_approved:
        # Show release in progress status
        bank_appointment_html = f"""<br><strong>Bank Appointment Date:</strong> {bank_appointment_date if bank_appointment_date else 'N/A'}
        <br><strong style="color: #28a745;">Bank Appointment Release:</strong> <span style="color: #28a745;">In Progress ✓</span>"""
    elif bank_appointment_date:
        bank_appointment_html = f"<br><strong>Bank Appointment Date:</strong> {bank_appointment_date}"
    else:
        bank_appointment_html = "<br><strong>Bank Appointment:</strong> None"

    st.markdown(f"""
    <div style="padding: 15px 0;">
        <strong>NRIC:</strong> {st.session_state.nric} &nbsp;&nbsp;&nbsp;&nbsp; <strong>Case Number:</strong> {st.session_state.case_number}
        {bank_appointment_html}
    </div>
    """, unsafe_allow_html=True)
else:
    # Show placeholders when no NRIC/Case Number provided yet
    st.markdown("""
    <div style="padding: 15px 0;">
        <strong>NRIC:</strong> _________ &nbsp;&nbsp;&nbsp;&nbsp; <strong>Case Number:</strong> _________
        <br><strong>Bank Appointment:</strong> _________
    </div>
    """, unsafe_allow_html=True)

# Display tax records table
if st.session_state.tax_records is not None:
    st.markdown("### Tax Assessment Records")

    # Format the dataframe for better display
    display_df = st.session_state.tax_records.copy()

    # Format currency columns
    if 'Payable' in display_df.columns:
        display_df['Payable (S$)'] = display_df['Payable'].apply(lambda x: f"{x:.2f}")
        display_df = display_df.drop('Payable', axis=1)

    if 'Paid' in display_df.columns:
        display_df['Paid (S$)'] = display_df['Paid'].apply(lambda x: f"{x:.2f}")
        display_df = display_df.drop('Paid', axis=1)

    if 'Balance' in display_df.columns:
        display_df['Balance (S$)'] = display_df['Balance'].apply(lambda x: f"{x:.2f}")
        display_df = display_df.drop('Balance', axis=1)

    # Reorder columns to match the reference image
    column_order = ['Date', 'Description', 'Year_of_Assessment', 'Payable (S$)', 'Paid (S$)', 'Balance (S$)']
    display_df = display_df[[col for col in column_order if col in display_df.columns]]

    # Rename Year_of_Assessment for display
    display_df = display_df.rename(columns={'Year_of_Assessment': 'Year of Assessment'})
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    # Check if user has provided NRIC and Case Number but no records found
    if st.session_state.nric and st.session_state.case_number:
        st.warning("⚠️ No matching tax records for the provided NRIC and Case Number.")
    else:
        st.info("ℹ️ Please mention your NRIC and Case Number in the chat to view your tax records.")

# Sidebar with chat controls
with st.sidebar:
    st.header("💬 Chat Controls")

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.bank_appointment_info = {
            "identification": {},
            "bank_account": {},
            "payment_evidence": {},
            "authorization": {},
            "multiple_accounts": {}
        }
        st.session_state.bank_appointment_release_approved = False
        st.session_state.nric = ""
        st.session_state.case_number = ""
        st.session_state.tax_records = None
        st.session_state.release_summary = ""
        st.session_state.email_sent = False
        st.session_state.bank_name = ""
        st.rerun()

    st.markdown("---")
    st.markdown("**Model:** GPT-3.5 Turbo")
    st.markdown("Built using Streamlit & OpenAI")
