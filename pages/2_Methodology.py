import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Methodology - AI Bootcamp",
    page_icon="🔬",
    layout="wide"
)

# Title
st.title("🔬 Methodology")

# Introduction
st.markdown("""
## How Our AI Chatbot Works

Understanding the technology behind our chatbot helps you get the most out of it.
This page explains our approach, the technology we use, and best practices for
interaction.
""")

# Technology Overview
st.header("🤖 Technology Stack")

col1, col2 = st.columns(2)

with col1:
    st.subheader("OpenAI GPT-3.5 Turbo")
    st.markdown("""
    Our chatbot is powered by OpenAI's GPT-3.5 Turbo, a state-of-the-art
    large language model that:

    - Understands and generates human-like text
    - Has been trained on diverse internet text
    - Can handle a wide variety of tasks
    - Responds in real-time with streaming output
    """)

with col2:
    st.subheader("Streamlit Framework")
    st.markdown("""
    The user interface is built with Streamlit, which provides:

    - Clean, intuitive design
    - Real-time interaction
    - Responsive layout
    - Session state management for conversation history
    """)

# How It Works
st.header("⚙️ How It Works")

st.markdown("""
### The Process Flow

1. **You Ask a Question**
   - You type your question or prompt in the chat input
   - The message is sent to our system

2. **Context Assembly**
   - Your current message is combined with previous conversation history
   - This provides context for more coherent responses

3. **AI Processing**
   - The conversation is sent to OpenAI's GPT-3.5 Turbo model
   - The AI analyzes the context and generates a response
   - Temperature setting (0.7) balances creativity and consistency

4. **Streaming Response**
   - The response is streamed back in real-time
   - You see the answer appear word by word
   - The full response is saved to conversation history

5. **Continuous Conversation**
   - Each exchange builds on previous messages
   - The chatbot maintains context throughout the session
   - You can ask follow-up questions naturally
""")

# Configuration
st.header("🔧 Configuration & Parameters")

st.markdown("""
### Model Settings

Our chatbot uses the following configuration:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| **Model** | gpt-3.5-turbo | The AI model powering responses |
| **Temperature** | 0.7 | Balances creativity (higher) vs consistency (lower) |
| **Max Tokens** | 1000 | Maximum length of each response |
| **Streaming** | Enabled | Real-time response display |

### What This Means

- **Temperature (0.7)**: Provides a good balance between creative, varied responses
  and consistent, focused answers
- **Max Tokens (1000)**: Allows detailed responses while maintaining reasonable
  response times
- **Streaming**: You see responses as they're generated, not all at once
""")

# Best Practices
st.header("💡 Best Practices")

st.markdown("""
### Getting the Best Results

To get the most helpful responses from our chatbot:

#### ✅ Do:
- **Be specific** - Clearly state what you need
- **Provide context** - Include relevant background information
- **Ask follow-ups** - Build on previous responses
- **Break down complex questions** - Ask step by step if needed
- **Experiment** - Try rephrasing if you don't get what you need

#### ❌ Avoid:
- **Vague questions** - "Tell me about stuff" is too broad
- **Expecting real-time data** - The model's knowledge has a cutoff date
- **Very long prompts** - Keep questions focused and manageable
- **Assuming context between sessions** - Each session starts fresh
""")

# Limitations
st.header("⚠️ Limitations & Considerations")

st.markdown("""
### What to Keep in Mind

While our chatbot is powerful, it has some limitations:

1. **Knowledge Cutoff**
   - The model was trained on data up to a specific date
   - It doesn't have real-time information or current events

2. **Not a Search Engine**
   - It generates responses based on patterns in training data
   - It may not always provide the most up-to-date information

3. **Context Window**
   - There's a limit to how much conversation history is maintained
   - Very long conversations may lose early context

4. **Accuracy**
   - While generally reliable, the AI can make mistakes
   - Always verify critical information from authoritative sources

5. **No Memory Between Sessions**
   - Each new session starts fresh
   - Previous conversations are not remembered
   - Use "Clear Chat History" to start a new conversation in the same session
""")

# Privacy & Data
st.header("🔒 Privacy & Data Handling")

st.markdown("""
### Your Data

- **Session-based**: Conversations are stored only in your browser session
- **Not persistent**: Chat history is cleared when you refresh or close the page
- **API Calls**: Messages are sent to OpenAI's API for processing
- **No Storage**: We don't store your conversations on our servers

For more information about OpenAI's data handling, please visit
[OpenAI's Privacy Policy](https://openai.com/policies/privacy-policy).
""")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & OpenAI")
