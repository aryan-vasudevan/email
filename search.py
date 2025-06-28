import requests
import os
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

def search_linkedin_profiles(role: str, company: str, num_results: int = 5):
    query = f"site:linkedin.com/in \"{role}\" \"{company}\""
    url = f"https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google",
        "num": num_results
    }
    res = requests.get(url, params=params).json()
    results = []
    for result in res.get("organic_results", []):
        link = result.get("link")
        title = result.get("title")
        snippet = result.get("snippet")
        results.append({"name": title, "profile_url": link, "summary": snippet})
    
    return results

