import praw

def get_reddit_instance():
    reddit = praw.Reddit(
        client_id="ryeqQiceSnGOqC5j1a73_g",
        client_secret="JOPnAB-qKNWJ8iG09h3GYCb7q04krQ",
        user_agent="windows:reddit_persona_scraper:v1.0 (by /u/khushi_goyal)"
    )
    return reddit

def extract_username_from_url(url):
    if url.endswith('/'):
        url = url[:-1]
    return url.split('/')[-1]

def fetch_user_data(username, reddit):
    user = reddit.redditor(username)
    posts = []
    comments = []

    try:
        for submission in user.submissions.new(limit=20):
            posts.append({
                "title": submission.title,
                "body": submission.selftext,
                "url": submission.url
            })
    except Exception as e:
        print(f"Error fetching posts: {e}")

    try:
        for comment in user.comments.new(limit=20):
            comments.append({
                "body": comment.body,
                "link": f"https://reddit.com{comment.permalink}"
            })
    except Exception as e:
        print(f"Error fetching comments: {e}")

    return posts, comments
