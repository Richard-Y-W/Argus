from engineering.source_ingestion.reddit_public import sanitize_listing

def test_sanitize_listing_excludes_identity_and_body():
    payload={"data":{"children":[{"data":{"title":"Costs","author":"person","selftext":"text","created_utc":1,"score":2,"num_comments":3,"permalink":"/r/a/x","subreddit":"a"}}]}}
    rows=sanitize_listing(payload)
    assert rows[0]["url"]=="https://www.reddit.com/r/a/x"
    assert "author" not in rows[0] and "selftext" not in rows[0]
