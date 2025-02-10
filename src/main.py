import smtplib
import logging
import os
from email.mime.text import MIMEText

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

email_address = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')
smtp_server = 'smtp.gmail.com'  
smtp_port = 587  


recipient_phone_number = input('Enter the recipient\'s phone number: ')
carrier_gateway = 'vtext.com'  


message_body = 'This was sent at 2:13 On monday'

CARRIER_GATEWAYS = {
    'AT&T': 'txt.att.net',
    'Verizon': 'vtext.com',
    'T-Mobile': 'tmomail.net',
    'Sprint': 'messaging.sprintpcs.com',
    'Virgin Mobile': 'vmobl.com',
    'MetroPCS': 'mymetropcs.com',
    'Boost Mobile': 'sms.myboostmobile.com',
    'Cricket': 'sms.cricketwireless.net',
    'Google Fi': 'msg.fi.google.com',
    'US Cellular': 'email.uscc.net'
}

def send_sms_via_email(email, password, smtp_server, smtp_port, phone_number, carrier_gateway, message):
    try:
        recipient_email = f'{phone_number}@{carrier_gateway}'

        msg = MIMEText(message)
        msg['From'] = email
        msg['To'] = recipient_email
        msg['Subject'] = '' 

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email, password) 
            server.sendmail(email, recipient_email, msg.as_string())

        logging.info(f"SMS sent successfully to {phone_number} via {carrier_gateway}!")
        return True

    except smtplib.SMTPException as e:
        logging.error(f"Failed to send SMS: SMTP error - {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False

if send_sms_via_email(email_address, email_password, smtp_server, smtp_port, recipient_phone_number, carrier_gateway, message_body):
    logging.info("SMS sent successfully!")
else:
    logging.error("Failed to send SMS.")