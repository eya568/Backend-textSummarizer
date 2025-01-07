from transformers import pipeline
class Summarizer:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")

    def summarize(self, text: str) -> str:
        summary = self.summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']






















