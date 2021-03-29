# Stock Market Wizard

This Python script compares financial data for a user-defined list of publicly traded companies against the S&P 500 (or some other basis). The script will generate a report of all companies from this list whose 1-day stock price % changes positively or negatively exceed the 1-day change of the basis by more than a user-specified threshold.

## Source Code Layout

The following is a high-level overview of the repository:

* __.gitignore__ => Specify files that should be ignored by source version control (git).
* __README.md__ => What you're reading - a description of how to work with the code!
* __fin_app.py__ => Our Python script that does the magic.

## Prerequisites

* [Python 3](https://www.python.org/downloads/) installed
* [requests](https://docs.python-requests.org/en/master/) library installed
* [Google API](https://developers.google.com/gmail/api/quickstart/python) libraries installed

To install requests:
```
pip install --upgrade requests
```

To install Google API:
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Note: [pip](https://pypi.org/project/pip/) is Python's default package manager. It should come with your Python 3 install.

## Configuration

You must generate a file called _config.json_ that the Python script uses for certain important information. It can be placed anywhere - this is called the "config path" of the application. The simplest config path you can use is the same folder as the Python script!

Below is an example config file that is subsequently explained:
```
{
    "endpoint": "https://query1.finance.yahoo.com",
    "s&p": "^GSPC",
    "tickers": [
        "INTC",
        "AMD",
        "NVDA",
        "TSM"
    ],
    "threshold": 1,
    "sender": "sender@gmail.com",
    "recipient": "recipient@gmail.com"
}
```

* __endpoint__ => Which API you would like to use to obtain financial data. The example uses Yahoo! Finance (undocumented).
* __s&p__ => The ticker symbol of the security you would like to use as your basis of comparison. The example uses the S&P 500.
* __tickers__ => A list of all ticker symbols of companies you would like to compare to the basis. The example is semiconductor heavy.
* __threshold__ => The % difference between the basis and each company that, if exceeded, triggers inclusion of that company in the report.
* __sender__ => Email address of the sender of the report (must be Gmail).
* __recipient__ => Email address of the recipient of the report (can be anything).

You must also enable the Gmail API on the account you wish to send the report from. Instructions for doing so can be found [here](https://developers.google.com/gmail/api/quickstart/python). The steps specified here will generate a file called _credentials.json_ for you. You must place this file in the same folder as config.json (i.e., the config path). The first time you run the Python script, you will be redirected to Gmail to authorize the app. Doing so will result in the automatic creation of a file called _token.json_ in the same folder. As long as token.json exists and is valid, you will not be redirected to Gmail when running the script subsequently.

## Running the Script

To run the Python script (after it is properly configured), use the following command:

```
python [path_to_script]/fin_app.py ([path_to_config_folder])
```

* __path_to_script__ => The path to the Python script's folder. Only needed if you are trying to run the script from somewhere else.
* __path_to_config_folder__ => The path to the folder that contains all necessary config files (config.json, credentials.json, token.json). If not specified, defaults to the current working directory.

Note: The above assumes that _python_ is in the user's path. The installation should do this for you. But if it doesn't, you must specify the full path to python.

## Authors

* **Josh Kimmel**