from unittest import TestCase, mock
from email_service import EmailAccount, EmailService
from external_api import SendgridAPI


class EmailAccountTest(TestCase):
    def test_new_email_account_proper_email_address_and_name(self):
        email_account = EmailAccount('test@example.com', 'Email Tester')
        self.assertEqual(email_account.email_address, 'test@example.com')
        self.assertEqual(email_account.name, 'Email Tester')

    def test_new_email_account_bad_email_address(self):
        self.assertRaises(ValueError,
                          EmailAccount,
                          'this is not a good email address format',
                          'Email Tester')

    def test_new_email_account_missing_name(self):
        self.assertRaises(ValueError,
                          EmailAccount,
                          'test@example.com',
                          '')


class EmailServiceTest(TestCase):
    def test_send_email_call_ext_api_send(self):
        mock_api = mock.create_autospec(SendgridAPI)

        email_service = EmailService(mock_api)
        recipient = EmailAccount('to@example.com', 'To Me')
        sender = EmailAccount('from@example.com', 'From You')
        subject = 'Test subject'
        body = 'body is not empty'
        email_service.send_email(recipient,
                                 sender,
                                 subject,
                                 body)

        mock_api.send.assert_called_with(recipient, sender, subject, body)
