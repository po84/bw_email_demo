import re


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
    ''' A class to pergorm email sending operation

    Attributes
    ----------
    external_api
        api that does the actual email sending

    '''
    def __init__(self, external_api) -> None:
        self.external_api = external_api

    def send_email(self,
                   recipient: EmailAccount,
                   sender: EmailAccount,
                   subject: str,
                   body: str) -> bool:
        # TODO business logic for stripping html from body
        result = self.external_api.send(recipient, sender, subject, body)
        return True
