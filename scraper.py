import requests
from bs4 import BeautifulSoup
import smtplib
import time

# Input the product's url
url = 'https://example.com'
# Input the e-mail from which you will automatically send notifications
sender = 'test@mail.com'
# Input your password
password = 'test123'
# Input the e-mail where you wish to receive the notifications
receiver = 'test2@mail.com'

# Type "My User Agent" in Google and paste the result as value for the key 'user-agent'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}


def check_price():
    # Input your target price
    target_price = 797

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Pass the HTML element and attribute in the title and price_str
    title = soup.find('h1', {'class': 'hidden-xs'}).get_text()
    print(f'Product "{title}" found, please wait...')
    price_str = soup.find('span', {'class': 'price'}).get_text()

    price_converted = float(''.join([x for x in price_str if not x.isalpha()]).strip().replace(',', '.'))

    if price_converted < target_price:
        send_mail()


def send_mail():
    # Find your e-mail provider's host and port values and simply pass them into the SMTP function below
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(sender, password)

    subject = 'Price is lower than last time!'
    body = f'Visit {url} to check it out!'

    msg = f"Subject: {subject}\n\n {body}"

    server.sendmail(from_addr=sender, to_addrs=receiver, msg=msg)

    print('E-MAIL SENT!')

    server.quit()


while True:
    check_price()
    time.sleep(60)
