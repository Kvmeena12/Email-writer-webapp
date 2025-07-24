import streamlit as st
from email_generator import generate_email
from few_shot import FewShotPosts


length_options = ["Short", "Medium", "Long"]
language_options = [
    "English", "Hinglish", "Bengali", "Hindi", "Spanish", "French", "German", "Chinese (Simplified)", 
    "Chinese (Traditional)", "Russian", "Arabic", "Portuguese", "Urdu", "Japanese", "Korean", 
    "Italian", "Dutch", "Turkish", "Vietnamese", "Polish", "Swedish", "Norwegian", "Greek", 
    "Hebrew", "Thai", "Indonesian", "Malay", "Czech", "Hungarian", "Romanian", 
    "Danish", "Finnish", "Bulgarian", "Serbian", "Croatian", "Slovak", "Lithuanian", 
    "Latvian", "Estonian", "Filipino", "Tamil", "Telugu", "Kannada", "Marathi", "Gujarati", 
    "Punjabi", "Persian", "Swahili", "Zulu", "Amharic", "Mongolian", "Albanian"
]

fs = FewShotPosts()  # Load data once to get tags if needed


def main():
    st.markdown(
    """
    <h2 style="
        margin-top: 40px;
        font-family: 'Arial', sans-serif;
        font-weight: 700;
        font-size: 2rem;
        color: #4B4B4B;">
        Intelligent Email Writing Assistant
    </h2>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <p style="
        font-family: 'Arial', sans-serif;
        font-size: 1.1rem;
        color: #666666;
        margin-bottom: 20px;
        line-height: 1.5;">
        Let AI help you write professional and engaging emails within seconds, reducing your stress and improving productivity.
    </p>
    """,
    unsafe_allow_html=True,
)

    # UI columns for the controls
    col1, col2, col3, col4 = st.columns([2, 2, 2, 3])

    with col1:
        selected_length = st.selectbox("Length", options=length_options)
    with col2:
        selected_language = st.selectbox("Language", options=language_options)
    with col3:
        writer_name = st.text_input("Writer's Name", value="Your Name")
    with col4:
        email_subject = st.text_input("Email Subject", value="Your Email Subject")

    # Optional: add topic input as free text or dropdown if needed
    topic = st.text_input("Topic (optional)", value="General")

    if st.button("Generate"):
        email_content = generate_email(selected_length, selected_language, topic, writer_name, email_subject)
        st.markdown("### Generated Email")
        st.markdown(email_content)

    # Footer placed at the bottom inside main()
    st.markdown("""<hr>""", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:gray; font-size:13px;'>"
        "Created by kvmeena | Powered by meta-llama/llama-4-scout-17b-16e-instruct"
        "</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
