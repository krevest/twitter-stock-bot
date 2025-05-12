# === bot.py ===
import snscrape.modules.twitter as sntwitter
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os
import time

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
RECIPIENTS = ['6266209570@tmomail.net', '6268992728@tmomail.net']

TWITTER_USERS = ['stockmktnewz', 'DeItaone']

seen_tweets = set()

def fetch_all_tweets(usernames, max_results=5):
    tweets = []
    for username in usernames:
        for tweet in sntwitter.TwitterUserScraper(username).get_items():
            text = f"{tweet.date.strftime('%Y-%m-%d %H:%M')} - @{username}: {tweet.content}"
            if text not in seen_tweets:
                tweets.append(text)
                seen_tweets.add(text)
                if len(tweets) >= max_results:
                    break
    return tweets

def send_sms(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ", ".join(RECIPIENTS)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def run_bot():
    tweets = fetch_all_tweets(TWITTER_USERS, max_results=5)
    if tweets:
        send_sms("\U0001F4E2 New Tweets", "\n\n".join(tweets))
    else:
        print("No new tweets at", datetime.now())

if __name__ == "__main__":
    while True:
        run_bot()
        time.sleep(600)  # every 10 mins
