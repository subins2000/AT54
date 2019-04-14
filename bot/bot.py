from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from telegram.ext import Updater, CommandHandler

import dataset
import smtplib


'''
CONFIG
'''
bot_key = '839558171:AAHysB91aSJ38Tz4eKRp3bXhnyUwUT3w-GM'
sysadmin_email = 'sysadmin@outlook.com'

smtp_config = {
    'host': 'smtp.gmail.com',
    'port': 587,
    'username': '',
    'password': ''
}
'''
END CONFIG
'''

db = dataset.connect('sqlite:///db.sqlite3')
failures = db['failures']

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def help(bot, update):
    update.message.reply_text(
        '/'
    )

updater = Updater(bot_key)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('help', help))

def send_mail(send_from, send_to, subject, message, files=[],
              server="localhost", port=587, username='', password='',
              use_tls=True):
    '''Compose and send email with provided info and attachments.
    https://stackoverflow.com/a/16509278/1372424

    Args:
        send_from (str): from name
        send_to (list[str]): to name
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    '''

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.ehlo()
        smtp.starttls()

    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

def callback_minute(bot, context):
    non_reported = failures.find(reported=0)

    for r in non_reported:
        msg = '''%s %s predicted to fail.
Likely to fail before %s
Probability : %s
''' % (r['serial_number'], r['model'], r['failure_when'], r['probability'])

        bot.send_message(
            '@AT54Notify',
            text=msg,
        )

        try:
            send_mail(
                'AT54Notify',
                [sysadmin_email],
                'HDD Failure Prediction',
                msg,
                [],
                smtp_config['host'],
                smtp_config['port'],
                smtp_config['username'],
                smtp_config['password'],
                True
            )
        except:
            print('Failed sending email')

        failures.update({
            'id': r['id'],
            'reported': 1
        }, ['id'])

        db.commit()

job_queue = updater.job_queue

# Periodically save jobs
job_queue.run_repeating(callback_minute, interval=60, first=0)

updater.start_polling()
updater.idle()