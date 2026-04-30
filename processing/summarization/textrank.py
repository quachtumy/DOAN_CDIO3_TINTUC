import re

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

def clean_text(text):
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def textrank_summarize(text, num_sentences=4):
    text = clean_text(text)

    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, num_sentences)

    return [str(sentence) for sentence in summary]