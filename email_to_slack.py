import imaplib
from imapclient import IMAPClient
from slack_sdk import WebClient
from dotenv import load_dotenv
import os
import email
from email.header import decode_header
import time
from bs4 import BeautifulSoup

# Load environment variables from .env file

load_dotenv()

client = IMAPClient('imap.titan.email')
client.login('dispatch@javarepair.com', 'jimsjava123')
print('login successful')


# Slack settings
SLACK_TOKEN = "xoxb-7230977860530-7390680074567-oUUuwgKGp9U1MH3lq8BiwTXC"

# Function to fetch emails
def fetch_emails():
    client.select_folder('INBOX')

        # Search for unseen messages
    messages = client.search(['UNSEEN'])
    print('checking for new emails...')
    
    for uid, message_data in client.fetch(messages, "RFC822").items():
            email_message = email.message_from_bytes(message_data[b"RFC822"])
            print(uid, email_message.get("From"), email_message.get("Subject"))
            sender = email_message.get("From")
            # Process based on sender
            if sender in ['sadmin@firstservicenetworks.com', 'example@vixxo.com']:
                # Example: Extract subject and body
                subject = email_message.get('Subject')
                body = email_message.get_payload(decode=True).decode()
                soup = BeautifulSoup(body, 'html.parser')
                output = str(soup.prettify())
                print(output)
                
                # Format message for Slack
                slack_message = "*From:* {sender}\n*Subject:* {subject}\n{body}"

                # Post message to Slack
                slack_client = WebClient(token= SLACK_TOKEN)
                channel_id = "vixxo"
                    
                response = slack_client.chat_postMessage(
                channel= channel_id,
                text= body)
                print("Message sent successfully:", response['ts'])  # Print timestamp of the message

                # Mark email as read (optional)
                #client.add_flags([msg_id], [imaplib.SEEN])

# Main loop
while True:
    fetch_emails()
    print('./.')
    time.sleep(300)  # Sleep for 5 minutes (300 seconds)
