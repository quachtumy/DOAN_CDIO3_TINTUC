from processing.summarization.textrank import textrank_summarize
from processing.summarization.gemini_refine import refine_summary

def summarize_pipeline(text):
    sentences = textrank_summarize(text)
    if not sentences:
        return []
    text = ' '.join(sentences)

    bullets = refine_summary(text)
    if not bullets:
        return sentences
    return bullets