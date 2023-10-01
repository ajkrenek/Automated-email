import math
from datetime import date
from datetime import datetime
from datetime import timedelta
import json, random
import pytumblr2
import praw
import schedule, time
import urllib.request
import smtplib

from bs4 import BeautifulSoup
import requests
from email.message import EmailMessage
from email.utils import make_msgid
from dataclasses import dataclass


with open('config.json') as f:
    config_data = json.load(f)

reddit = praw.Reddit(   client_id=config_data['CLIENT_ID'], 
                        client_secret=config_data['CLIENT_REDDIT_SECRET'],
                        password=config_data['PASSWORD'], 
                        user_agent=config_data['USER_AGENT'],
                        username=config_data['USERNAME'])

client_key=config_data['CLIENT_KEY']
client_secret=config_data['CLIENT_TUMBLR_SECRET'] 
oauth_token=config_data['OAUTH_TOKEN'] 
oauth_secret=config_data['OAUTH_SECRET']
client = pytumblr.TumblrRestClient(client_key, client_secret, oauth_token, oauth_secret)


ahora = datetime.now()
current_day = ahora.day
current_year = ahora.year
current_month = ahora.month

def tumblr_post(quote_query):
    search_url = 'https://www.tumblr.com/search/{}?t=1'.format(random.choice(quote_query).replace(" ", "%20"))

    random_a_tag = random.choice(BeautifulSoup(urllib.request.urlopen(search_url).read(), 'html.parser').find_all("a", {"class": "BSUG4"}))
    
    blog_name = random_a_tag.get("data-login-wall-blog-name")
    
    blog_info = client.blog_info(blog_name)

    get_random_post = random.randint(0, blog_info['blog']['total_posts'])

    posts_raw_data = client.posts(blog_name,limit=1, offset=get_random_post)
    post_refined_data = posts_raw_data['posts'][0]


    return post_refined_data
            
def tumblr_text(post_info):
    try: 
        return post_info['content'][0]['text']
    
    except:

        try: 
            return post_info['trail'][0]['content'][0]['text']
        
        except:
            return "default quote"


def reddit_picture_url(reddit_subreddit):
    random_post_id = reddit.subreddit(reddit_subreddit).random()
    checked = {}
    while random_post_id.domain != 'i.redd.it':
        if random_post_id not in checked:
            checked[random_post_id] = 1
        
        random_post_id = reddit.subreddit(reddit_subreddit).random()

    return random_post_id.url


def get_message(ann_date):
    email_message = """\
            <html>
                <body>
                    <p> <em>{tumblr_text}</em> {tumblr_url}  </p>
                    <br>
                    <img src = {sub_image}
                    width="400" height="400"/>
                </body>
            </html>
        """
    if current_day == ann_date:
        email_message = """\
            <html>
                <h2> Happy {years} years and {months} months!!</h2>
                <body>
                    <p> <em>{tumblr_text}</em> {tumblr_url}  </p>
                    <br>
                    <img src = {sub_image}
                    width="400" height="400"/>
                </body>
            </html>
        """
    return email_message


@dataclass
class Mail:

    email: str
    password: str
    to_email: str
    subject: str
    send_time: str
    ann_date: str
    tumblr_search_query: str
    subreddit_list: "list[str]"
    port: int
    
    def email_depart(self):
        schedule.every().day.at(self.send_time).do(self.send_mail)
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    def send_mail(self):
        corrected_date = datetime.strptime(self.ann_date, '%Y/%m/%d').date()
        years = current_year - corrected_date.year
        months = current_month - corrected_date.month
        day = corrected_date.day
        email_html_message = get_message(day)

        tumblr_post_info = tumblr_post(self.tumblr_search_query)
        tumblr_url = tumblr_post_info['post_url']
        tumblr_quote = tumblr_text(tumblr_post_info)

        reddit_sub_name = random.choice(self.subreddit_list)
        reddit_image = reddit_picture_url(reddit_sub_name)
        msg = EmailMessage()

        msg["Subject"] = self.subject
        msg["From"] = self.email
        msg["To"] = self.to_email
        msg.add_alternative(email_html_message.format(years=years, months=months,tumblr_text=tumblr_text, tumblr_url=tumblr_url, reddit_sub=reddit_sub, sub_image=sub_image), subtype = 'html')

        with smtplib.SMTP_SSL("smtp.gmail.com", self.port) as server:
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()

email = Mail(email="example@gmail.com",
            password=config_data['EMAIL_PASSWORD'], 
            to_email="receiver@gmail.com", 
            subject="SUBJECT",
            send_time="15:00",
            ann_date="2020/08/02", #YYYY/MM/DD format, 
            tumblr_search_query=["inspirational quotes"], 
            subreddit_list=['frogs', 'CatsWithHats'], 
            port=465)


if __name__ == '__main__':
    email.email_depart()
