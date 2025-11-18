# AIBootcamp
A Streamlit-based web application featuring a ChatGPT-powered chatbot

## Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd AIBootcamp
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

5. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```

## Running the Application

1. Make sure your virtual environment is activated:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Start the Streamlit server:
```bash
streamlit run app.py
```

3. The application will automatically open in your browser at `http://localhost:8501`
If it doesn't open automatically, you can manually navigate to `http://localhost:8501` in your web browser