import os
import sys
import base64

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)

def send_email():
    message = Mail(
        from_email='lennonchoong@gmail.com',
        to_emails='lennonchoong@yahoo.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>'
    )

    with open(sys.argv[1], 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName(str(sys.argv[1])), #File directory
        FileType(str(sys.argv[2])), #MIME type
        Disposition('attachment')
    )
    message.attachment = attachedFile

    #Use own API Key
    sg = SendGridAPIClient("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")
    response = sg.send(message)
    print(response.status_code, response.body, response.headers)

send_email()