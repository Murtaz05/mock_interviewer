from initialization import *


# Streamlit app setup
st.title("AI Mock Interviewer 💼")

# Sidebar inputs
st.sidebar.text_input("Enter Job Role", placeholder="e.g., Data Scientist", key="job_role")
st.sidebar.text_area("Enter Job Description", placeholder="Provide job description here...", height=150, key="job_description")
resume_pdf = st.sidebar.file_uploader("Upload Resume (PDF only)", type=["pdf"], key="resume_pdf")

if not st.session_state["interview_start"]:
    if st.session_state.get("resume_pdf"):
        resume_text = extract_text_from_pdf(st.session_state["resume_pdf"])
        st.session_state["resume_text"] = resume_text


    if st.sidebar.button("Submit Details") or st.session_state["details_submitted"] :
        if all(key in st.session_state for key in ["job_role", "job_description", "resume_text"]):
            st.session_state["details_submitted"] = True
            st.session_state["resume_summary"] = summarize_resume(st.session_state["resume_text"])
            # Display job and resume details
            with st.expander("Job and Resume Details"):
                # st.subheader("Job and Resume Details")
                st.write(f"**Job Role:** {st.session_state['job_role']}")
                st.write("**Job Description:**")
                st.write(st.session_state["job_description"])
                st.write("**Resume Summary:**")
                st.write(st.session_state["resume_summary"])
                st.session_state["resume_feedback"] = resume_feedback(st.session_state['resume_summary'],st.session_state['job_role'],st.session_state["job_description"])
            with st.expander("Resume Feedback"):
                    st.write(st.session_state["resume_feedback"])
        else:
            st.session_state["details_submitted"] = False
            st.sidebar.error("Please provide Job Role, Job Description, and Resume first.")


    if st.session_state["details_submitted"] and not st.session_state["interview_start"]:
        # Start interview, first question
        if st.button("Start Interview"):
            st.session_state["interview_start"] = True
            get_first_question() #takes question in st.session_state["current_question"]

if st.session_state["interview_start"] and not st.session_state["interview_concluded"]:
    st.subheader("Question")
    ask_question(st.session_state["current_question"])

    if  st.session_state["question_asked"] and not st.session_state["response_received"]:
        get_user_response()

        if st.button("Submit Response"):
            if not st.session_state["response_input"]:
                st.error("Please enter a response.")
            else:
                st.session_state["response_feedback"] = get_response_feedback(st.session_state["response_input"])
                st.subheader("Feedback")
                play_text_as_audio(st.session_state["response_feedback"])
                st.write(st.session_state["response_feedback"])
                st.session_state["response_received"] = True


    if st.session_state["question_asked"] and st.session_state["response_received"]:
        if st.button("Next Question"):
            update_conversation_history_st("AI - Question", st.session_state["current_question"])
            update_conversation_history_st("Candidate - Response", st.session_state["response_input"])
            update_conversation_history_st("Feedback",  st.session_state["response_feedback"])

            get_next_question()
            st.session_state["question_asked"] = False
            st.session_state["response_received"] = False
            # st.session_state["new_question"] = True
            st.rerun()
    # Display conversation history
    with st.expander("Conversation History"):
        if "conversation_history" in st.session_state:
            for turn in st.session_state["conversation_history"]:
                for speaker, message in turn.items():
                    st.write(f"**{speaker}:** {message}")

    if st.button("End Interview"):
        conclude_interview()

if st.session_state["interview_concluded"]:
    st.header("Good Luck for Your Actual Interview")