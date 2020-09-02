# Python program to scrape website
# and save quotes from website
import os
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

# Get env Variables
TWILIO_ACCOUNT_ID = os.environ.get('TWILIO_ACCOUNT_ID')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')
DESTINATION_NUMBER = os.environ.get('DESTINATION_NUMBER')

# Make Request
URL = "https://gardinonursery.com/product-category/categories/hoyas/hoyas-full-list/"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')

urls = []

# Checks for "Add to Cart" Buttons
for row in soup.findAll('a',
                        attrs={'class': 'button'}
                        ):
    if (row.getText() == "Add to cart"):
        urls.append("https://gardinonursery.com/" + row['href'])

# Seperate Urls into comma seperated Values
urlsString = ''.join(map(str, urls))

body = f'{len(urls)} Hoyas are avalable! Thay\'re at these URLs {urlsString}'


def sendText():
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = TWILIO_ACCOUNT_ID
    auth_token = TWILIO_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=body,
                        from_='+14159174763',
                        to=DESTINATION_NUMBER
                    )
    print(message.sid)


# Notify user of count is above 1
if (len(urls) > 1):
    sendText()
else:
    print('Only 1 Url')
