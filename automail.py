import smtplib, ssl, random, schedule, time
import urllib.request
import os
from email.message import EmailMessage
from email.utils import make_msgid
from bs4 import BeautifulSoup


def example_quote():
    with open('example quotes.txt', 'r') as f:
        read = f.read()
        array = read.split('\n')
        quote = random.choice(array)
    return quote

def example_url():
    with open('example.txt', 'r') as f:
        read = f.read()
        array = read.split('\n')
        tquote = random.choice(array)
#opens random url from text file, scrapes the text from the webpage between <p> tags and removes the <p> tags
    html = urllib.request.urlopen(tquote).read()
    soup = BeautifulSoup(html, 'html.parser')
    p_tag = soup.p
    text_p_tag = p_tag.contents[0]
    # combines the text from the webpage and the link to the post
    text_url = text_p_tag + '\n' + tquote
    return text_url

def picture():
    image = random.choice(os.listdir("file name"))
    return image

#setting up email/message
def mail():
    port = 465 #gmail server port
#calls the returned values
    example_pic = picutre()
    exampleQ = example_quote()
    exampleU = example_url()

    msg = EmailMessage()

    msg["Subject"] = "Automated Test"
    msg["From"] = "sender@email.com"
    msg["To"] = "receiver@email.com"
    
    picture_cid = make_msgid()

    msg.add_alternative("""\
    <html>
        <body>
            <p> {exampleQ} </p>
            <p> {exampleU} </p>
            <p> Insert your picture
                <a href="https://i.imgur.com/XqoqnyH.jpg"> </a> #can insert with url link too
            </p>
            <img src = "cid:{picture_cid}" />
        </body>
    </html>
""".format(exampleQ=exampleQ, exampleU=exampleU, picture_cid=picture_cid[1:-1]), subtype = 'html')

    with open("file name/" + example_pic, 'rb') as img:
        msg.get_payload()[0].add_related(img.read(), 'image', 'jpeg', cid=picture_cid)

    email = "sender@email.com"
    password = ""

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.send_message(msg)
        server.quit()

#schedule email daily
schedule.every().day.at("15:00").do(mail)
while True:
    schedule.run_pending()
    time.sleep(1)

