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

    def test_send_email_call_ext_api_send_with_empty_subject(self):
        mock_api = mock.create_autospec(SendgridAPI)

        email_service = EmailService(mock_api)
        recipient = EmailAccount('to@example.com', 'To Me')
        sender = EmailAccount('from@example.com', 'From You')
        body = 'body is not empty'
        email_service.send_email(recipient,
                                 sender,
                                 '',
                                 body)

        mock_api.send.assert_called_with(recipient,
                                         sender,
                                         '(no subject)',
                                         body)

    def test_send_email_call_ext_api_send_with_empty_body(self):
        mock_api = mock.create_autospec(SendgridAPI)

        email_service = EmailService(mock_api)
        recipient = EmailAccount('to@example.com', 'To Me')
        sender = EmailAccount('from@example.com', 'From You')
        subject = 'Test subject'
        body = ''
        self.assertRaises(ValueError,
                          email_service.send_email,
                          recipient,
                          sender,
                          subject,
                          body)

    def test_send_email_call_ext_api_send_with_body_containing_html(self):
        mock_api = mock.create_autospec(SendgridAPI)

        email_service = EmailService(mock_api)
        recipient = EmailAccount('to@example.com', 'To Me')
        sender = EmailAccount('from@example.com', 'From You')
        subject = 'Test subject'
        body = '<h1>Your Bill</h><p>$10</p>'
        email_service.send_email(recipient,
                                 sender,
                                 subject,
                                 body)

        mock_api.send.assert_called_with(recipient,
                                         sender,
                                         subject,
                                         'Your Bill $10')
    # these were used to make sure the API calls work, commented out because
    # they are not really unit tests
    # def test_send_email_with_sendgrid(self):
    #     sendgrid_api = SendgridAPI('')
    #     email_service = EmailService(sendgrid_api)
    #     recipient = EmailAccount('potong616@gmail.com', 'Po Tong')
    #     sender = EmailAccount('po.tmp.test@gmail.com', 'Po Tong')
    #     subject = 'Test subject'
    #     body = 'body is not empty'
    #     email_service.send_email(recipient,
    #                              sender,
    #                              subject,
    #                              body)

    # def test_send_email_with_mailgun(self):
    #     mailgun_api = MailgunAPI('')
    #     email_service = EmailService(mailgun_api)
    #     recipient = EmailAccount('potong616@gmail.com', 'Po Tong')
    #     sender = EmailAccount('po.tmp.test@gmail.com', 'Po Tong')
    #     subject = 'Test subject'
    #     body = 'body is not empty'
    #     email_service.send_email(recipient,
    #                              sender,
    #                              subject,
    #                              body)
