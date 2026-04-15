# evaluator.py
import os

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:

    def load_dotenv(*_args, **_kwargs):
        return False


from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def evaluate_response(query, ai_response):
    prompt = f"""
    Evaluate the response strictly.

    Return output in this format:
    Score: <number between 1 to 5>
    Reason: <short explanation>

    Query: {query}
    Response: {ai_response}
    """

    result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict evaluator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return result.choices[0].message.content