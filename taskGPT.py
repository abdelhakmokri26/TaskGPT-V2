import openai
import streamlit as st
import requests
from streamlit_option_menu import option_menu

# pip install streamlit-chat
from streamlit_chat import message
import json

st.set_page_config(layout="wide")

openai.api_key = st.secrets["api_secret"]

with open('about.txt', 'r') as file:
    # Load the JSON data
    about = file.read()

with open('how_it_works.txt', 'r') as file:
    # Load the JSON data
    how_it_works = file.read()

with open('future.txt', 'r') as file:
    # Load the JSON data
    future = file.read()


with open('frameworks.json', 'r') as file:
    # Load the JSON data
    frameworks = json.load(file)

messages = [{"role": "system",
            "content": "Provide full detailed of the following information about the [task or user story]: Task/user story, Description of the task/user story, Estimated effort required, Due datelists, and Explain things like you're a product manager and product owner. Additionally, please provide any relevant notes or comments that may be useful for completing the task or user story. Ideally, I'd like these details to be provided in an easy-to-read format, such as a table or list. I'd also like the information to be up-to-date and accurate, If I need details on a specific user story or task, I'll provide you with the task name. Please let me know if you need any additional information or context to provide these details. "}]


# Creating the chatbot interface
st.title(":cyclone: :blue[_TasksGPT:_]")
st.header('**_ChatGPT_** for PMs & Product Owners')
st.divider()

with st.sidebar:
    selected = option_menu("Menu", ["TaskGPT", 'How it works', 'Demo', 'Vision', 'About', 'Research'],
                           icons=['house', 'code-square', 'file-earmark-play', 'robot', 'info-square', 'book-half'], menu_icon="cast",
                           default_index=0)

if selected == 'TaskGPT':

    col1, col2, = st.columns([1, 2])

    with col1:
        def generate_response(prompt):
            messages.append({"role": "user", "content": prompt})
            print(messages)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # text-davinci-002-render-sha
                messages=messages,
            )

            message = response.choices[0]['message']["content"]

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
            messages.append({"role": "user", "content": 'include in the response: ' + ' and '.join(
                str(option) for option in options) + 'for each task'})

        platform_options = st.selectbox('Choose a platform', ('', 'Web', 'Mobile', 'Desktop'))
        project_managment = (pmt for pmt in [''] + frameworks["Project Managment"])

        project_management_tool = st.selectbox('Choose your project management tool', project_managment)
        functionality = st.selectbox('Functionality', ('', 'New feature', 'Upgrade', 'Reported issue', 'Bug'))
        print(project_management_tool)
        file = st.file_uploader('upload file')

        if project_management_tool != '':
            messages.append({"role": "user", "content": 'Create a ' + project_management_tool + ' like tasks for this ' + (functionality if functionality != '' else 'project:') })

        if platform_options != '':
            messages.append({"role": "user", "content": 'bare in mind that this a ' + platform_options + ' App'})

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

if selected == 'How it works':
    text = ":writing_hand: "+str(how_it_works)
    st.subheader(':warning: Note: This App is currently using ChatGPT API')
    st.divider()
    st.markdown(text)
    st.image("img/chatGPT-API.png")

if selected == 'Demo':
    st.subheader(':tv: Demo')
    st.divider()
    video_file = open('video.mp4', 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes)
    
    
if selected == 'Vision':
    text = str(future)
    st.subheader(':first_place_medal: Our Vision')
    st.divider()
    st.markdown(text)
    

if selected == 'About':
    text = str(about)
    st.subheader(':information_source: About')
    st.divider()
    st.markdown(text)

    st.write("[Contact Me](https://abdelhakmokri.pythonanywhere.com/contact/)")
