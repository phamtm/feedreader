from threading import Thread

from flask import current_app, 		\
				  render_template
from flask.ext.mail import Message

from app import mail

import os.path


def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)


def send_email(to, subject, template, **kwargs):
	app = current_app._get_current_object()

	if app.config['NO_SEND_EMAIL']:
		# Write to a temporary file
		filepath = os.path.join(app.config['TMP_DIR'], 'tmp_mail.txt')
		with open(filepath, 'a') as f:
			msg = '\n' + render_template(template + '.txt', **kwargs)
			f.write(msg)
		return
	else:
		msg = Message('[Flask] ' + subject,
						sender = app.config['MAIL_USERNAME'],
						recipients = [to])
		msg.body = render_template(template + '.txt', **kwargs)
		msg.html = render_template(template + '.html', **kwargs)

		thr = Thread(target = send_async_email, args = [app, msg])
		thr.start()

		return thr

