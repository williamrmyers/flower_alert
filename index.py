#!/usr/bin/env python3

# Python program to scrape website
# and save quotes from website
import os
from os import path
import requests
import time
from bs4 import BeautifulSoup
from twilio.rest import Client
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Get env Variables
TWILIO_ACCOUNT_ID = os.environ.get('TWILIO_ACCOUNT_ID')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')
DESTINATION_NUMBER = os.environ.get('DESTINATION_NUMBER')


# Options for Selenium
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


# driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
# In linux this is "/usr/bin/chromedriver"
dr = webdriver.Chrome(options=chrome_options)
dr.get( "https://gardinonursery.com/product-category/categories/hoyas/hoyas-list-full/")
soup = BeautifulSoup(dr.page_source,"html5lib")

# Links to Avalable Products
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
            new_stock = True
        else:
            new_stock = False

# Write to file with new stock list
with open(tempfilename, "w") as write_file:
    json.dump(urls, write_file)

# Seperate Urls into comma seperated Values
urlsString = '\n\n'.join(map(str, urls))


body = f'{len(urls)} Hoyas are avalable! Thay\'re at these URLs {urlsString}'

# Get current time
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)


def sendText():
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = TWILIO_ACCOUNT_ID
    auth_token = TWILIO_TOKEN
    client = Client(account_sid, auth_token)
    print('Sending to:', DESTINATION_NUMBER)

    message = client.messages \
                    .create(
                        body=body,
                        from_='+14159174763',
                        to=DESTINATION_NUMBER
                    )
    print(current_time,"Message Sent" ,message.sid)


# Notify user of count is above 1 & if the number of urls is greater than earlier run
# First condition is counting the number of non flower items like pots
if (new_stock == True):
    sendText()
else:
    print(current_time,': No Hoyas avalable')