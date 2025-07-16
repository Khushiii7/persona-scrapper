import spacy
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")

try:
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
except Exception as e:
    summarizer = None
    print("Summarization model not available, using fallback.")

try:
    sentiment_analyzer = pipeline("sentiment-analysis")
except Exception as e:
    sentiment_analyzer = None
    print("Sentiment model not available, using fallback.")

def build_user_persona(posts, comments):
    persona = {
        "Interests": [],
        "Writing Style": "",
        "Tone": "",
        "Frequently Mentioned Topics": [],
        "Demographics": "",
        "Values": "",
        "Goals": "",
        "Challenges": ""
    }
    citations = {
        "Interests": [],
        "Writing Style": [],
        "Tone": [],
        "Frequently Mentioned Topics": [],
        "Demographics": [],
        "Values": [],
        "Goals": [],
        "Challenges": []
    }

    all_texts = []

    for p in posts:
        text = p['title'] + " " + p['body']
        all_texts.append((text, p['url']))

    for c in comments:
        all_texts.append((c['body'], c['link']))

    combined_text = " ".join([t[0] for t in all_texts])
    summary = ""
    if summarizer:
        try:
            summary = summarizer(combined_text[:1024], max_length=60, min_length=10, do_sample=False)[0]['summary_text']
        except Exception as e:
            summary = ""

    interests = set()
    topics = set()
    demographics = set()
    for text, link in all_texts:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT", "EVENT", "WORK_OF_ART"]:
                interests.add(ent.text)
                citations["Interests"].append(link)
            if ent.label_ in ["GPE", "NORP", "PERSON"]:
                demographics.add(ent.text)
                citations["Demographics"].append(link)
        for chunk in doc.noun_chunks:
            topics.add(chunk.text)
    if summary:
        persona["Frequently Mentioned Topics"] = list(set(summary.split()))[:10]
    else:
        persona["Frequently Mentioned Topics"] = list(topics)[:10]
    persona["Interests"] = list(interests)
    persona["Demographics"] = ", ".join(list(demographics)[:3])

    total_len = sum(len(t[0].split()) for t in all_texts) / len(all_texts) if all_texts else 0
    persona["Writing Style"] = "Detailed" if total_len > 20 else "Concise"
    citations["Writing Style"] = [t[1] for t in all_texts]

    if sentiment_analyzer:
        sentiments = []
        for t, _ in all_texts:
            try:
                result = sentiment_analyzer(t[:512])[0]
                sentiments.append(result['label'])
            except Exception:
                continue
        if sentiments:
            if sentiments.count("POSITIVE") > sentiments.count("NEGATIVE"):
                persona["Tone"] = "Positive"
            elif sentiments.count("NEGATIVE") > sentiments.count("POSITIVE"):
                persona["Tone"] = "Negative"
            else:
                persona["Tone"] = "Neutral"
        else:
            persona["Tone"] = "Neutral"
    else:
        if any("love" in t[0] or "great" in t[0] for t in all_texts):
            persona["Tone"] = "Positive"
        elif any("hate" in t[0] or "bad" in t[0] for t in all_texts):
            persona["Tone"] = "Negative"
        else:
            persona["Tone"] = "Neutral"
    citations["Tone"] = [t[1] for t in all_texts]

    def extract_section(text, keyword):
        if not text:
            return ""
        sentences = text.split('.')
        for s in sentences:
            if keyword.lower() in s.lower():
                return s.strip()
        return ""

    if summarizer:
        try:
            values = summarizer(combined_text[:1024] + "\nWhat values does this user express?", max_length=40, min_length=10, do_sample=False)[0]['summary_text']
            goals = summarizer(combined_text[:1024] + "\nWhat goals does this user have?", max_length=40, min_length=10, do_sample=False)[0]['summary_text']
            challenges = summarizer(combined_text[:1024] + "\nWhat challenges does this user face?", max_length=40, min_length=10, do_sample=False)[0]['summary_text']
            persona["Values"] = values
            persona["Goals"] = goals
            persona["Challenges"] = challenges
            citations["Values"] = [t[1] for t in all_texts]
            citations["Goals"] = [t[1] for t in all_texts]
            citations["Challenges"] = [t[1] for t in all_texts]
        except Exception:
            persona["Values"] = extract_section(combined_text, "value")
            persona["Goals"] = extract_section(combined_text, "goal")
            persona["Challenges"] = extract_section(combined_text, "challenge")
    else:
        persona["Values"] = extract_section(combined_text, "value")
        persona["Goals"] = extract_section(combined_text, "goal")
        persona["Challenges"] = extract_section(combined_text, "challenge")
        citations["Values"] = [t[1] for t in all_texts]
        citations["Goals"] = [t[1] for t in all_texts]
        citations["Challenges"] = [t[1] for t in all_texts]

    return persona, citations