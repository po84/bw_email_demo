from flask import Flask, request, abort
from ..email_service.email_service import EmailAccount, EmailService
from ..email_service.external_api import SendgridAPI, MailgunAPI


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')
    ext_email_service = app.config.get('EXTERNAL_EMAIL_API')
    if ext_email_service == 'mailgun':
        ext_email_api = MailgunAPI(app.config.get('MAILGUN_API_KEY'))
    else:
        ext_email_api = SendgridAPI(app.config.get('SENDGRID_API_KEY'))

    @app.route('/email', methods=['POST'])
    def send_email():
        if not request.is_json:
            abort(400)

        request_data = request.get_json()
        if not request_data:
            abort(400)

        recipient = _build_recipient(request_data)
        sender = _build_sender(request_data)

        if 'subject' not in request_data:
            abort(400, _missing_data_msg('subject'))

        subject = request_data['subject']

        if 'body' not in request_data:
            abort(400, _missing_data_msg('body'))

        body = request_data['body']

        email_service = EmailService(ext_email_api)

        try:
            send_succeeded = email_service.send_email(recipient,
                                                      sender,
                                                      subject,
                                                      body)
        except ValueError as e:
            abort(400, str(e))

        if not send_succeeded:
            abort(500)

        return 'OK'
    return app


def _build_recipient(json_data):
    if 'to' not in json_data:
        abort(400, _missing_data_msg('to'))
    if 'to_name' not in json_data:
        abort(400, _missing_data_msg('to_name'))

    email = json_data['to']
    name = json_data['to_name']

    try:
        return EmailAccount(email_address=email,
                            name=name)
    except ValueError as e:
        abort(400, str(e))


def _build_sender(json_data):
    if 'from' not in json_data:
        abort(400, _missing_data_msg('from'))
    if 'from_name' not in json_data:
        abort(400, _missing_data_msg('from_name'))

    email = json_data['from']
    name = json_data['from_name']

    try:
        return EmailAccount(email_address=email,
                            name=name)
    except ValueError as e:
        abort(400, str(e))


def _missing_data_msg(field_name):
    return 'Missing required field: {}'.format(field_name)
