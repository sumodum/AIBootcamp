# Deployment Guide - Streamlit Community Cloud

## Prerequisites
1. A GitHub account
2. Code pushed to a GitHub repository
3. A Streamlit Community Cloud account

## Step-by-Step Deployment Instructions
1. Push your code to GitHub repository:
```bash
git add .
git commit -m "<commit_msg>"
git push origin main
```

2. Set up Streamlit Community Cloud:
   1. Go to https://streamlit.io/cloud
   2. Click "Sign up" and sign in with your GitHub account
   3. Authorise Streamlit to access your GitHub repositories

3. Prepare for app deployment:
   1. Click "New app" in the Streamlit Cloud dashboard
   2. Select:
      - **Repository**: Choose your GitHub repository (AIBootcamp)
      - **Branch**: main
      - **Main file path**: app.py
   3. Click "Advanced settings" before deploying

4. Configure secrets:
In the "Advanced settings" section, add the environment variables as secrets:

   1. In the "Secrets" text box, paste the following format:

   ```toml
   # OpenAI API Configuration
   OPENAI_API_KEY = "your_openai_api_key"

   # App Password Protection
   APP_PASSWORD = "your_chosen_password"

   # Email Configuration
   SMTP_SERVER = "smtp.gmail.com"
   SMTP_PORT = 587
   SENDER_EMAIL = "your_gmail_address"
   SENDER_PASSWORD = "your_gmail_app_password"

   # Bank Email Mappings
   BANK_EMAILS = "UOB:yumgiraffeyum@gmail.com,DBS:yumgiraffeyum@gmail.com,OCBC:yumgiraffeyum@gmail.com,HSBC:yumgiraffeyum@gmail.com"

   # IRAS Contact Information
   IRAS_CONTACT_PHONE = "(+65) 6356 7012"
   IRAS_CONTACT_EMAIL = "tax_support@iras.gov.sg"
   IRAS_WEBSITE = "www.iras.gov.sg"
   IRAS_OPERATING_HOURS = "Mondays to Fridays (8 a.m. to 5 p.m.)"
   ```

   2. **Replace the placeholder values** with the actual credentials:
      - `your_openai_api_key` → Your OpenAI API key
      - `your_chosen_password` → The password users will need to access the app
      - `your_gmail_address` → Your Gmail address
      - `your_gmail_app_password` → Your Gmail App Password (16-character code)

   3. Click "Save"

5. Deploy the app:
   1. Click "Deploy"
   2. Wait for the app to build and deploy
   3. Once deployed, a public URL will be generated


6. Test the deployed app with the URL
   1. Visit the app URL
   2. You should see a password login screen
   3. Enter the password you configured in `APP_PASSWORD`
   4. Test the functionalities