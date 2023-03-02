import datetime, math
import json, random, pytumblr, praw
import schedule, time
import urllib.request
import smtplib

from bs4 import BeautifulSoup
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

client = pytumblr.TumblrRestClient( client_key=config_data['CLIENT_KEY'], 
                                    client_secret=config_data['CLIENT_TUMBLR_SECRET'], 
                                    oauth_token=config_data['OAUTH_TOKEN'], 
                                    oauth_secret=config_data['OAUTH_SECRET'])


ahora = datetime.datetime.now()
today_date = datetime.date.today()
current_year = ahora.year
current_month = ahora.month

def ann_date(ann_year: int, ann_month:int, ann_day: int):
    
    first_date = datetime.date(ann_year, ann_month, ann_day)
    anniversary_date = datetime.date(current_year, current_month, ann_day)
    years_since = ((anniversary_date - first_date).days)/365          #converts number of days into years
    rounded = round(years_since,5)                            #rounds to 5 decimal place
    digits = math.modf(rounded)                               #splits the decimal into two: [decimal places, whole numbers]
    years = math.floor(digits[1])                             #takes the lowest value of the whole numbers
    months = round(digits[0]*12)                              #converts the decimal of the year into months

    return [years, months]


def tumblr_post(quote_query: list[str]) -> list[str]:
    
    quote = random.choice(quote_query)
    tumblr_url = 'https://www.tumblr.com/search/{}?t=1'
    search_url = tumblr_url.format(quote.replace(" ", "%20"))
    html = urllib.request.urlopen(search_url).read()
    soup = BeautifulSoup(html, 'html.parser')

    a_element = soup.find_all("a", {"class": "BSUG4"})
    random_a_tag = random.choice(a_element)
    blog_name = random_a_tag.get("data-login-wall-blog-name")

    blog_info = client.blog_info(blog_name)
    total_posts = blog_info['blog']['total_posts']
    offset = random.randint(0, total_posts)
    posts_data = client.posts(blog_name, limit=1, offset=offset)
    random_post_dict_list = posts_data['posts']
    post_dict = random_post_dict_list[0]
    blog_post_url = post_dict['post_url']

    if 'text' in post_dict:
        return [blog_post_url, post_dict['text']]   

    else:
        return [blog_post_url, post_dict['trail'][0]['content']]
            

def reddit_picture_url(subreddit_query: list[str]) -> list[str]:

    sub = random.choice(subreddit_query)
    subreddit = reddit.subreddit(sub)
    new_posts = list(subreddit.new(limit=20))
    random_post = random.choice(new_posts)
    while not random_post.url.endswith(('.png', '.jpg', '.jpeg')):
        random_post = subreddit.random()
    return [sub, random_post.url]


@dataclass
class Mail:

    email: str
    password: str
    to_email: str
    subject: str
    ann_year: int
    ann_month: int
    ann_day: int
    tumblr_search_query: str
    subreddit_list: list[str]
    port: int

    def send_mail(self):
        tumblr_quote = tumblr_post(self.tumblr_search_query)
        tumblr_url = tumblr_quote[0]
        tumblr_text = tumblr_quote[1]
        reddit_image = reddit_picture_url(self.subreddit_list)
        reddit_sub = reddit_image[0]
        sub_image = reddit_image[1]
        msg = EmailMessage()

        msg["Subject"] = self.subject
        msg["From"] = self.email
        msg["To"] = self.to_email
        msg.add_alternative("""\
            <html>
                <body>
                    <p> <em>{tumblr_text}</em> 
                    <br>
                    {tumblr_url}  
                    </p>
                    <br>
                    <img src = {sub_image}
                    width="400" height="400"/>
                </body>
            </html>
        """.format(tumblr_text=tumblr_text, tumblr_url=tumblr_url, reddit_sub=reddit_sub, sub_image=sub_image), subtype = 'html')

        with smtplib.SMTP_SSL("smtp.gmail.com", self.port) as server:
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()

    def send__ann_mail(self):
        dates = ann_date(self.ann_year, self.ann_month, self.ann_day)
        years = dates[0]
        months = dates[1]

        tumblr_quote = tumblr_post(self.tumblr_search_query)
        tumblr_url = tumblr_quote[0]
        tumblr_text = tumblr_quote[1]

        reddit_image = reddit_picture_url(self.subreddit_list)
        reddit_sub = reddit_image[0]
        sub_image = reddit_image[1]
        
        msg = EmailMessage()

        msg["Subject"] = self.subject
        msg["From"] = self.email
        msg["To"] = self.to_email
        msg.add_alternative("""\
            <html>
                <h2> Happy {years} years and {months} months!!</h2>
                <body>
                    <p> <em>{tumblr_text}</em> 
                    <br>
                    {tumblr_url}  
                    </p>
                    <br>
                    <img src = {sub_image}
                    width="400" height="400"/>
                </body>
            </html>
        """.format(years=years, months=months, tumblr_text=tumblr_text, tumblr_url=tumblr_url, reddit_sub=reddit_sub, sub_image=sub_image), subtype = 'html')

        with smtplib.SMTP_SSL("smtp.gmail.com", self.port) as server:
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()            


email = Mail(email="example@gmail.com",
            password=config_data['EMAIL_PASSWORD'], 
            to_email="receiver@gmail.com", 
            subject="SUBJECT",
            ann_year=2020,
            ann_month=int("08"),
            ann_day=17, 
            tumblr_search_query=["inspirational quotes"], 
            subreddit_list=['frogs', 'CatsWithHats'], 
            port=465)


if __name__ == '__main__':
    if today_date == 17:
        schedule.every().day.at("15:00").do(email.send_ann_mail)
        
    else:
        schedule.every().day.at("15:00").do(email.send_mail)
        
    while True:
        schedule.run_pending()
        time.sleep(1)
