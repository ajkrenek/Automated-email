import smtplib, ssl, random, schedule, time, praw, datetime, re, math
import urllib.request
from email.message import EmailMessage
from email.utils import make_msgid
from bs4 import BeautifulSoup

    #global variables
now = datetime.datetime.now()
today_date = datetime.date.today()
first_date=datetime.date(2020, 8, 17)
ad = 17
cy = now.year
cm = now.month
special_date = datetime.date(cy, cm, ad)

years_since = ((special_date - first_date).days)/365
digits = math.modf(years_since)
years = str(digits[1])
year = years[0]
months = str(digits[0])
month = months[2]

reddit = praw.Reddit(client_id="", client_secret='',

                 password='', user_agent='',

                 username='')

def reddit_quote():

    with open('reddit.txt', 'r') as f:
        read = f.read()
        array = read.split('\n')
        link = random.choice(array)

    reddit_url = link
    another_list = []


    submissions = reddit.submission(url=reddit_url)
    for top_level_comment in submissions.comments:
        another_list.append(top_level_comment.body)

    reddit_comment = random.choice(another_list)
    for item in reddit_comment:
        if item == '[removed]':
            continue
        if item == '[deleted]':
            continue
        if item == ' ':
            new_reddit_comment = reddit_comment
            break
    return new_reddit_comment

def tumblr_url():
    tumblr_url = 'https://www.tumblr.com/search/love%20quotes?t=1'
    html = urllib.request.urlopen(tumblr_url).read()
    soup = BeautifulSoup(html, 'html.parser')
    some_list = []
    for post in soup.find_all('a', href=True):
        some_list.append(post['href'])


    post_url = re.findall(r'''
    #structure of post url : https://somename.tumblr.com/post/12094812094814/some-post-name
    https?://                      # https part
    (?:[-\w.]|(?:%[\da-fA-F]{2}))+ # name.tumblr part
    /                              # forward slash
    \w+                            #'post'
    /                              # forward slash
    \d+                            # the digits
    /                              # forward slash
    [\w-]*                         # some-post-name
    ''',str(some_list), re.VERBOSE)

    post = random.choice(post_url)
    return post

def reddit_picture_url():

    url_list = ""
    sub = "frogs"
    subreddit = reddit.subreddit(sub)
    new_subreddit = subreddit.new(limit=20)

    for submission in new_subreddit:
        picture_url = str(submission.url)
        if picture_url.endswith('jpg') or picture_url.endswith('jpeg') or picture_url.endswith('png'):
            url_list += picture_url +'\n'

    url_link = url_list.split()
    random_url = random.choice(url_link)

    return random_url

#setting up email/message

    #global email variables

email = ""
password = ""
port = 465 #gmail port

def mail():
    Quote = reddit_quote()
    Url = tumblr_url()
    Picture = reddit_picture_url()

    msg = EmailMessage()

    msg["Subject"] = ""
    msg["From"] = ""
    msg["To"] = ""

    msg.add_alternative("""\
    <html>
        <head> <h1>  </h1> </head>
        <body>
            <p> {Quote} </p>
            <p> {Url} </p>
            <img src = {Picture}
            width="400" height="400"/> 
        </body>
    </html>
""".format(Quote=Quote, Url=Url, Picture=Picture), subtype = 'html')

    with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
        server.login(email, password)
        server.send_message(msg)
        server.quit()

def special_mail():
    loveQ = love_quote()
    loveU = love_url()
    frogU = frog_picture_url()

    msg = EmailMessage()

    msg["Subject"] = ""
    msg["From"] = ""
    msg["To"] = ""

    msg.add_alternative("""\
    <html>
        <head> <h1> Special Day </h1> </head>
        <h2> Happy {years} years and {months} months!!</h2>
        <body>
            <p> {Quote} </p>
            <p> {Url} </p>
            <img src = {Picture}
            width="400" height="400"/> 
        </body>
    </html>
""".format(Quote=Quote, Url=Url, Picture=Picture, years=year, months=month), subtype = 'html')

    with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
        server.login(email, password)
        server.send_message(msg)
        server.quit()

if today_date == special_date:
    schedule.every().day.at("20:00").do(special_mail)
else:
    schedule.every().day.at("20:00").do(mail)
while True:
    schedule.run_pending()
    time.sleep(1)



