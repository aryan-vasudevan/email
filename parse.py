import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def parse_prompt(user_prompt):
    system_prompt = """
    You are a helpful assistant. Extract the role, company, and goal from the user's message.
    Format your response as JSON: {"role": ..., "company": ..., "goal": ...}
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return dict(eval(completion.choices[0].message.content))