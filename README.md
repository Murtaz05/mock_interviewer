# AI Mock Interviewer

## Overview
AI Mock Interviewer is a web application designed to help job candidates prepare for interviews effectively. The app uses AI to simulate a real interview environment, providing personalized questions, real-time feedback, and audio-based interactions based on a candidate's resume and the job description. This project aims to enhance the candidate's confidence and readiness for actual interviews.

---

## Key Features
- **Job Role and Resume Analysis**: Analyze the candidate's uploaded resume against the job description to generate targeted questions.
- **AI-Driven Questions**: Dynamically generate interview questions tailored to the job role and resume details.
- **Real-Time Feedback**: Provide constructive feedback for candidate responses to improve performance.
- **Audio Integration**: Convert questions and feedback into speech for an immersive experience.
- **Conversation History**: Download a complete history of the interview for review and analysis.
- **Resume Feedback**: Highlight strengths and areas for improvement in the candidate's resume.

---

## Technologies Used
### Frontend:
- [Streamlit](https://streamlit.io): For creating an interactive web interface.

### Backend:
- [GROQ API](https://www.groq.com/): Utilizing the LLaMA Model to generate interview questions and provide feedback based on resume and job descriptions.
- [PyPDF2](https://pypi.org/project/PyPDF2/): For extracting text from uploaded resumes.
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/): To process audio-based responses.
- [gTTS](https://pypi.org/project/gTTS/): For converting text to speech.


### Others:
- [Python](https://www.python.org): The core programming language for the project.
- [Streamlit Session State](https://docs.streamlit.io/library/advanced-features/session-state): For maintaining interview state across interactions.

---

## Installation
### Prerequisites
- Python 3.8 or higher
- Virtual environment manager (optional but recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Murtaz05/mock-interviewer.git
   cd mock_interviewer
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run main_code.py
   ```

---

## Usage
1. **Provide Details**:
   - Enter the job role and description in the sidebar.
   - Upload your resume (PDF format).
2. **View Analysis**:
   - Review the resume summary and feedback.
   - Check the job details and their alignment with the resume.
3. **Start Interview**:
   - Click the "Start Interview" button.
   - Respond to questions via audio input or via typing.
   - You can edit your response after recording
   - Receive feedback after you submit your response.
4. **Review Session**:
   - Use the "Conversation History" section to review all questions, responses, and feedback.
5. **Conclude**:
   - End the session and receive a motivational message.
   - Option to download the conversation history.

---

## File Structure
```
├── main_code.py            # Main application logic
├── initialization.py       # Helper functions and initialization
├── requirements.txt        # Python dependencies
├── README.md               # Project overview
└── sample_data/            # Example resumes and job descriptions (optional)
```

---

## Contribution
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to your forked repository:
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request.

---

## Acknowledgments
- Special thanks to my mentors (Usman Bukhari and Hafsa Habib) for continuous support.
- My team members Muhammad Usman, Usman Ahmed Khan, and Waqas Ishaq
- Special thanks to the Langchain, Groq and Streamlit teams for their powerful APIs and tools.
- Inspired by the need for practical, accessible interview preparation tools.

---

## Future Enhancements
- Robust error handling.
- Incorporate video-based interviews for better candidate engagement.
- Add multi-language support for non-English speakers.
- Include mock technical assessments alongside the interview process.
- Enable integration with LinkedIn for automated profile analysis.
- Enable integration with LinkedIn for automated JD analysis.


---

## Contact
For inquiries, please reach out to [murtaza_nadeem](mailto:murtaza.itu@gmail.com).

