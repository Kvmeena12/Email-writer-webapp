import pandas as pd
import json
from datetime import datetime

class FewShotPosts:
    def __init__(self, file_path="data/processed_email.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            self.df = pd.json_normalize(posts)

            # Ensure tags is a list for every row
            if 'tags' in self.df.columns:
                self.df['tags'] = self.df['tags'].apply(lambda x: x if isinstance(x, list) else [])
                all_tags = self.df['tags'].sum()
                self.unique_tags = sorted(set(all_tags))
            else:
                self.df['tags'] = [[] for _ in range(len(self.df))]
                self.unique_tags = []

            # Ensure 'language' column exists, fill missing with 'English'
            if 'language' not in self.df.columns:
                self.df['language'] = "English"
            else:
                self.df['language'].fillna("English", inplace=True)

            # Ensure 'length' column exists, categorize if line_count exists
            if 'length' not in self.df.columns and 'line_count' in self.df.columns:
                self.df['length'] = self.df['line_count'].apply(self.categorize_length)
            elif 'length' not in self.df.columns:
                self.df['length'] = "Medium"

            # Add 'date' column with default current date-time if missing
            if 'date' not in self.df.columns:
                current_time = datetime.now().strftime("%A, %B %d, %Y, %I:%M %p %Z")
                self.df['date'] = current_time

    def get_filtered_examples(self, length, language, tag):
        df_filtered = self.df[
            self.df['tags'].apply(lambda tags: tag in tags if isinstance(tags,list) else False) &
            (self.df['language'] == language) &
            (self.df['length'] == length)
        ]

        examples = []
        for _, row in df_filtered.iterrows():
            examples.append({
                "subject": row.get('subject', f"Regarding {tag}"),
                "greeting": row.get('greeting', "Hello,"),
                "body": row.get('body', row.get('text', '')),
                "closing": row.get('closing', "Best regards,"),
                "signature": row.get('signature', "[Your Name]"),
                "description": row.get('description', ''),
                "date": row.get('date', '')
            })
        return examples

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
    samples = fs.get_filtered_examples("Medium", "English", "Job Search")
    for s in samples:
        print(s)
