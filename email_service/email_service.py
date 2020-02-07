import re
from html.parser import HTMLParser


class EmailAccount(object):
    ''' A class to represent an email account

    Attributes
    ----------
    email_address : str
        email address associated with the email account

    name : str
        display name of the email account

    Raises:
        ValueError: If email_address is not of proper format or name is missing
    '''
    def __init__(self, email_address: str, name: str) -> None:
        email_address = email_address.strip()
        if not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email_address):
            raise ValueError('Invalid email address format')

        self.email_address = email_address
        name = name.strip()
        if name == '':
            raise ValueError('Missing name')

        self.name = name


class EmailService(object):
    ''' A class to perform email sending operation

    Attributes
    ----------
    external_api
        api that does the actual email sending

    Raises:
        ValueError: If body is empty
    '''
    def __init__(self, external_api) -> None:
        self.external_api = external_api

    def send_email(self,
                   recipient: EmailAccount,
                   sender: EmailAccount,
                   subject: str,
                   body: str) -> bool:

        subject = subject.strip()
        if subject == '':
            subject = '(no subject)'

        html_remover = EmailHTMLRemover()
        html_remover.feed(body)

        body = html_remover.get_data()

        if body == '':
            raise ValueError('Empty email body')

        return self.external_api.send(recipient, sender, subject, body)


class EmailHTMLRemover(HTMLParser):
    ''' A class to remove HTML tags from email body. This is VERY rudimentary
    and will remove ALL contents enclosed by angle brackets.
    '''
    def __init__(self):
        self.reset()
        self.convert_charrefs = True
        self.data = []

    def handle_data(self, d):
        cleaned_data = d.strip()
        if cleaned_data != '':
            self.data.append(cleaned_data)

    def get_data(self):
        return ' '.join(self.data)
