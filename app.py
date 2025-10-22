# import streamlit as st
# from email_generator import generate_email
# from few_shot import FewShotPosts


# length_options = ["Short", "Medium", "Long"]
# language_options = [
#     "English", "Hinglish","Hindi","Bengali"
# ]

# fs = FewShotPosts()  # Load data once to get tags if needed


# def main():
#     st.markdown(
#     """
#     <h2 style="
#         margin-top: 40px;
#         font-family: 'Arial', sans-serif;
#         font-weight: 700;
#         font-size: 2rem;
#         color: #4B4B4B;">
#         Intelligent Email Writing Assistant
#     </h2>
#     """,
#     unsafe_allow_html=True,
# )
#     st.markdown(
#     """
#     <p style="
#         font-family: 'Arial', sans-serif;
#         font-size: 1.1rem;
#         color: #666666;
#         margin-bottom: 20px;
#         line-height: 1.5;">
#      Hey 👋! Let AI help you craft professional and engaging emails in seconds, reducing your stress and boosting your productivity.
#     </p>
#     """,
#     unsafe_allow_html=True,
# )

#     # UI columns for the controls
#     col1, col2, col3, col4 = st.columns([2, 2, 2, 3])

#     with col1:
#         selected_length = st.selectbox("Length", options=length_options)
#     with col2:
#         selected_language = st.selectbox("Language", options=language_options)
#     with col3:
#         writer_name = st.text_input("Writer's Name", value="Your Name")
#     with col4:
#         email_subject = st.text_input("Email Subject", value="Your Email Subject")

#     # Optional: add topic input as free text or dropdown if needed
#     topic = st.text_input("Topic (optional)", value="General")

#     if st.button("Generate"):
#         email_content = generate_email(selected_length, selected_language, topic, writer_name, email_subject)
#         st.markdown("### Generated Email")
#         st.markdown(email_content)

#     # Footer placed at the bottom inside main()
#     st.markdown("""<hr>""", unsafe_allow_html=True)
#     st.markdown(
#         "<p style='text-align:center; color:gray; font-size:13px;'>"
#         "Created by kvmeena | Powered by meta-llama/llama-4-scout-17b-16e-instruct"
#         "</p>",
#         unsafe_allow_html=True
#     )


# if __name__ == "__main__":
#     main()
import streamlit as st
from email_generator import send_email_smtp

st.set_page_config(page_title="Email Writer", page_icon="✉️")

st.title("Email Writer")
st.write("Generate professional emails quickly.")

# --- Inputs for generating email (existing UI / structure preserved where possible) ---
writer_name = st.text_input("Your name", value="", help="Display name that will appear as the sender.")
subject = st.text_input("Subject", value="", help="Subject line for the email.")
recipient_role = st.text_input("Recipient role (e.g., Hiring Manager, Customer)", value="")
tone = st.selectbox("Tone", ["Professional", "Casual", "Friendly", "Formal"])
prompt = st.text_area("Write what you want to say (bullet points or short description)", height=120)
generate_btn = st.button("Generate Email")

generated_email = ""
if generate_btn:
    # Placeholder generation logic; replace with existing generator if present.
    # Keep this simple and consistent with repo style.
    generated_email = (
        f"Hi {recipient_role or 'there'},\n\n"
        f"{prompt.strip()}\n\n"
        f"Best regards,\n{writer_name or ''}"
    )

if generated_email:
    st.subheader("Generated Email")
    st.text_area("Email", value=generated_email, height=240)

    # --- New: Send Email UI ---
    st.markdown("---")
    st.subheader("📧 Send Email")
    col1, col2 = st.columns(2)

    with col1:
        recipient_email = st.text_input("Recipient email", placeholder="example@email.com")

    with col2:
        send_btn = st.button("Send Email", type="primary")

    if send_btn:
        # Validation
        if not recipient_email or recipient_email.strip() == "":
            st.error("Please enter a recipient email address.")
        elif "@" not in recipient_email or recipient_email.startswith("@") or recipient_email.endswith("@"):
            st.error("Please enter a valid email address.")
        else:
            with st.spinner("Sending email..."):
                success, msg = send_email_smtp(
                    recipient_email=recipient_email.strip(),
                    subject=subject,
                    email_body=generated_email,
                    sender_name=writer_name,
                )
            if success:
                st.success(msg)
            else:
                st.error(msg)
