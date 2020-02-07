class SendgridAPI(object):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        pass

    def send(self, recipient, sender, subject, body):
        pass
