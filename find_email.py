import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def find_email(title):
    domain_prompt = f"Get the emails for this profile {title}"
    res = client.chat.completions.create(
        model="gpt-4",
        # tools=[{"type": "web_search_preview"}],
        messages=[
            {"role": "system", "content": f"""Extract the company domain (like meta.com, google.com) and name from a provided linkedin profile and its details. Then, you need to find potential emails for this title, for example they could be in the form of:
                'first.last@company_domain',
                'firstlast@company_domain',
                'firstlast@company_domain',
                'first_last@company_domain',
                'first@company_domain',
                'last@company_domain',
                'lastfirst@company_domain,
                or maybe more, come up with the rest
                Strictly and only respond with a list of all potential emails: [email1, email2, ...]
            """},

            {"role": "user", "content": domain_prompt}
        ]
    )
    domain_response = res.choices[0].message.content.strip().lower()

    return domain_response
