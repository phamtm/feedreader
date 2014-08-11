from threading import Thread

from flask import current_app,      \
                  render_template
from flask.ext.mail import Message

from app import mail

import os.path


def send_async_email(app, msg):
    """Send an email to user.
    :param app: The flask app
    :param msg: The message body
    """

    with app.app_context():
        mail.send(msg)


def send_email(recipient, subject, template, **kwargs):
    """Send an email to user asynchronously. If *NO_SEND_EMAIL* is set, log
    the email into *tmp/tmp_mail.txt* instead of actually sending it.
    :param recipient: The recipient of the email
    :param subject: The subject of the email
    :param template: The path to the template file
    """

    app = current_app._get_current_object()

    if app.config['NO_SEND_EMAIL']:
        # Write to a temporary file
        filepath = os.path.join(app.config['TMP_DIR'], 'tmp_mail.txt')
        with open(filepath, 'a') as outfile:
            msg = '\n' + render_template(template + '.txt', **kwargs)
            outfile.write(msg)
        return
    else:
        msg = Message('[Flask] ' + subject,
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[recipient])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)

        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()

        return thr
