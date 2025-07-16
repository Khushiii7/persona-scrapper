import os
from utils import get_reddit_instance, extract_username_from_url, fetch_user_data
from persona_extractor import build_user_persona

def save_persona_to_file(username, persona, citations):
    os.makedirs("output", exist_ok=True)
    with open(f"output/{username}_persona.txt", "w", encoding="utf-8") as f:
        f.write(f"User Persona for {username}\n\n")
        for key in persona:
            f.write(f"{key}: {persona[key]}\n")
            f.write("Citations:\n")
            for c in citations[key]:
                f.write(f"- {c}\n")
            f.write("\n")

if __name__ == "__main__":
    reddit = get_reddit_instance()
    url = input("Enter Reddit Profile URL: ")
    username = extract_username_from_url(url)
    posts, comments = fetch_user_data(username, reddit)
    persona, citations = build_user_persona(posts, comments)
    save_persona_to_file(username, persona, citations)
    print(f"Persona for {username} saved successfully!")
