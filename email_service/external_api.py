import json
import requests


class SendgridAPI(object):
    def __init__(self, api_key: str) -> None:
        self.send_mail_endpoint = 'https://api.sendgrid.com/v3/mail/send'
        self.token_string = 'Bearer {}'.format(api_key)

    def send(self, recipient, sender, subject, body):
        data = {
            'personalizations': [
                {
                    'to': [
                        {'email': recipient.email_address,
                         'name': recipient.name}
                    ]
                }
            ],
            'from': {'email': sender.email_address,
                     'name': sender.name},
            'subject': subject,
            'content': [
                {'type': 'text/plain',
                 'value': body}
            ]
        }

        headers = {'Authorization': self.token_string,
                   'Content-Type': 'application/json'}

        send_result = requests.post(self.send_mail_endpoint,
                                    headers=headers,
                                    data=json.dumps(data))

        if send_result.status_code == 202:
            return True
        else:
            return False


class MailgunAPI:
    def __init__(self, api_key: str) -> None:
        self.send_mail_endpoint = 'https://api.mailgun.net/v3/sandbox8fa3c3ceac1a4b12aeeb3f202ebe3b68.mailgun.org/messages'
        self.api_key = api_key

    def send(self, recipient, sender, subject, body):
        data = {'from': '{name} <{email}>'.format(name=sender.name,
                                                  email=sender.email_address),
                'to': [recipient.email_address],
                'subject': subject,
                'text': body}

        send_result = requests.post(self.send_mail_endpoint,
                                    auth=('api', self.api_key),
                                    data=data)

        if send_result.status_code == 200:
            return True
        else:
            return False
