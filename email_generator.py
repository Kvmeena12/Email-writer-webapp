# Keep existing helper functions (if any) below or import them from elsewhere in the project.
from LLM_Help import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 7 lines"
    elif length == "Medium":
        return "6 to 12 lines" 
    elif length == "Long":
        return "11 to 20 lines"
    else:
        return "6 to 10 lines"

def generate_email(length, language, tag, writer_name="Your Name", email_subject=None):
    prompt = get_prompt(length, language, tag, writer_name, email_subject)
    response = llm.invoke(prompt)
    return response.content

def get_prompt(length, language, tag, writer_name, email_subject):
    length_str = get_length_str(length)
    subject_text = email_subject if email_subject else f"Regarding {tag}"
    examples = few_shot.get_filtered_examples(length, language, tag)

    # Build prompt with description and date included in examples
    prompt = f'''
Generate a professional email containing a subject, greeting, body, polite closing, and signature including the writer's name.

Topic: {tag}
Length: {length_str}
Language: {language}
Subject: {subject_text}
Writer's Name: {writer_name}

'''

    if examples:
        prompt += "Here are some example emails to follow:\n"
        for i, ex in enumerate(examples[:2]):  # Use up to 2 examples
            prompt += f"\nExample {i+1}:\n"
            prompt += f"Description: {ex['description']}\n" if ex['description'] else ""
            prompt += f"Date: {ex['date']}\n" if ex['date'] else ""
            prompt += f"Subject: {ex['subject']}\n"
            prompt += f"Greeting: {ex['greeting']}\n"
            prompt += f"Body:\n{ex['body']}\n"
            prompt += f"Closing: {ex['closing']}\n"
            prompt += f"Signature: {ex['signature']}\n"

    prompt += f"\nPlease write an email consistent with the above details and examples. Include \"{writer_name}\" in the signature."

    return prompt


if __name__ == "__main__":
    print(generate_email("Medium", "English", "Job Search", "Alice", "Application Follow-Up"))
