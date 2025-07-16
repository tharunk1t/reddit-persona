import praw
import pandas as pd
import datetime as dt

def init_reddit():
    import os
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

def fetch_user_content(reddit, username, max_items=300):
    redditor = reddit.redditor(username)
    rows = []

    for post in redditor.submissions.new(limit=max_items):
        rows.append({
            "type": "post",
            "text": (post.title or "") + "\n" + (post.selftext or ""),
            "permalink": "https://reddit.com" + post.permalink,
            "utc": dt.datetime.utcfromtimestamp(post.created_utc)
        })

    for comment in redditor.comments.new(limit=max_items):
        rows.append({
            "type": "comment",
            "text": comment.body,
            "permalink": "https://reddit.com" + comment.permalink,
            "utc": dt.datetime.utcfromtimestamp(comment.created_utc)
        })

    return pd.DataFrame(rows).sort_values("utc", ascending=False).reset_index(drop=True)
