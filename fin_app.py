'''
This script demonstrates the power of using API's to perform quality-of-life automation
We use Yahoo! Finance's API to retrieve data. Documentation can be found here: https://python-yahoofinance.readthedocs.io/en/latest/api.html
'''

# imports
# these specify Python libraries that you would like to use as part of our program
import sys # to extract command line arguments
import os.path # for access to file system
import json # to read .json config file
import requests # to make HTTP requests
import base64 # for email encoding
from email.mime.text import MIMEText # to include HTML in email
from email.mime.multipart import MIMEMultipart # to include HTML in email
from googleapiclient.discovery import build # Gmail API
from google_auth_oauthlib.flow import InstalledAppFlow # Gmail API
from google.auth.transport.requests import Request # Gmail API
from google.oauth2.credentials import Credentials # Gmail API

SCOPES = ['https://www.googleapis.com/auth/gmail.send'] # define the OAuth scope to be send-only

# read in a config file
def parse_config(path):
    data = None
    with open(path) as f:
        data = json.load(f)
    return data

# make API request via HTTP
def api_request(endpoint, uri):
    target = '{}/{}'.format(endpoint, uri)
    res = requests.get(target)
    res.raise_for_status()
    out = res.json()["optionChain"]["result"][0]["quote"]
    return {'price': out["regularMarketPrice"], 'change': out["regularMarketChangePercent"]}

# generate an HTML report of the provided data
def generate_report(sp_data, ticker_data, threshold):
    to_capture = []
    for t in ticker_data:
        test = abs(t['change'] - sp_data['change'])
        if test > threshold:
            to_capture.append(t)
    html = "<html><body><div><p>See below for the day's interesting stocks report.</p><br>"
    for t in to_capture:
        html = '{}<div><p>Symbol: {}</p><p>Stock Price: ${}</p><p>% Change: {}</p><br>'.format(html, t["symbol"], t["price"], t["change"])
    html = '{}</div></body></html>'.format(html)
    return html

# gain access to Gmail API
# see https://developers.google.com/gmail/api/quickstart/python for more information
def email_auth (base_path):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_path = os.path.join(base_path, 'token.json')
    creds_path = os.path.join(base_path, 'credentials.json')
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

# send an email to a recipient
def send_email(sender, recipient, msg, base_path):
    service = email_auth(base_path) # authenticate to Gmail
    
    # craft the message
    message = MIMEMultipart("alternative") # allows for combination of plain text and HTML
    message["Subject"] = "Daily Stock Report"
    message["From"] = sender
    message["To"] = recipient
    part1 = MIMEText(msg, "html")
    message.attach(part1)
    to_send = {'raw': base64.urlsafe_b64encode(bytes(message.as_string(), 'utf-8')).decode('utf-8')} # yeah, this is annoying...

    # send the message
    service.users().messages().send(userId=sender, body=to_send).execute()

# main method to generate the daily financial report
def collect_fin_data (base_path):
    try:
        print ("Beginning financial report creation...")
        config = parse_config(os.path.join(base_path, "config.json")) # read config file
        ticker_data = []
        sp_data = api_request(config['endpoint'], '/v7/finance/options/{}'.format(config['s&p'])) # get S&P data
        for symbol in config['tickers']: # get each specified company's data
            try:
                curr_data = api_request(config['endpoint'], '/v7/finance/options/{}'.format(symbol))
                curr_data["symbol"] = symbol
                ticker_data.append(curr_data)
            except Exception as e:
                print ('Skipping symbol {} due to API retrieval error.'.format(symbol))
        report = generate_report(sp_data, ticker_data, config["threshold"]) # generate stock report based on data
        print ("Report generated. Sending via email...")
        send_email(config['sender'], config['recipient'], report, base_path) # send out stock report
        print ("Report successful sent!")
    except Exception as e:
        print (e)
        pass

# main entry point for the application
# this conditional allows for our module to be used in other modules if needed
if __name__ == "__main__":
    base_path = "" # default path to base app directory (=cwd)
    if len(sys.argv) > 1: # try to grab base path from the command line
        base_path = str(sys.argv[1])
    collect_fin_data(base_path)
