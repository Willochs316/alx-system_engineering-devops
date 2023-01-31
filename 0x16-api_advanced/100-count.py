import requests
import re
from collections import Counter

def count_words(subreddit, word_list=[]):
    word_list = [w.lower() for w in word_list]
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, allow_redirects=False)
    if res.status_code != 200:
        return
    
    data = res.json()
    articles = [child["data"]["title"] for child in data["data"]["children"]]
    articles = " ".join(articles).lower()
    articles = re.sub(r'[^\w\s]', '', articles)
    words = articles.split()
    
    word_count = Counter(words)
    result = []
    for word in word_list:
        if word in word_count:
            result.append((word, word_count[word]))
    
    result = sorted(result, key=lambda x: (-x[1], x[0]))
    for r in result:
        print("{}: {}".format(r[0], r[1]))