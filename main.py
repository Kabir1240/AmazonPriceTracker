import requests
import os
import smtplib as smtp
from bs4 import BeautifulSoup
from dotenv import load_dotenv


# get environ variables and create global variables
load_dotenv()
FROM_EMAIL = os.environ.get("FROM_EMAIL")
EMAIL_PASSWORD = os.environ.get("PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")
USER_AGENT = os.environ.get("USER_AGENT")


def send_email(from_email, from_pass, to_email, subject, message_body) -> None:
    """
    sends email from one account to another
    :return: None
    """
    with smtp.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=from_email, password=from_pass)
        connection.sendmail(
            from_addr=from_email,
            to_addrs=to_email,
            msg=f"Subject: {subject}\n\n{message_body}")


# send request to URL
headers = \
    {
        "User-Agent":USER_AGENT,
        "Accept-Language":"en-US,en;q=0.9"
    }

url = "https://appbrewery.github.io/instant_pot/"
response = requests.get(url=url, headers=headers)
response.raise_for_status()

# create soup, find relevant data
soup = BeautifulSoup(response.text, "html.parser")
price = float(soup.find(name="span", class_="a-price-whole").text + \
        soup.find(name="span", class_="a-price-fraction").text)

# if price is cheap, create and send email
if price <= 100:
    item = soup.find(name="span", id="productTitle").text.replace("\xe9", "")
    subject = "AMAZON SALE!"
    message_body = f"{item} is now {price}\n{url}"
    print(message_body)
    send_email(FROM_EMAIL, EMAIL_PASSWORD, TO_EMAIL, subject, message_body)
