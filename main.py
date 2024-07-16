import requests
import os
import smtplib as smtp
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()
FROM_EMAIL = os.environ.get("FROM_EMAIL")
EMAIL_PASSWORD = os.environ.get("PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")


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
            msg=f"{subject}\n\n{message_body}")


url = "https://appbrewery.github.io/instant_pot/"
response = requests.get(url=url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
price = float(soup.find(name="span", class_="a-price-whole").text + \
        soup.find(name="span", class_="a-price-fraction").text)

if price <= 100:
    item = soup.find(name="span", id="productTitle").text.replace("\xe9", "")
    subject = "AMAZON SALE!"
    message_body = f"{item} is now {price}\n{url}"
    print(message_body)
    send_email(FROM_EMAIL, EMAIL_PASSWORD, TO_EMAIL, subject, message_body)
