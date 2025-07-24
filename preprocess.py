import pandas as pd
import json

class FewShotPosts:
    def __init__(self, file_path="data/processed_email.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            self.df = pd.json_normalize(posts)
            if 'length' not in self.df.columns and 'line_count' in self.df.columns:
                self.df['length'] = self.df['line_count'].apply(self.categorize_length)
            if 'tags' in self.df.columns:
                all_tags = self.df['tags'].apply(lambda x: x if isinstance(x, list) else []).sum()
                self.unique_tags = list(set(all_tags))
            else:
                self.unique_tags = []

    def get_filtered_emails(self, length, language, tag):
        df_filtered = self.df[
            (self.df.get('tags', pd.Series([])).apply(lambda tags: tag in tags if isinstance(tags, list) else False)) &
            (self.df.get('language') == language) &
            (self.df.get('length') == length)
        ]
        # If new email fields are present, include them; else, fall back to 'text'
        email_examples = []
        for _, row in df_filtered.iterrows():
            if all(field in row for field in ['subject', 'greeting', 'body', 'closing', 'signature']):
                email_examples.append({
                    "subject": row.get('subject'),
                    "greeting": row.get('greeting'),
                    "body": row.get('body'),
                    "closing": row.get('closing'),
                    "signature": row.get('signature')
                })
            else:
                # Legacy fallback
                email_examples.append({
                    "subject": f"Regarding {tag}",
                    "greeting": "Hello,",
                    "body": row.get('text', ''),
                    "closing": "Best regards,",
                    "signature": "[Your Name]"
                })
        return email_examples

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags or []

if __name__ == "__main__":
    fs = FewShotPosts()
    print("Available Tags:", fs.get_tags())
    emails = fs.get_filtered_emails("Medium", "English", "Job Search")
    for email in emails:
        print(email)
