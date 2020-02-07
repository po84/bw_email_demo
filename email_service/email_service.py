class EmailAccount(object):
    ''' A class to represent an email account

    Attributes
    ----------
    email_address : str
        email address associated with the email account

    naame : str
        display name of the email account

    '''
    def __init__(self, email_address: str, name:str) -> None:
        pass


class EmailService(object):
    def __init__(self, external_api) -> None:
        self.external_api = external_api

    def send_email(self,
                   recipient: EmailAccount,
                   sender: EmailAccount,
                   subject: str,
                   body: str) -> bool:
        # TODO business logic for stripping html from body
        result = self.external_api.send(recipient, sender, subject, body)
