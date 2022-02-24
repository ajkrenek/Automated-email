import requests, bs4, smtplib, ssl, random, schedule, time
from email.message import EmailMessage


#setting up email/message
def mail():
#random quote
    with open('example.txt', 'r') as f:
            read = f.read()
            array = read.split('\n')
            quote = random.choice(array)

    port = 465

    msg = EmailMessage()
#joannagarcia122@gmail.com
    msg["Subject"] = "Love Test"
    msg["From"] = ""
    msg["To"] = ""
    msg.set_content(quote)

    email = ""
    password = ""

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.send_message(msg)
        server.quit()

#schedule email daily
schedule.every(10).seconds.do(mail)
while True:
    schedule.run_pending()
    time.sleep(1)
