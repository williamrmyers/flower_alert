# Python program to scrape website
# and save quotes from website
import os
from os import path
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import json

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


tempfilename = "prev-stock.json"
# Check if temp file exists
if not path.exists(tempfilename):
    print('Creating File:', tempfilename)
    # Creates File
    f = open(tempfilename, "x")
    # The first time it runs, you will always have new stock.
    new_stock = True

else:
    # Read in file
    with open(tempfilename, "r") as read_file:
        prev_stock = json.load(read_file)
        # Compare new list to old
        # Set bool to indicate that number of avalable flowers has changed.
        if(len(urls) > len(prev_stock)):
            print('New Stock')
            new_stock = True
        else:
            print('no new Stock')
            new_stock = False

# Write to file with new stock list
with open(tempfilename, "w") as write_file:
    json.dump(urls, write_file)

# Seperate Urls into comma seperated Values
urlsString = '\n\n'.join(map(str, urls))


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


# Notify user of count is above 1 & if the number of urls is greater than earlier run
# First condition is counting the number of non flower items like pots
if (new_stock == True):
    sendText()
else:
    print('No Hoyas avalable')
