import openai
import streamlit as st
import requests
from streamlit_option_menu import option_menu

# pip install streamlit-chat
from streamlit_chat import message


st.set_page_config(layout="wide")

openai.api_key = st.secrets["api_secret"]

messages = [{"role": "system",
             "content": "Give me full list of tasks for the following project and Explain things like you're a product manager and product owner with more than 6 years of "
                        "experience and has experience as fullstack developer, and you are talking to a software "
                        "professional with 2 years of experience."}]
# Creating the chatbot interface
st.title(":cyclone: :blue[_TasksGPT:_]")
st.header('**_ChatGPT_** for PMs & Product Owners')
st.divider()

with st.sidebar:
    selected = option_menu("Menu", ["TaskGPT", 'How it works', 'Future', 'About', 'Research'],
                           icons=['house', 'code-square', 'robot', 'info-square', 'book-half'], menu_icon="cast",
                           default_index=0)

if selected == 'TaskGPT':

    col1, col2, = st.columns([1, 2])

    with col1:
        def generate_response(prompt):
            messages.append({"role": "user", "content": prompt})
            print(messages)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", #text-davinci-002-render-sha
                messages=messages

            )
            print(response)
            message = response.choices[0]["message"]["content"]
            return message


        # Storing the chat
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []

        if 'past' not in st.session_state:
            st.session_state['past'] = []


        # We will get the user's input by calling the get_text function
        def get_text():

            input_text = st.text_input("You: ", placeholder="Hello, Let's create tasks for your project?", key="input")
            return input_text


        user_input = get_text()

        send = st.button('Send', use_container_width=True)

        options = st.multiselect(
            'Include more detais',
            ['Acceptance Criteria', 'Steps to build', 'Estimated Time'])
        if len(options) > 0:
            messages.append({"role": "user", "content": 'include in the response: ' + ' and '.join(str(option) for option in options) + 'for each task'})


        file = st.file_uploader('upload file')
    if user_input or send:
        output = generate_response(user_input)
        # store the output
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

        if st.session_state['generated']:
            with col2:
                for i in range(len(st.session_state['generated']) - 1, -1, -1):
                    message(st.session_state["generated"][i], key=str(i), avatar_style='icons')
                    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user', avatar_style='shapes')
