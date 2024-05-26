# Import the required libraries
import streamlit as st
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.tools.arxiv_toolkit import ArxivToolkit
import streamlit_shadcn_ui as ui

# Initialize session state for the input area if not already done
if 'openai_access_token' not in st.session_state:
    st.session_state.openai_access_token = ""
if 'query' not in st.session_state:
    st.session_state.query = ""

# Function to clear the input area
def clear_input():
    st.session_state.query = ""

# Set up the Streamlit app
st.title("Research you Desired Topic with Arxiv 🤖")
st.caption("This app allows you to chat with arXiv using OpenAI GPT-4 model. You'll be provided with citations from the pages visted and resources given")

# Get OpenAI API key from user
st.session_state.openai_access_token = st.text_input("OpenAI API Key", type="password")

clicked = ui.button("Submit your Topic", key="clk_btn")
reset_clicked = ui.button("Reset", key="reset_btn")

# If reset button is clicked, clear the input area
if reset_clicked:
    clear_input()

st.write("UI Button Clicked:", clicked)

# If OpenAI API key is provided, create an instance of Assistant
if st.session_state.openai_access_token:
    # Create an instance of the Assistant
    assistant = Assistant(
        llm=OpenAIChat(
            model="gpt-4",
            max_tokens=1024,
            temperature=0.9,
            api_key=st.session_state.openai_access_token
        ), tools=[ArxivToolkit()], show_tool_calls=True
    )
    # Get the search query from the user
    st.session_state.query = st.text_input("Enter the Search Query", value=st.session_state.query, type="default")
    
    # If query is provided, run the AI Assistant
    if clicked and st.session_state.query:
        response = assistant.run(st.session_state.query, stream=True)
        st.write(response)
