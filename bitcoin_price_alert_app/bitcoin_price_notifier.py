# Bitcon Price Alert V0.5
# A python app that fetches the current price of bitcoins and sends notifications via Telegram IFTTT or Email
# to run this program type python bitcoin_alert_prototype1 -e 10000 -t 60 -d gmail

# v0.5 integration of twitter notification and android sms 

# importing the required modules

import requests
import time
import json
import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from requests import Request, Session

# the coinmarketcap api url
BITCOIN_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

# setting the parameters to send with the above url to fetch INR converted BTC value
parameters = {
    'start': '1',
    'limit': '1',
    'convert': 'INR'
}
# setting the http header to recive the data in a json format
headers = {
    'Accepts': 'application/json',

    # coinmarketcap individual key
    'X-CMC_PRO_API_KEY': 'eefc4ab7-05d5-458d-8dfe-7297fe574a9d',
}

# ifttt webhook-telegram applet url to send notofications on telegram
IFTTT_WEBHOOKS_TELEGRAM = "https://maker.ifttt.com/trigger/bitcoin_price_update/with/key/bhU0A_GCHddT_gcdRvdW5rmVVXFl-rZittf1lV2-O3q"

# ifttt webhook-ifttt notification applet url to send notofications on ifttt app
IFTTT_WEBHOOK_PUSH_NOTIFICATION = "https://maker.ifttt.com/trigger/bitcoin_price_emergency_alert/with/key/bhU0A_GCHddT_gcdRvdW5rmVVXFl-rZittf1lV2-O3q"

# ifttt webhook-twitter post applet url to send notofications on ifttt app
IFTTT_WEBHOOK_TWITTER = "https://maker.ifttt.com/trigger/twitter-notification-applet/with/key/bhU0A_GCHddT_gcdRvdW5rmVVXFl-rZittf1lV2-O3q"

# ifttt webhook-android-sms applet url to send notofications on ifttt app
IFTTT_WEBHOOK_SMS = "https://maker.ifttt.com/trigger/android-sms-applet/with/key/bhU0A_GCHddT_gcdRvdW5rmVVXFl-rZittf1lV2-O3q"


# function to fetch the current BTC value GET Method


def bitcoin_price_alert():
    print('bitcoin_price_alert()')
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(BITCOIN_URL, params=parameters)
    data = json.loads(response.text)

    price = float(data['data'][0]['quote']['INR']['price'])
    # print(price)

    return round(price)


# function to send the telegram notification POST method
def post_ifttt_telegram(event, value):
    print('post_ifttt_telegram()')
    data = {'value1': value}

    post_event = IFTTT_WEBHOOKS_TELEGRAM.format(event)

    requests.post(post_event, json=data)

    print('Channel message has been sent')


# function to send the twit POST method
def post_ifttt_twitter(event, value):
    print('post_ifttt_twitter()')
    data = {'value1': value}

    post_event = IFTTT_WEBHOOK_TWITTER.format(event)

    requests.post(post_event, json=data)

    print('Twitt has been posted')


# function to send the android sms POST method
def post_ifttt_android_sms(event, value, phone):
    print('post_ifttt_twitter()')
    data = {'value1': value, 'value2': phone}

    post_event = IFTTT_WEBHOOK_SMS.format(event)

    requests.post(post_event, json=data)

    print('SMS has been Sent')


# function to send the ifttt notification POST method
def post_ifttt_push_notification(event, value):
    print('post_ifttt_push_notification()')
    data = {'value1': value}

    post_event = IFTTT_WEBHOOK_PUSH_NOTIFICATION.format(event)

    requests.post(post_event, json=data)

    print('Notification has been sent')


# function to send notifications in mails.
def send_emails(bitcoin_log):
    print('send_emails()')
    # fetching the current bitcoin value
    #bitcoin_current_price = bitcoin_log

    # taking the recipent details as user input
    recipent_name = input('Please enter the Recipent/Reciver Name.')
    recipent_email_address = input(
        'Please enter the Recipent/Reciver Email-id.')

    # settting up the mail default structure
    msg = MIMEMultipart()

    password1 = 'appm2020'
    msg['From'] = 'socialbeenoreply@gmail.com'
    msg['To'] = recipent_email_address

    # mail message body
    message = '\nHi, '+recipent_name+"\nBitcoin Price now at  " + \
        str(bitcoin_log) +\
        '\nAct Fast.\nBUY OR SELL NOW!!!!,\nRegards,\nFerrigo Mocha'

    # formatting and attaching the message body to the mail structure
    msg.attach(MIMEText(message, 'utf-8'))

    # creating the gmail sever to send mails
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # loging in the 'From' gmail id
    server.login(msg['From'], password1)

    # sending the mail
    server.sendmail(msg['From'], msg['To'], message)

    server.quit()

    print("successfully sent email to %s:" % (msg['To']))


# function to formate the telegram message
def telegram_message_formate(bitcoin_log):
    print('telegram_message_formate()')
    rows = []
    for bitcoin_value in bitcoin_log:
        date = bitcoin_value['date'].strftime('%d.%m.%Y %H:%M')
        value = bitcoin_value['bitcoin_current_amount']
        row = '{}: ₹ <b>{}</b>'.format(date, value)
        rows.append(row)
    return '<br>'.join(rows)

# function to formate the telegram message


def email_message_formate(bitcoin_log):
    print('email_message_formate()')
    rows = []
    for bitcoin_value in bitcoin_log:
        date = bitcoin_value['date'].strftime('%d.%m.%Y %H:%M')
        value = bitcoin_value['bitcoin_current_amount']
        row = '\nDate {}: is Rs: {}'.format(date, value)
        rows.append(row)
    return '\n'.join(rows)


# ifttt push notification master driver function that runs to fetch BTC value and send a push notification
def ifttt_master_driver(alert_limit, time_interval, bitcoin_log_lenght):
    print('Please wait from sometime the app is running you will be prompted when the notification is sent')
    bitcoin_log = []
    BITCOIN_ALERT_LMIT = float(alert_limit[0])
    TIME_INTERVAL = float(time_interval[0])
    while True:
        bitcoin_current_amount = bitcoin_price_alert()
        date = datetime.now()
        bitcoin_log.append(
            {'date': date, 'bitcoin_current_amount': bitcoin_current_amount})

        if bitcoin_current_amount < BITCOIN_ALERT_LMIT:
            post_ifttt_push_notification(
                'bitcoin_price_emergency_alert', bitcoin_current_amount)

        if len(bitcoin_log) == bitcoin_log_lenght[0]:
            post_ifttt_push_notification('bitcoin_price_update',
                                         telegram_message_formate(bitcoin_log))
            bitcoin_log = []

        time.sleep(TIME_INTERVAL*60)


# telegram notification master driver function that runs to fetch BTC value and send a telegram message
def telegram_master_driver(alert_limit, time_interval, bitcoin_log_lenght):
    print('Please wait from sometime the app is running you will be prompted when the message is sent')
    bitcoin_log = []
    BITCOIN_ALERT_LMIT = float(alert_limit[0])
    TIME_INTERVAL = float(time_interval[0])
    while True:
        bitcoin_current_amount = bitcoin_price_alert()
        date = datetime.now()
        bitcoin_log.append(
            {'date': date, 'bitcoin_current_amount': bitcoin_current_amount})

        if bitcoin_current_amount < BITCOIN_ALERT_LMIT:
            post_ifttt_telegram(
                'bitcoin_price_emergency_alert', bitcoin_current_amount)

        if len(bitcoin_log) == bitcoin_log_lenght[0]:
            post_ifttt_telegram('bitcoin_price_update',
                                telegram_message_formate(bitcoin_log))
            bitcoin_log = []

        time.sleep(TIME_INTERVAL*60)


# twitter post master driver function that runs to fetch BTC value and post on twitter account
def twitter_master_driver(alert_limit, time_interval, bitcoin_log_lenght):
    print('**Please wait from sometime the app is running you will be prompted when the message is sent')
    bitcoin_log = []
    BITCOIN_ALERT_LMIT = float(alert_limit[0])
    TIME_INTERVAL = float(time_interval[0])
    while True:
        bitcoin_current_amount = bitcoin_price_alert()
        date = datetime.now()
        bitcoin_log.append(
            {'date': date, 'bitcoin_current_amount': bitcoin_current_amount})

        if bitcoin_current_amount < BITCOIN_ALERT_LMIT:
            post_ifttt_twitter(
                'bitcoin_price_emergency_alert', bitcoin_current_amount)

        if len(bitcoin_log) == bitcoin_log_lenght[0]:
            post_ifttt_twitter('bitcoin_price_update',
                               telegram_message_formate(bitcoin_log))
            bitcoin_log = []

        time.sleep(TIME_INTERVAL*60)


# sms post master driver function that runs to fetch BTC value and sends and sms to the number
def sms_master_driver(alert_limit, time_interval, bitcoin_log_lenght):
    print('Please wait from sometime the app is running you will be prompted when the message is sent')

    phone_no = input(
        'Enter the Phone Number to send SMS. Include country code e.g. 12024561111,+911234567890----> ')

    bitcoin_log = []
    BITCOIN_ALERT_LMIT = float(alert_limit[0])
    TIME_INTERVAL = float(time_interval[0])
    while True:
        bitcoin_current_amount = bitcoin_price_alert()
        date = datetime.now()
        bitcoin_log.append(
            {'date': date, 'bitcoin_current_amount': bitcoin_current_amount})

        if bitcoin_current_amount < BITCOIN_ALERT_LMIT:
            post_ifttt_android_sms(
                'bitcoin_price_emergency_alert', bitcoin_current_amount, phone_no)

        if len(bitcoin_log) == bitcoin_log_lenght[0]:
            post_ifttt_android_sms('bitcoin_price_update',
                                   email_message_formate(bitcoin_log), phone_no)
            bitcoin_log = []

        time.sleep(TIME_INTERVAL*60)


# driver code to send BTC current value notification through email
def send_email_master_driver(alert_limit, time_interval, bitcoin_log_lenght):
    print('Please wait from sometime the app is running you will be prompted from name and mail id')
    bitcoin_log = []
    BITCOIN_ALERT_LMIT = float(alert_limit[0])
    TIME_INTERVAL = float(time_interval[0])
    while True:
        bitcoin_current_amount = bitcoin_price_alert()
        date = datetime.now()
        bitcoin_log.append(
            {'date': date, 'bitcoin_current_amount': bitcoin_current_amount})

        if bitcoin_current_amount < BITCOIN_ALERT_LMIT:
            send_emails(bitcoin_current_amount)

        if len(bitcoin_log) == bitcoin_log_lenght[0]:
            send_emails(email_message_formate(bitcoin_log))
            bitcoin_log = []

        time.sleep(TIME_INTERVAL*60)


# the master control function the heart of the app that takes imput from cmd using the argsparser libary and calls the right function and passes the argumments.
def master_control():
    print('Welcome To Bitcoin Price Alert App')
    cmd_input = argparse.ArgumentParser(
        description='Bitcoin Price Alert App.', epilog='This app gives the value of 1 BTC in INR. Destination (-d) must be provided. To recive notification on IFTTT install IFTTT mobile app. To recive notification on Telegram install Telegram mobile app and join this channel https://t.me/mybitcoinproject . Prerequisite : MUST HAVE A IFTTT APP AND TELEGRAM APP INSTALLED TO RECIVE NOTIFICATION ALSO MUST JOIN THE TELEGRAM Bit_Coin CHANNEL TO RECIVE MESSAGES. PRESS Ctrl+C to terminate the app')

    cmd_input.add_argument('-a', '--alert_amount', type=int, nargs=1, default=[
                           10000], metavar='alert_amount', help='The price of 1 bitcoin when an emergency alert will be sent. Default is 10000 USD')

    cmd_input.add_argument('-t', '--time_interval', type=int, nargs=1, default=[
                           5], metavar='time_interval', help='The time interval in minutes after which the lastest value of bitcoin will be fetched. Defalut is 5 minutes')

    cmd_input.add_argument('-l', '--log_lenght', type=int, nargs=1, default=[
                           2], metavar='log_lenght', help='The number of records/entries you want example 5 entries at 5 minutes interval. Default length is 2')

    cmd_input.add_argument('-d', '--destination_app', metavar='destination_app',
                           help='The mobile application on which you want to recive alert. Destination app options are (1) IFTTT app, (2) Telegram App, (3) Email, (4) Twitter, (5) SMS', required=True)

    args = cmd_input.parse_args()

    print('Bitcoin App started with time interval of ',
          args.time_interval[0], ' and threshold = $',  args.alert_amount[0], 'for destination ', args.destination_app)

    # this is the switch control this will call only that function that is mentioned
    # by user and transfer the control to it.
    if(args.destination_app == 'telegram'):
        print('To recive notification on Telegram install Telegram mobile app and join this channel https://t.me/mybitcoinproject .')
        telegram_master_driver(
            args.alert_amount, args.time_interval, args.log_lenght)
    if(args.destination_app == 'ifttt'):
        ifttt_master_driver(args.alert_amount,
                            args.time_interval, args.log_lenght)
    if(args.destination_app == 'email'):
        send_email_master_driver(
            args.alert_amount, args.time_interval, args.log_lenght)
    if(args.destination_app == 'twitter'):
        twitter_master_driver(
            args.alert_amount, args.time_interval, args.log_lenght)
    if(args.destination_app == 'sms'):
        sms_master_driver(
            args.alert_amount, args.time_interval, args.log_lenght)


if __name__ == '__main__':
    # calling the master control to start the app.
    master_control()