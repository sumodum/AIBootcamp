import streamlit as st

# Page configuration
st.set_page_config(
    page_title="About Us - AI Bootcamp",
    page_icon="👥",
    layout="wide"
)

# Title
st.title("👥 About Us")

# Introduction
st.markdown("""
## Welcome to AI Bootcamp

AI Bootcamp is dedicated to making artificial intelligence accessible and understandable
to everyone. Our mission is to provide cutting-edge AI tools and educational resources
that empower individuals and organizations to harness the power of AI technology.
""")

# Mission & Vision
col1, col2 = st.columns(2)

with col1:
    st.header("🎯 Our Mission")
    st.markdown("""
    To democratize access to AI technology by providing intuitive, powerful tools
    that anyone can use, regardless of their technical background.

    We believe that AI should be:
    - **Accessible** - Easy to use for everyone
    - **Transparent** - Clear about how it works
    - **Helpful** - Solving real-world problems
    - **Ethical** - Used responsibly and fairly
    """)

with col2:
    st.header("🔭 Our Vision")
    st.markdown("""
    To create a world where AI technology enhances human capabilities and creativity,
    helping people work smarter, learn faster, and achieve more.

    We envision a future where:
    - AI assists in everyday tasks
    - Learning is personalized and effective
    - Innovation is accelerated
    - Human potential is amplified
    """)

# What We Offer
st.header("💡 What We Offer")

st.markdown("""
### AI-Powered Chatbot
Our flagship feature is an intelligent chatbot powered by OpenAI's GPT-3.5 Turbo,
providing you with:
- Instant answers to your questions
- Creative problem-solving assistance
- Learning support across various topics
- Professional writing and editing help
- And much more!

### Educational Resources
We're committed to helping you understand AI technology through:
- Clear explanations of how our tools work
- Best practices for AI interaction
- Tips for getting the most out of AI assistants
- Transparent methodology and limitations
""")

# Team Section (placeholder)
st.header("👨‍👩‍👧‍👦 Our Team")
st.markdown("""
AI Bootcamp is built by a passionate team dedicated to making AI technology
accessible and beneficial for all.

*[Team information can be customized here]*
""")

# Contact
st.header("📧 Get in Touch")
st.markdown("""
We'd love to hear from you! Whether you have questions, feedback, or just want
to say hello, feel free to reach out.

*[Contact information can be added here]*
""")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & OpenAI")
