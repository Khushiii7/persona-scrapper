import os
from utils import get_reddit_instance, extract_username_from_url, fetch_user_data
from persona_extractor import build_user_persona

def extract_quote(posts, comments):
    # Try to find a representative quote from posts or comments
    for p in posts:
        if p['body'] and len(p['body'].split()) > 6:
            return p['body'].strip().replace('\n', ' ')
    for c in comments:
        if c['body'] and len(c['body'].split()) > 6:
            return c['body'].strip().replace('\n', ' ')
    return "[No representative quote found]"

def save_persona_to_file(username, persona, citations, posts, comments):
    os.makedirs("output", exist_ok=True)
    with open(f"output/{username}_persona.txt", "w", encoding="utf-8") as f:
        f.write(f"USER PERSONA: {username}\n\n")
        f.write(f"Age: [Unknown]\n")
        f.write(f"Occupation: [Unknown]\n")
        f.write(f"Status: [Unknown]\n")
        f.write(f"Location: {persona.get('Demographics', '[Unknown]')}\n")
        f.write(f"Tier: [N/A]\n")
        f.write(f"Archetype: [N/A]\n\n")
        quote = extract_quote(posts, comments)
        f.write(f"Quote: \"{quote}\"\n\n")
        f.write("PERSONALITY:\n")
        f.write(f"- Writing Style: {persona.get('Writing Style', '[Unknown]')}\n")
        f.write(f"- Tone: {persona.get('Tone', '[Unknown]')}\n\n")
        f.write("MOTIVATIONS:\n")
        f.write(f"- Values: {persona.get('Values', '[Unknown]')}\n\n")
        f.write("BEHAVIOURS & HABITS:\n")
        for topic in persona.get('Frequently Mentioned Topics', []):
            f.write(f"- {topic}\n")
        f.write("\nFRUSTRATIONS:\n")
        f.write(f"- Challenges: {persona.get('Challenges', '[Unknown]')}\n\n")
        f.write("GOALS & NEEDS:\n")
        f.write(f"- Goals: {persona.get('Goals', '[Unknown]')}\n\n")
        f.write("INTERESTS:\n")
        for interest in persona.get('Interests', []):
            f.write(f"- {interest}\n")
        f.write("\nCITATIONS:\n")
        for key in persona:
            if citations.get(key):
                f.write(f"\n{key} Citations:\n")
                for c in citations[key]:
                    f.write(f"- {c}\n")

if __name__ == "__main__":
    reddit = get_reddit_instance()
    url = input("Enter Reddit Profile URL: ")
    username = extract_username_from_url(url)
    posts, comments = fetch_user_data(username, reddit)
    persona, citations = build_user_persona(posts, comments)
    save_persona_to_file(username, persona, citations, posts, comments)
    print(f"Persona for {username} saved successfully!")
