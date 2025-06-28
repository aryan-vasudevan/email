import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def search_linkedin_profiles(role, company, num_results = 10):
    query = f"site:linkedin.com/in \"{role}\" \"{company}\""
    url = f"https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google",
        "num": num_results
    }
    res = requests.get(url, params=params).json()

    validated = []
    for result in res.get("organic_results", []):
        link = result.get("link")
        title = result.get("title")
        snippet = result.get("snippet")
        candidate = {"name": title, "profile_url": link, "summary": snippet}

        # Use GPT to verify relevance
        check_prompt = f" This is a LinkedIn title: '{title}'\nBased on this, is the person currently working at {company} (not a former employee)? Respond with 'yes' or 'no'."
        check = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a filter for validating job roles and company association."},
                {"role": "user", "content": check_prompt}
            ]
        )
        answer = check.choices[0].message.content.strip().lower()
        if 'yes' in answer:
            validated.append(candidate)
    return validated


