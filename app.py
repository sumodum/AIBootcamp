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

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load BANK_EMAIL_MAPPING info from .env 
bank_emails_str = os.getenv("BANK_EMAILS", "")
BANK_EMAIL_MAPPING = {}
if bank_emails_str:
    for mapping in bank_emails_str.split(","):
        if ":" in mapping:
            bank, email = mapping.split(":", 1)
            BANK_EMAIL_MAPPING[bank.strip()] = email.strip()

# Load IRAS Contact Information from .env
IRAS_CONTACT_PHONE = os.getenv("IRAS_CONTACT_PHONE", "(+65) 6356 7012")
IRAS_CONTACT_EMAIL = os.getenv("IRAS_CONTACT_EMAIL", "tax_support@iras.gov.sg")
IRAS_WEBSITE = os.getenv("IRAS_WEBSITE", "www.iras.gov.sg")
IRAS_OPERATING_HOURS = os.getenv("IRAS_OPERATING_HOURS", "Mondays to Fridays (8 a.m. to 5 p.m.)")

# Page configuration
st.set_page_config(
    page_title="IRAS Tax Buddy",
    page_icon="🤖",
    layout="wide"
)

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

# Function to extract NRIC and Case Number
def extract_nric_case(text):
    nric_pattern = r'\b[STFG]\d{7}[A-Z]\b'
    case_pattern = r'\bTX\d{3}\b'

    nric_match = re.search(nric_pattern, text, re.IGNORECASE)
    case_match = re.search(case_pattern, text, re.IGNORECASE)

    return nric_match.group(0).upper() if nric_match else None, case_match.group(0).upper() if case_match else None

# Function to extract bank name
def extract_bank_name(text):
    text_upper = text.upper()
    for bank in BANK_EMAIL_MAPPING.keys():
        if bank in text_upper:
            return bank
    return None

# Function to load tax records
def load_tax_records(nric, case_number):
    try:
        df = pd.read_csv("data/tax_records.csv")
        filtered_df = df[(df['NRIC'] == nric) & (df['Case_Number'] == case_number)]

        if not filtered_df.empty:
            columns_to_drop = ['NRIC', 'Case_Number']
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
        # Get SMTP configuration
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")

        # Debug: Check email configuration
        print(f"[EMAIL DEBUG] SMTP Server: {smtp_server}")
        print(f"[EMAIL DEBUG] SMTP Port: {smtp_port}")
        print(f"[EMAIL DEBUG] Sender Email: {sender_email}")
        print(f"[EMAIL DEBUG] Password configured: {'Yes' if sender_password else 'No'}")
        print(f"[EMAIL DEBUG] Bank Name: {bank_name}")

        # Determine recipient bank email
        if bank_name and bank_name in BANK_EMAIL_MAPPING:
            bank_email = BANK_EMAIL_MAPPING[bank_name]
            print(f"[EMAIL DEBUG] Bank email from mapping: {bank_email}")
        else:
            bank_email = "yumgiraffeyum@gmail.com"
            print(f"[EMAIL DEBUG] Using default bank email: {bank_email}")

        # Validate email configuration
        if not sender_email or not sender_password:
            error_msg = "⚠️ Email configuration not found. Please configure SENDER_EMAIL and SENDER_PASSWORD in .env file."
            print(f"[EMAIL DEBUG ERROR] {error_msg}")
            st.error(error_msg)
            return False, None

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = bank_email
        msg['Subject'] = f"IRAS Bank Appointment Release Notice - {nric} ({case_number})"
        
        current_date = datetime.now().strftime("%d %B %Y")
        current_time = datetime.now().strftime("%H:%M:%S")

        email_body = f"""
        Dear Bank Officer,

        This is an official notification from the Inland Revenue Authority of Singapore (IRAS) regarding a Bank Appointment Release request.

        [SUBJECT LINE]: BANK APPOINTMENT RELEASE NOTICE

        [DOCUMENT INFORMATION]
        Reference Number: IRAS-BankAppt-{case_number}
        Date of Issue: {current_date}
        Time of Issue: {current_time}
        Issuing Authority: Inland Revenue Authority of Singapore (IRAS)

        [CASE DETAILS FROM AI SUMMARY - only include the BANK APPOINTMENT INFORMATION, FUND AVAILABILITY and VERIFICATION parts of the summary]
        {summary}

        [AUTHORIZATION STATEMENT]: OFFICIAL AUTHORIZATION

        This release notice authorizes {bank_name if bank_name else "the bank"} to proceed with releasing the affected account(s) for the above-referenced taxpayer.

        Verification Status:
            - Taxpayer identity confirmed
            - Tax liabilities verified as settled
            - Bank account details validated
            - Release conditions met

        [ACTION REQUIRED FROM BANK]
        Please take the following actions:
        1. Process this bank appointment release at your earliest convenience
        2. Restore the affected account(s) to normal operation
        3. Notify the account holder once the release has been completed
        4. Send a confirmation to IRAS upon completion

        [CONTACT INFORMATION]
        For any queries regarding this notice, please contact IRAS:
        • Phone: {IRAS_CONTACT_PHONE}
        • Email: {IRAS_CONTACT_EMAIL}
        • Website: {IRAS_WEBSITE}
        • Operating Hours: {IRAS_OPERATING_HOURS}

        [IMPORTANT NOTES]
        • This is an official communication from IRAS
        • Please verify the authenticity of this notice if required
        • Retain this notice for your records

        [CLOSING]
        Thank you for your prompt attention to this matter.

        Yours sincerely,
        Inland Revenue Authority of Singapore (IRAS)

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        [AUTOMATED SYSTEM FOOTER]
        This is an automated notification from IRAS Tax Buddy System.
        Generated on: {current_date} at {current_time}
        Reference: IRAS-BankAppt-{case_number}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        [DISCLAIMER]
        CONFIDENTIALITY NOTICE: This email and any attachments are confidential and intended solely for the addressee.
        If you are not the intended recipient, please delete this email and notify the sender immediately.
        """

        msg.attach(MIMEText(email_body, 'plain'))

        # Send email with detailed logging
        print(f"[EMAIL DEBUG] Attempting to send email...")
        print(f"[EMAIL DEBUG] From: {sender_email}")
        print(f"[EMAIL DEBUG] To: {bank_email}")
        print(f"[EMAIL DEBUG] Subject: {msg['Subject']}")

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            print(f"[EMAIL DEBUG] Connected to SMTP server")
            server.starttls()
            print(f"[EMAIL DEBUG] TLS started")
            server.login(sender_email, sender_password)
            print(f"[EMAIL DEBUG] Login successful")
            server.send_message(msg)
            print(f"[EMAIL DEBUG] Email sent successfully!")

        print(f"[EMAIL DEBUG] ✓ Email sent to {bank_email}")
        return True, bank_email

    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"❌ SMTP Authentication failed. Please check your SENDER_EMAIL and SENDER_PASSWORD in .env file. Error: {str(e)}"
        print(f"[EMAIL DEBUG ERROR] {error_msg}")
        st.error(error_msg)
        return False, None
    except smtplib.SMTPException as e:
        error_msg = f"❌ SMTP error occurred: {str(e)}"
        print(f"[EMAIL DEBUG ERROR] {error_msg}")
        st.error(error_msg)
        return False, None
    except Exception as e:
        error_msg = f"❌ Failed to send email notification: {str(e)}"
        print(f"[EMAIL DEBUG ERROR] {error_msg}")
        st.error(error_msg)
        return False, None

# Display chat history in a scrollable container with fixed height
with st.container(height=400, border=True):
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

with st.form(key=f"chat_form_{st.session_state.input_key}", clear_on_submit=True):
    input_col1, input_col2 = st.columns([0.92, 0.08])

    with input_col1:
        user_input = st.text_input("Your message:", placeholder="What would you like to know?", label_visibility="collapsed", key=f"chat_input_{st.session_state.input_key}")

    with input_col2:
        send_button = st.form_submit_button("▶", use_container_width=True)

if send_button and user_input:
    extracted_nric, extracted_case = extract_nric_case(user_input)
    if extracted_nric:
        st.session_state.nric = extracted_nric
    if extracted_case:
        st.session_state.case_number = extracted_case

    # Always load fresh tax records from CSV when NRIC and Case Number are available
    # This ensures the AI receives the latest data for its responses
    if st.session_state.nric and st.session_state.case_number:
        st.session_state.tax_records = load_tax_records(st.session_state.nric, st.session_state.case_number)

    # Extract bank name from user input
    extracted_bank = extract_bank_name(user_input)
    if extracted_bank:
        st.session_state.bank_name = extracted_bank

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Load SOP content for bank appointment release process
    try:
        sop_content = ""
        try:
            with open("SOP.txt", "r") as f:
                sop_content = f.read()
        except:
            pass

        system_message = """You are IRAS Tax Buddy, a helpful assistant for Individual Income Tax (IIT) related questions in Singapore.
        SCOPE: You handle IIT (Individual Income Tax) bank appointment cases only. Taxpayers are transferred to you after IVR triaging.
        
        You can help users with:
        - General tax questions and information
        - Understanding tax assessments and payments
        - IRAS procedures and requirements
        - Tax filing guidance
        - Bank Appointment Release Process (IIT only)

        When users mention their NRIC or Case Number, acknowledge it naturally and let them know their details will be auto-filled in the My Tax Portal section below.
        Also, verify with the users that the tax type that they are enquiring is IIT.
        
        === BANK APPOINTMENT RELEASE PROCESS (IIT ONLY) ===

        STEP 1: TAXPAYER VERIFICATION AND INFORMATION DISCLOSURE
        ---------------------------------------------------------
        When a user provides their NRIC and case number (or requests bank appointment release):

        A. Identity Verification:
        - The system automatically extracts and verifies NRIC and case number
        - Acknowledge receipt: "Hello! Thank you for providing your NRIC and case number."

        B. Mandatory Information Disclosure (CRITICAL - DO THIS IMMEDIATELY):

        TRIGGER: If you see "CURRENT TAX RECORDS FOR USER" section in the system context below, this means the tax records have been loaded successfully.

        ACTION: You MUST IMMEDIATELY disclose the following information WITHOUT waiting for further user input:

        1. Check if BANK APPOINTMENT DETAILS section exists in the system context:
           - If YES: This user has a bank appointment, proceed with disclosure
           - If NO: Inform user they don't have an active bank appointment

        2. Use the ACTUAL data from "BANK APPOINTMENT DETAILS" and "TAX LIABILITY SUMMARY" sections provided in the system context

        3. Disclose IMMEDIATELY (in your first response after seeing their NRIC):
           - The FULL tax liability amount for the Year of Assessment
           - The Bank Appointment Information:
             * Appointed Bank name (from BANK APPOINTMENT DETAILS)
             * Appointment Amount earmarked (from BANK APPOINTMENT DETAILS)
             * Date of appointment (from BANK APPOINTMENT DETAILS)
             * Year of Assessment (from BANK APPOINTMENT DETAILS)

        CRITICAL: Do NOT say "Let me check" or "One moment please" and then stop. IMMEDIATELY provide the disclosure in the same response.

        Required Disclosure Format (use actual data, NOT placeholders):

        "Hello! Thank you for providing your NRIC and case number. I've retrieved your tax information.

        I can see you have a bank appointment with [Appointed Bank] for [Appointment Amount] made on [Appointment Date] for YA [Year of Assessment]. Your total tax liability for YA [Year of Assessment] is [Total Payable], and your current outstanding balance is [Current Balance].

        Would you like to proceed with the bank appointment release process?"

        Example with real data:
        "Hello! Thank you for providing your NRIC and case number. I've retrieved your tax information.

        I can see you have a bank appointment with DBS for S$750.00 made on 25 Mar 2025 for YA 2025. Your total tax liability for YA 2025 is S$1250.00, and your current outstanding balance is S$0.00.

        Would you like to proceed with the bank appointment release process?"

        STEP 2: FUND AVAILABILITY ASSESSMENT
        -------------------------------------
        CRITICAL - You MUST ask this question using the ACTUAL values from the BANK APPOINTMENT DETAILS provided:

        "Do you currently have the full appointment amount of [Appointment Amount] available in your [Appointed Bank] account?"

        Example with real data: "Do you currently have the full appointment amount of S$750.00 available in your DBS account?"

        - If user answers "NO" or indicates insufficient funds:
            -> REJECT the request immediately
            -> Response: "We are unable to proceed with the bank appointment release at this time as the full appointment amount is not available in your account. To explore alternative payment arrangements, please provide your contact details (mobile number or email address). An IRAS officer will reach out to you within the next three working days."
            -> DO NOT proceed further
            -> DO NOT include "BANK_APPOINTMENT_RELEASE_APPROVED"

        - If user answers "YES":
            -> Proceed to Step 3

        STEP 3: BANK ACCOUNT CONFIRMATION
        ----------------------------------
        If funds are available, proceed with:

        A. Request Bank Account Confirmation: "Please confirm the bank account that contains the full funds for settlement. Which bank is this account with?"

        B. Verification:
            - Check if the bank mentioned matches the Appointed Bank in their records
            - If mismatch: Ask for clarification
            - Request last 4 digits of account number for verification

        STEP 4: RELEASE DETERMINATION AND SUMMARY GENERATION
        -----------------------------------------------------
        Once all information is collected, you MUST make a determination:

        APPROVAL CONDITIONS (ALL must be met):
        1. Tax liability Balance = 0 (fully settled) OR full payment confirmation provided
        2. User confirms full appointment amount is available in their account
        3. Bank account matches the Appointed Bank
        4. All required information collected (NRIC, bank info, account details)

        If ALL conditions are met:
            -> Generate a COMPREHENSIVE SUMMARY (see format below)
            -> Include the exact phrase, "BANK_APPOINTMENT_RELEASE_APPROVED"
            -> Inform user that the release process will be initiated
            -> Explain next steps (IRAS will notify the bank, account will be released)

        If conditions are NOT met:
            -> Generate a COMPREHENSIVE SUMMARY explaining what is missing
            -> DO NOT include "BANK_APPOINTMENT_RELEASE_APPROVED"
            -> Clearly state why the release cannot proceed
            -> Guide user on what they need to do next (Ensure sufficient amount in the bank account and attempt for bank appointment release again, OR leave contact details for an IRAS officer to reach out to the user for alternative arrangement)

        SUMMARY FORMAT (CRITICAL - ALWAYS GENERATE THIS):
        =================================================
        When making a final determination, provide a structured summary using ACTUAL DATA from the system context:

        "
        Thank you for your cooperation.
        Your request for bank appointment release is [APPROVED/REJECTED]
        REASON: [Explanation]
        
        Let me provide a summary of this case:

        CASE DETAILS:
        - NRIC: [NRIC]
        - Case Number: [Case Number]
        - Year of Assessment: [YA]

        BANK APPOINTMENT INFORMATION:
        - Appointed Bank: [Bank Name]
        - Appointment Amount: S$[Amount]
        - Appointment Date: [Date]

        TAX LIABILITY STATUS:
        - Total Payable: S$[Amount]
        - Total Paid: S$[Amount]
        - Current Balance: S$[Amount]

        FUND AVAILABILITY:
        - User confirmed [YES/NO] to having full appointment amount available

        VERIFICATION:
        - Bank Account Confirmed: [Bank Name]
        - Account Details: [Last 4 digits if provided]

        [If approved: Include BANK_APPOINTMENT_RELEASE_APPROVED keyword]
        [If approved: Explain next steps - email sent to bank, account will be released]
        [If rejected: Explain what is missing and what user needs to do]"

        CONVERSATIONAL APPROACH (MIMIC HUMAN INTERACTION):
        - Ask for information one question at a time, like a human would
        - Do not list multiple questions in a single response
        - Keep your questions natural and conversational, in a professional yet friendly tone
        - Wait for the user's answer before asking the next question
        - Acknowledge their answer before moving to the next question
        - Track what information has been provided, so that the same question is not asked multiple times
        - Follow the format provided, especially for the summary at the end of interaction 
        - Use the same font throughout all responses

        REJECTION SCENARIOS:
        - Insufficient funds: User says they don't have full amount
        - Incomplete records: Cannot load tax records
        - Missing information: Required details not provided
        - Unresolved balance: Tax liability not fully settled and no payment evidence
        - Bank mismatch: User's bank doesn't match appointed bank
        """

        if st.session_state.tax_records is not None and not st.session_state.tax_records.empty:
            bank_appt_info = ""
            try:
                df = pd.read_csv("data/tax_records.csv")
                filtered_df = df[(df['NRIC'] == st.session_state.nric) & (df['Case_Number'] == st.session_state.case_number)]
                if not filtered_df.empty:
                    # Get appointment details
                    appointments = filtered_df[filtered_df['Bank_Appointment_Date'].notna() & (filtered_df['Bank_Appointment_Date'] != '')]
                    if not appointments.empty:
                        appt_row = appointments.iloc[-1]
                        appt_bank = appt_row['Appointed_Bank'] if pd.notna(appt_row.get('Appointed_Bank')) else 'N/A'
                        appt_amount = f"S${appt_row['Appointment_Amount']:.2f}" if pd.notna(appt_row.get('Appointment_Amount')) else 'N/A'

                        bank_appt_info = f"""
                        BANK APPOINTMENT DETAILS:
                        - Appointed Bank: {appt_bank}
                        - Appointment Amount: {appt_amount}
                        - Appointment Date: {appt_row['Bank_Appointment_Date']}
                        - Year of Assessment: {appt_row['Year_of_Assessment']}
                        """

                    # Get tax liability summary
                    total_payable = filtered_df['Payable'].sum()
                    total_paid = filtered_df['Paid'].sum()
                    current_balance = filtered_df['Balance'].iloc[-1]

                    tax_summary = f"""
                    ===================================================================
                    CURRENT TAX RECORDS FOR USER (NRIC: {st.session_state.nric}, Case: {st.session_state.case_number}):

                    TAX LIABILITY SUMMARY:
                    - Total Payable: S${total_payable:.2f}
                    - Total Paid: S${total_paid:.2f}
                    - Current Balance: S${current_balance:.2f}
                    {bank_appt_info}

                    IMPORTANT INSTRUCTIONS:
                    - Use exact values when disclosing information to the user
                    - When stating "I can see you have a bank appointment with...", use the values from BANK APPOINTMENT DETAILS above
                    - When stating "Your total tax liability...", use the Total Payable value from TAX LIABILITY SUMMARY above
                    - When asking about fund availability, use the Appointment Amount from BANK APPOINTMENT DETAILS above
                    - Use the actual data provided above, not the placeholders like [Amount] or [Bank Name]
                    ===================================================================
                    """
                    system_message += tax_summary
            except:
                tax_summary = f"\n\nThe user has loaded their tax records for NRIC {st.session_state.nric} (Case {st.session_state.case_number}). You can reference their tax information if relevant to their questions."
                system_message += tax_summary

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

        # Debug: Check AI response
        print(f"[APPROVAL DEBUG] Checking AI response for approval keyword...")
        print(f"[APPROVAL DEBUG] Response contains 'BANK_APPOINTMENT_RELEASE_APPROVED': {'BANK_APPOINTMENT_RELEASE_APPROVED' in full_response}")

        # Check if AI approved the bank appointment release
        if "BANK_APPOINTMENT_RELEASE_APPROVED" in full_response:
            print(f"[APPROVAL DEBUG] ✓ Approval keyword detected!")
            st.session_state.bank_appointment_release_approved = True

            # Store the summary for email
            st.session_state.release_summary = full_response.replace("BANK_APPOINTMENT_RELEASE_APPROVED", "").strip()
            full_response = full_response.replace("BANK_APPOINTMENT_RELEASE_APPROVED", "").strip()

            print(f"[APPROVAL DEBUG] Email sent status: {st.session_state.email_sent}")
            print(f"[APPROVAL DEBUG] NRIC: {st.session_state.nric}")
            print(f"[APPROVAL DEBUG] Case Number: {st.session_state.case_number}")
            print(f"[APPROVAL DEBUG] Bank Name: {st.session_state.bank_name}")

            # Send email to bank
            if not st.session_state.email_sent and st.session_state.nric and st.session_state.case_number:
                print(f"[APPROVAL DEBUG] Initiating email send...")
                email_sent, bank_email = send_bank_release_email(
                    st.session_state.release_summary,
                    st.session_state.nric,
                    st.session_state.case_number,
                    st.session_state.bank_name
                )
                if email_sent:
                    st.session_state.email_sent = True
                    bank_display = f"{st.session_state.bank_name} ({bank_email})" if st.session_state.bank_name else bank_email
                    print(f"[APPROVAL DEBUG] ✓ Email sent successfully to {bank_display}")
                    st.success(f"✉️ Bank appointment release notice sent to {bank_display}")
                else:
                    print(f"[APPROVAL DEBUG] ✗ Email sending failed")
            else:
                print(f"[APPROVAL DEBUG] Email not sent - Conditions not met:")
                print(f"  - Email already sent: {st.session_state.email_sent}")
                print(f"  - NRIC present: {bool(st.session_state.nric)}")
                print(f"  - Case Number present: {bool(st.session_state.case_number)}")
        else:
            print(f"[APPROVAL DEBUG] ✗ Approval keyword NOT detected in response")

        extracted_nric, extracted_case = extract_nric_case(full_response)
        if extracted_nric:
            st.session_state.nric = extracted_nric
        if extracted_case:
            st.session_state.case_number = extracted_case
            
        extracted_bank = extract_bank_name(full_response)
        if extracted_bank:
            st.session_state.bank_name = extracted_bank

    except Exception as e:
        error_message = f"Error: {str(e)}"
        if "api_key" in str(e).lower():
            error_message = "⚠️ OpenAI API key not found or invalid. Please check your .env file."
        full_response = error_message

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

# Auto-fetch fresh tax records from CSV whenever NRIC and Case Number are available
# This ensures the latest data from the CSV file is always displayed
if st.session_state.nric and st.session_state.case_number:
    st.session_state.tax_records = load_tax_records(st.session_state.nric, st.session_state.case_number)

# Display NRIC and Case Number
if st.session_state.nric and st.session_state.case_number:
    bank_appointment_date = None
    appointed_bank = None
    appointment_amount = None

    if st.session_state.tax_records is not None:
        try:
            df = pd.read_csv("data/tax_records.csv")
            filtered_df = df[(df['NRIC'] == st.session_state.nric) & (df['Case_Number'] == st.session_state.case_number)]
            if not filtered_df.empty:
                # Get the most recent bank appointment
                if 'Bank_Appointment_Date' in filtered_df.columns:
                    appointments = filtered_df[filtered_df['Bank_Appointment_Date'].notna() & (filtered_df['Bank_Appointment_Date'] != '')]
                    if not appointments.empty:
                        bank_appointment_date = appointments.iloc[-1]['Bank_Appointment_Date']

                        # Get appointed bank and amount
                        if 'Appointed_Bank' in appointments.columns:
                            appointed_bank = appointments.iloc[-1]['Appointed_Bank']
                        if 'Appointment_Amount' in appointments.columns:
                            appointment_amount = appointments.iloc[-1]['Appointment_Amount']
        except:
            pass

    # Show actual values when NRIC and Case Number are provided
    bank_appointment_html = ""
    if st.session_state.bank_appointment_release_approved:
        bank_info = f"{appointed_bank}" if appointed_bank and pd.notna(appointed_bank) else "N/A"
        amount_info = f"S${appointment_amount:.2f}" if appointment_amount and pd.notna(appointment_amount) else "N/A"

        bank_appointment_html = f"""<br><strong>Bank Appointment Date:</strong> {bank_appointment_date if bank_appointment_date else 'N/A'}
        <br><strong>Appointed Bank:</strong> {bank_info}
        <br><strong>Appointment Amount:</strong> {amount_info}
        <br><strong style="color: #28a745;">Bank Appointment Release:</strong> <span style="color: #28a745;">In Progress ✓</span>"""
    elif bank_appointment_date:
        bank_info = f"{appointed_bank}" if appointed_bank and pd.notna(appointed_bank) else "N/A"
        amount_info = f"S${appointment_amount:.2f}" if appointment_amount and pd.notna(appointment_amount) else "N/A"

        bank_appointment_html = f"""<br><strong>Bank Appointment Date:</strong> {bank_appointment_date}
        <br><strong>Appointed Bank:</strong> {bank_info}
        <br><strong>Appointment Amount:</strong> {amount_info}"""
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
        <br><strong>Bank Appointment Status:</strong> _________
    </div>
    """, unsafe_allow_html=True)

# Display tax records table
if st.session_state.tax_records is not None:
    st.markdown("### Tax Assessment Records")
    
    display_df = st.session_state.tax_records.copy()

    if 'Payable' in display_df.columns:
        display_df['Payable (S$)'] = display_df['Payable'].apply(lambda x: f"{x:.2f}")
        display_df = display_df.drop('Payable', axis=1)

    if 'Paid' in display_df.columns:
        display_df['Paid (S$)'] = display_df['Paid'].apply(lambda x: f"{x:.2f}")
        display_df = display_df.drop('Paid', axis=1)

    if 'Balance' in display_df.columns:
        display_df['Balance (S$)'] = display_df['Balance'].apply(lambda x: f"{x:.2f}")
        display_df = display_df.drop('Balance', axis=1)

    if 'Appointment_Amount' in display_df.columns:
        display_df['Appointment Amount (S$)'] = display_df['Appointment_Amount'].apply(
            lambda x: f"{x:.2f}" if pd.notna(x) and x != '' else ''
        )
        display_df = display_df.drop('Appointment_Amount', axis=1)

    column_order = [
        'Date',
        'Description',
        'Year_of_Assessment',
        'Payable (S$)',
        'Paid (S$)',
        'Balance (S$)',
        'Bank_Appointment_Date',
        'Appointed_Bank',
        'Appointment Amount (S$)'
    ]
    display_df = display_df[[col for col in column_order if col in display_df.columns]]

    display_df = display_df.rename(columns={
        'Year_of_Assessment': 'Year of Assessment',
        'Bank_Appointment_Date': 'Bank Appt Date',
        'Appointed_Bank': 'Appointed Bank'
    })

    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
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
