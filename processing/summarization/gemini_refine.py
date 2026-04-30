import os
import time
from dotenv import load_dotenv
from pathlib import Path
from google import genai

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


def refine_summary(text, max_retries=3):
    prompt = f"""
    Chuyển đoạn tóm tắt sau thành 4-5 ý chính dạng bullet.

    Yêu cầu:
    - mỗi ý 1 câu ngắn (10-12 từ)
    - rõ ràng, giống báo chí
    - không lặp
    - mỗi dòng bắt đầu bằng "-"

    Nội dung:
    {text}
    """

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-flash-lite-latest',
                contents=prompt,
                config={'temperature': 0.3}
            )

            result = response.text or ''

            lines = [
                line.replace('-', '').strip()
                for line in result.split('\n')
                if line.strip().startswith('-')
            ]

            if lines:
                return lines

        except Exception as e:
            print(f'[Gemini Retry {attempt+1}] {e}')

            time.sleep(5 * (attempt + 1))

    return []