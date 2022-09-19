import smtplib, ssl, random, schedule, time, praw, datetime, re, math
import urllib.request
from email.message import EmailMessage
from email.utils import make_msgid
from bs4 import BeautifulSoup

### Global variables ###
now = datetime.datetime.now()
today_date = datetime.date.today()
first_date = datetime.date(2020, 8, 17)                                         #specify date you want to compare to
specific_day = 17
current_year = now.year
current_month = now.month
special_date = datetime.date(current_year, current_month, specific_day)         #specifies the special date

### Calculating and converting the date ###
years_since = ((special_date - first_date).days)/365                            #converts number of days into years
rounded = round(years_since,5)                                                  #rounds to 5 decimal place
digits = math.modf(rounded)                                                     #splits the decimal into two: [decimal places, whole numbers]
years = math.floor(digits[1])                                                   #takes the lowest value of the whole numbers
months = round(digits[0]*12)                                                    #converts the decimal of the year into months

### Initializes reddit praw API ####
reddit = praw.Reddit(client_id='',
                    client_secret='',                          
                    password='',
                    user_agent='',
                    username='')
class Mail:

    def __init__(self, file_name, tumblr_url_query, subreddit_query, email, password, subject, to_email, email_list, port):
        self.file_name = file_name
        self.tumblr_url_query = tumblr_url_query
        self.subreddit_query = subreddit_query

        self.email = email
        self.password = password
        self.subject = subject
        self.to_email = to_email
        self.email_list = email_list
        self.port = port

    ### Email Object Functions ###

    def reddit_quote(self, file_name):

        with open(self.file_name, 'r') as f:                            #opens text file with list of links
            read = f.read()
            array = read.split('\n')
            link = random.choice(array)

        reddit_url = link
        another_list = []


        submissions = reddit.submission(url=reddit_url)                 #parses through the reddit comment thread and appends to a list
        for top_level_comment in submissions.comments:
            another_list.append(top_level_comment.body)

        reddit_comment = random.choice(another_list)                    #parses through the list and skips over removed, deleted, or empty comments
        for item in reddit_comment:
            if item == '[removed]':
                continue
            if item == '[deleted]':
                continue
            if item == ' ':
                new_reddit_comment = reddit_comment
                break
        return new_reddit_comment

    def tumblr_url(self, tumblr_url_query):
        tumblr_url = self.tumblr_url_query
        html = urllib.request.urlopen(tumblr_url).read()
        soup = BeautifulSoup(html, 'html.parser')
        some_list = []
        for post in soup.find_all('a', href=True):                      #looks through the HTML of the specified link for 'a' tags and adds matches to a list
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

        post = random.choice(post_url)                                  #looks for tumblr link and returns a random post from the list
        return post

    def reddit_picture_url(self, subreddit_query):

        url_list = ""
        sub = self.subreddit_query
        subreddit = reddit.subreddit(sub)
        new_subreddit = subreddit.new(limit=20)

        for submission in new_subreddit:                                #looks through the first 20 posts that contain images and appends them to a list
            picture_url = str(submission.url)
            if picture_url.endswith('jpg') or picture_url.endswith('jpeg') or picture_url.endswith('png'):
                url_list += picture_url +'\n'

        url_link = url_list.split()
        random_url = random.choice(url_link)                            #splits the url and returns a random image

        return random_url


    ### Sending Email Functions ###
    def get_email(self, email_list):
        if self.email_list is not None:
            email_list = []
            with open(self.email_list, 'r') as searchfile:
                for line in searchfile:
                    emails = line.strip()
                    email_list.append(emails)
            return email_list
        else:
            pass

    def send_mail(self):
        Quote = self.reddit_quote(self.file_name)
        Url = self.tumblr_url(self.tumblr_url)
        Picture = self.reddit_picture_url(self.subreddit_query)
        msg = EmailMessage()
        recipients = self.get_email(self.email_list)
        msg["Subject"] = self.subject
        msg["From"] = self.email
        if self.email_list is not None:
            msg["To"] = ", ".join(recipients)
        else:
            msg["To"] = self.to_email

        msg.add_alternative("""\
    <html>
        <head> <h1> </h1> </head>
        <body>
            <p> {Quote} </p>
            <p> {Url} </p>
            <img src = {Picture} width="400" height="400"/>
        </body>
    </html>
    """.format(Quote=Quote, Url=Url, Picture=Picture), subtype = 'html')    #embeds quote, link, and picture resized to 400x400 pixels

        with smtplib.SMTP_SSL("smtp.gmail.com", self.port) as server:
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()

    def special_mail():
        Quote = self.reddit_quote(self.file_name)
        Url = self.tumblr_url(self.tumblr_url)
        Picture = self.reddit_picture_url(self.subreddit_query)
        msg = EmailMessage()
        recipients = self.get_email(self.email_list)
        msg["Subject"] = self.subject
        msg["From"] = self.email
        if self.email_list is not None:
            msg["To"] = ", ".join(recipients)
        else:
            msg["To"] = self.to_email

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
""".format(Quote=Quote, Url=Url, Picture=Picture, years=year, months=month), subtype = 'html') #embeds the year and month into email

        with smtplib.SMTP_SSL("smtp.gmail.com", self.port) as server:
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()





email = Mail('text file with list of reddit threads (eg: reddit.txt'),                              #self.file
            'tumblr url query (eg: https://www.tumblr.com/search/love%20quotes?t=1)',               #self.tumblr_url
            'subreddit query',                                                                      #self.subreddit
            "email you will be sending from",                                                       #self.email
            "email password",                                                                       #self.password
            "subject",                                                                              #self.subject
            "email list you want to send to",                                                       #self.to_email 
            "email list you wish to use",                                                           #self.email_list
            email port number)                                                                      #self.port


if __name__ == '__main__':
    if today_date == special_date:
        schedule.every().day.at("15:00").do(email.special_mail)
    else:
        schedule.every().day.at("15:00").do(email.send_mail)
    while True:
        schedule.run_pending()
        time.sleep(1)
