from dotenv import load_dotenv
load_dotenv()  # loading all the environment variables
import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=False)
    return response

# Function to extract text from the response
def extract_text_from_response(response):
    if hasattr(response, 'candidates'):
        for candidate in response.candidates:
            if hasattr(candidate, 'content'):
                for part in candidate.content.parts:
                    if hasattr(part, 'text'):
                        return part.text
    return "No text found in the response"

# Initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    # Add user query to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    
    response_text = extract_text_from_response(response)
    st.write(response_text)
    st.session_state['chat_history'].append(("Bot", response_text))

st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

# Print version information
st.write(f"google-generativeai version: {genai.__version__}")

    
