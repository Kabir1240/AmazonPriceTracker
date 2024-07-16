import requests
import os
import smtplib as smtp
from bs4 import BeautifulSoup
from dotenv import dot_env


FROM_EMAIL = os.environ.get("email")
EMAIL_PASSWORD = os.environ.get("password")

def send_email(self, from_email, from_pass, to_email, subject, message_body) -> None:
    """
    sends email from one account to another
    :return: None
    """
    with smtp.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=from_email, password=from_pass)
        connection.sendmail(
            from_addr=from_email,
            to_addr=to_email,
            msg=f"{subject}\n\n{message_body}")


url = "https://appbrewery.github.io/instant_pot/"
response = requests.get(url=url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
price = float(soup.find(name="span", class_="a-price-whole").text + \
        soup.find(name="span", class_="a-price-fraction").text)

if price <= 100:
    print(FROM_EMAIL, EMAIL_PASSWORD)