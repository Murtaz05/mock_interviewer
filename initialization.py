from gtts import gTTS
import os
import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq
from langchain_core.chat_history import InMemoryChatMessageHistory
from PyPDF2 import PdfReader
import tempfile
import pygame
from dotenv import load_dotenv
import speech_recognition as sr

if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []

if "response_input" not in st.session_state:
    st.session_state["response_input"] = ""

if "current_question" not in st.session_state:
    st.session_state["current_question"] = ""

if "interview_start" not in st.session_state:
    st.session_state["interview_start"] = False

if "details_submitted" not in st.session_state:
    st.session_state["details_submitted"] = False

if "response_received" not in st.session_state:
    st.session_state["response_received"] = False

if "question_asked" not in st.session_state:
    st.session_state["question_asked"] = False

if "interview_concluded" not in st.session_state:
    st.session_state["interview_concluded"] = False

if "new_question" not in st.session_state:
    st.session_state["new_question"] = False

# Load environment variables
load_dotenv()

# API keys from .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the Groq model
model = ChatGroq(model="llama3-8b-8192")

# Chat history storage
store = {}
session_id = "single_user_session"

# Initialize audio recognizer
recognizer = sr.Recognizer()

def get_session_history(session_id: str):
    """Retrieve or create chat history for a session."""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def extract_text_from_pdf(pdf_file):
    """Extract text content from a PDF file."""
    reader = PdfReader(pdf_file)
    return "".join(page.extract_text() for page in reader.pages)

def play_text_as_audio(text):
    """Convert text to speech and play audio."""
    tts = gTTS(text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio_path = temp_audio.name
        tts.save(temp_audio_path)
    pygame.mixer.init()
    pygame.mixer.music.load(temp_audio_path)
    pygame.mixer.music.play()

def transcribe_audio():
    """Transcribe speech to text using a microphone."""
    st.write("Listening...")
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            recognizer.pause_threshold = 2
            audio = recognizer.listen(source)
            st.write("Processing...")
            transcription = recognizer.recognize_google(audio)
            # Use a temporary key to avoid conflicts
            st.session_state["temp_transcription"] = transcription
            st.success("Transcription completed!")
    except sr.UnknownValueError:
        st.error("Could not understand the audio.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def summarize_resume(text):
    """Summarize resume text using the Groq API."""
    summary_prompt = (
        "Shortly summarize the following resume text, highlighting key skills, experience, and achievements:\n"
        f"{text}"
    )
    response = with_message_history.invoke(
        [HumanMessage(content=summary_prompt)],
        config={"configurable": {"session_id": "resume_summary"}},
    )
    return response.content

def get_model_response(prompt):
    return with_message_history.invoke(
        [HumanMessage(content=prompt)],
        config={"configurable": {"session_id": session_id}}).content


def resume_feedback(resume_summary, job_role, jd):
    # Construct the prompt for feedback
    prompt = (
        f"You are an expert hiring manager for {job_role} roles. Evaluate the candidates resume content as per the job description and provide a very short feedback:\n"
        f"job description: {jd}\n"
        f"resume: {resume_summary}\n"
    )
    response = with_message_history.invoke(
        [HumanMessage(content=prompt)],
        config={"configurable": {"session_id": session_id}},
    ).content
    # Call the AI model to get feedback
    return response



def get_first_question():
    """Generate the AI's first interview question and play it as audio."""
    prompt = (
        f"""
             You are an expert interviewer for data science field. Begin interview for the provided job role. You may ask 
             questions related to candidate past experience from their resume and job description of current position.
             Keep questions short and be professional. Do not include any note   
        """
    )
    st.session_state["current_question"] = get_model_response(prompt)

def get_next_question():
    prompt = (
        f"""
        Please ask next question, it could be based on previous response or any new question.
        """)
    st.session_state["current_question"] = get_model_response(prompt)

# def get_question(is_first_question=False):
#     prompt = (
#         f"""
#         You are an expert interviewer for data science field. Begin interview for the provided job role. You may ask
#         questions related to candidate past experience from their resume and job description of current position.
#         Keep questions short and be professional.
#         """ if is_first_question else
#         "Please ask next question, it could be based on candidates answer or any new question."
#     )
#     st.session_state["current_question"] = get_model_response(prompt)


def get_response_feedback(user_response):
    # Construct the prompt for feedback
    prompt = (
        f"Evaluate the following response based on your asked question:\n\n"
        f"Response: {user_response}\n\n"
        f"Provide constructive feedback in 2 sentences."
    )
    # Call the AI model to get feedback
    return get_model_response(prompt)

def update_conversation_history_st(speaker, message):
    """Update the conversation history."""
    st.session_state["conversation_history"].append({speaker: message})

def ask_question(question):
    if not st.session_state["question_asked"]:
        play_text_as_audio(question)
        st.session_state["question_asked"] = True
    st.write(question)


def get_user_response():
    st.subheader("Your Response")

    # Record response
    if st.button("Record Your Response"):
        transcribe_audio()

    # Text area for response input
    st.text_area(
        "Edit your response here:",
        st.session_state.get("temp_transcription",""),
        height=100,
        key="response_input",
    )

def conclude_interview():
    st.session_state["interview_concluded"] = True
# Initialize the RunnableWithMessageHistory
with_message_history = RunnableWithMessageHistory(model, get_session_history)
