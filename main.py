import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os

AMAZON_ENDPOINT = os.environ.get("AMAZON_ENDPOINT")
MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("PASSWORD")

headers = {
    "User-Agent":"Defined",
    "Accept-Language":"pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(AMAZON_ENDPOINT,headers=headers)

web_page = response.text

soup = BeautifulSoup(web_page,'lxml')

price = float(soup.select(selector=".a-offscreen")[0].getText().split("$")[1])
product_title = soup.select(selector='#productTitle')[0].getText().strip()


if price < 100.0:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        message = f"Subject:Amazon Price Alert!\n\n{product_title}\nnow: ${price}\n{AMAZON_ENDPOINT}"
        message = message.encode('utf-8')
        connection.sendmail(from_addr=MY_EMAIL, 
                    to_addrs="t11324218@outlook.com", 
                    msg=message) 