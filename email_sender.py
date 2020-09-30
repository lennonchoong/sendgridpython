import os
import sys
import base64

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Email, Content, Cc, Bcc, Personalization, Attachment, FileContent, FileName, FileType, Disposition)

def send_email(string):
    input_string = string.split("&")
    hashset = {}

    for substring in input_string:
        key, val = substring.split("=")
        hashset[key] = val.replace("'", "")

    message = Mail()

    for key in hashset:
        if key == "to_emails":
            personalization = Personalization()
            for emails in hashset[key].split(";"):
                personalization.add_to(Email(emails))
            message.add_personalization(personalization)
        elif key == "content":
            message.add_content(Content(hashset['content_type'], hashset[key]))
        elif key == "cc_email":
            for emails in hashset[key].split(";"):
                message.add_cc(Cc(emails))
        elif key == "bcc_email":
            for emails in hashset[key].split(";"):
                message.add_bcc(Bcc(emails))
        elif "attachment" in key and "_type" not in key:
            attached_file = Attachment()
            with open(hashset[key], 'rb') as f:
                data = f.read()
                f.close()
            encoded_file = base64.b64encode(data).decode()
            attached_file.file_content = FileContent(encoded_file)
            attached_file.file_name = FileName(hashset[key][hashset[key].rfind("/") + 1:])
            attached_file.file_type = FileType(hashset[key + "_type"])
            attached_file.disposition =  Disposition('attachment')
            message.add_attachment(attached_file)
        else:
            setattr(message, key, hashset[key])

    #Use own API Key
    sg = SendGridAPIClient("")
    response = sg.send(message)
    print("REQUEST BODY : " + str(message.get()))
    print(response.status_code, response.body, response.headers)

send_email(sys.argv[1])