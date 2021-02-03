from bs4 import BeautifulSoup
import requests
import re
import smtplib
import ssl

port = 587
smtp_server = "smtp.gmail.com"
sender_email = "aldal.bugra@gmail.com"
receiver_email = "aldal.bugra@gmail.com"
password = "PASSWORD123"

source = requests.get(
    "https://www.timeanddate.com/weather/turkey/denizli").text
soup = BeautifulSoup(source, "lxml")
comment = soup.findAll("p")
comment_text = re.search(r"<p>(.*?)</p>", str(comment)).group(0)[3:-4]
degree_lab = soup.findAll("div", {"class": "h2"})
degrees = re.search(r">(.*?)°C", str(degree_lab)).group(0)[1:]

message = u' '.join((degrees, comment_text)).encode('utf-8').strip()


context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
