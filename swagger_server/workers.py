from celery import Celery
import os
import requests
from flask_mail import Mail, Message
from flask import Flask
import re

REDIS = os.environ['REDIS']
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

mail_config = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 465,
    'MAIL_USERNAME': 'p.l.a.n.t.s.amw@gmail.com',
    'MAIL_PASSWORD': 'plants30l',
    'MAIL_USE_TLS': False,
    'MAIL_USE_SSL': True
}

mail_app = Flask(__name__)

for key in mail_config:
    mail_app.config[key] = mail_config[key]


def make_celery():
    celery = Celery(
        __name__,
        backend=REDIS,
        broker=REDIS
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery()


@celery.task()  # pragma: no cover
def notify(address, data):  # pragma no cover
    if not EMAIL_REGEX.match(address):
        requests.put(address, json=data, headers={'Content-Type': 'application/json'})
    else:
        print('Sending mails...')

        mail = Mail(mail_app)
        mail.init_app(mail_app)

        print('Sending email to %s' % address)
        msg = Message('P.L.A.N.T.S. notification', sender=mail_config['MAIL_USERNAME'], recipients=[address])
        msg.body = str(data)
        with mail_app.app_context():
            mail.send(msg)
        print('All mails are sent')


@celery.task()  # pragma: no cover
def check_event(data, events):  # pragma: no cover
    print('celery check')
    match_value = False

    for e in events:
        event_param = e['data']

        if hasattr(event_param, 'sensor') is False:
            print('here')
            print(e)
            notify.delay(e['return_address'], data)

        elif data['sensor'] == event_param['sensor']:
            if hasattr(event_param, 'min_value') and hasattr(event_param, 'max_value'):
                if event_param['min_value'] <= data['value'] <= event_param['max_value']:
                    match_value = True
            elif hasattr(event_param, 'min_value'):
                if event_param['min_value'] <= data['value']:
                    match_value = True
            elif hasattr(event_param, 'max_value'):
                if event_param['max_value'] >= data['value']:
                    match_value = True
            else:
                match_value = True
            print('match value is'+ match_value)
            if match_value:
                notify.delay(e['return_address'], data)
