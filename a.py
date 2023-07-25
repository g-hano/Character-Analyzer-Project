import base64

from transformers import pipeline
import json
import streamlit as st

summarize = pipeline('summarization', model="facebook/bart-large-cnn")

with open("questions.json", "r", encoding="utf-8") as file:
    questions_data = json.load(file)

def show_question(question_data):
    st.write(question_data["question"])
    selected_option = st.radio("Options", question_data["options"])
    return selected_option

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Character Analyzer",
        page_icon=":heart:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    with st.container():
        st.title("Guessing Your Personality👨‍👩‍👦")

    set_background("image.jpg")

    # Create a two-column layout for the buttons
    col1, col2 = st.columns(2)

    # Initialize an index to keep track of the current question
    question_index = st.session_state.get("question_index", 0)
    answers = st.session_state.get("answers", [])

    if len(answers) <= question_index:
        selected_option = show_question(questions_data[question_index])
    else:
        selected_option = None

    # Show the current question if answers to previous questions have been given
    if len(answers) > question_index:
        show_question(questions_data[question_index])


    if selected_option is not None:
        answers.append(selected_option)
        st.session_state["answers"] = answers

    st.empty()  # Empty space to align the buttons

    # Handle navigation and save answers
    with col1:
        if st.button("Previous") and question_index > 0:
            question_index -= 1
            st.session_state["question_index"] = question_index

    with col2:
        if selected_option is not None:
            answers.append(selected_option)
            st.session_state["answers"] = answers
        if st.button("Next") and question_index < len(questions_data) - 1:
            question_index += 1
            st.session_state["question_index"] = question_index

    ARTICLE = st.text_area("What do you do in your spare time? What are your hobbies? (up to 450 characters)", max_chars=450)

    # Add the "Send" button
    if st.button("Send"):
        # Check if ARTICLE is not empty before summarizing
        if ARTICLE.strip():
            summary = summarize(ARTICLE, max_length=int(len(ARTICLE) / 3), min_length=0, do_sample=False)
        else:
            summary = ""
        st.write("\nSummary:", summary)



if __name__ == "__main__":
    main()
