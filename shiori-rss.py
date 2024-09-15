# Shiori RSS Feed Parser
# Replace the [SHIORI INSTANCE] with your Shiori instance URL as well as the [USERNAME] and [PASSWORD] placeholders.

import requests
import feedparser

keywords = ['hacker'] # Keyword simple or empty for all
tag = [{'name': 'hackernews'}] # Example for tagging

session = requests.Session()

# This will log into Shiori and obtain the JWT
login_url = '[SHIORI INSTANCE]/api/v1/auth/login'
login_data = '{"username": "[USERNAME]", "password": "[PASSWORD]"}'
login_response = session.post(login_url, data=login_data, headers={"Content-Type": "application/json"})

if login_response.status_code == 200:
    response_json = login_response.json()
    token = response_json['message']['token']
    print(f"Login successful. Token: {token}")
else:
    print(f"Login failed with status code {login_response.status_code} and message {login_response.text}")
    exit()

# Set headers with token above

headers = {"Authorization": f"Bearer {token}"}

rss_feed_url = 'https://feeds.feedburner.com/TheHackersNews?format=xml' # Feed Sample
feed = feedparser.parse(rss_feed_url)

shiori_bookmark_url = 'https://[SHIORI INSTANCE]/api/bookmarks'

# Keyword matching - currently set to take all articles unless keyword specified

for entry in feed.entries:
    combined_text = f"{entry.title} {entry.summary}"
    if not keywords or any(keyword.lower() in combined_text.lower() for keyword in keywords):
        bookmark_data = {
            'url': entry.link,
            'title': entry.title,
            'tags': tag
        }
        bookmark_response = session.post(shiori_bookmark_url, json=bookmark_data, headers=headers)
        if bookmark_response.status_code in [200, 201]:
            bookmark_id = bookmark_response.json().get('id')
            print(f"Bookmark added: {entry.title} (ID: {bookmark_id})")
        else:
            print(f"Failed to add bookmark for: {entry.title}. Status code: {bookmark_response.status_code}, Response: {bookmark_response.text}")
    else:
        print(f"No keywords found in: {entry.title}")
