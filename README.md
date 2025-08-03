# LLM_WEB

**LLM_WEB** is an intelligent, customizable AI-powered assistant designed to help you write professional, engaging emails in seconds. Built using Streamlit, Python, and the Meta-Llama LLM (via Groq), this tool streamlines email composition for various lengths, languages, and topics, greatly reducing stress and boosting productivity.

---

## 🌟 Live Demo

> **[Live App](https://emailwriters.streamlit.app/)**  
> *(Note: Replace this link with your actual Streamlit Cloud or deployment URL if different.)*

---

## 🚀 Features

- **AI Email Generation**: Write emails that include subject, greeting, body, closing, and signature.
- **Multi-language Support**: Choose from dozens of languages including English, Hindi, Bengali, Spanish, French, and more.
- **Custom Lengths**: Select between Short, Medium, or Long emails.
- **Few-Shot Learning**: The model leverages curated example emails to make outputs more relevant and human-like.
- **Topic Selection**: Input a topic to tailor the email content.
- **Personalization**: Add your name and custom email subject.
- **Easy-to-use UI**: Built with Streamlit for a simple and interactive experience.

---

## 🖥️ How It Works

1. **Choose Email Settings**: Select the desired length, language, your name, and subject.
2. **Enter Topic**: Optionally specify a topic for the email.
3. **Generate**: Click "Generate" to let the AI craft your email.
4. **Copy & Use**: Easily copy the generated email for use in your communications.

---

## 🏗️ Tech Stack

- **Python**
- **Streamlit** (for the web app UI)
- **Meta-Llama LLM via Groq** (for text generation)
- **Pandas** (for example management)
- **dotenv** (for secret management)

---

## 📂 Project Structure

- `app.py`: Main Streamlit web application.
- `LLM_Help.py`: Handles LLM API integration.
- `email_generator.py`: Core logic for prompt creation and email generation.
- `few_shot.py` & `preprocess.py`: Manage and filter example emails for few-shot learning.
- `data/processed_email.json`: Stores example email data for reference.

---

## ⚡ Example Usage

1. Run the app locally:
   ```bash
   streamlit run app.py
   ```
2. Open your browser to the provided local URL (usually http://localhost:8501).
3. Set your Groq API key in `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```

---

## 🙌 Credits

Created by [kvmeena](https://github.com/Kvmeena12) | Powered by Meta-Llama (Groq)


## 🔗 Repository

[https://github.com/Kvmeena12/LLM_WEB](https://github.com/Kvmeena12/LLM_WEB)
