import praw

def get_reddit_instance():
    import os

    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
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
