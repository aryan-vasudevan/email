from parse import parse_prompt
from search import search_linkedin_profiles

user_prompt = input()
parsed_prompt = parse_prompt(user_prompt)

profiles = search_linkedin_profiles(parsed_prompt["role"], parsed_prompt["company"])
print(profiles)

