import pandas as pd
import numpy as np
import re
import unicodedata
from underthesea import text_normalize, word_tokenize

def clean_text(text):
    if not text:
        return ''
    
    # Xoá html code trong dữ liệu
    text = re.sub(r'<[^>]*>', '', text)

    # Chuẩn hoá về bảng mã Unicode
    text = unicodedata.normalize('NFC', text)

    # Chuẩn hoá tiếng việt
    text = text_normalize(text)

    # Đưa về chữ viết thường
    text = text.lower()
    
    return text

def preprocess_list(texts):
    return [clean_text(text) for text in texts]