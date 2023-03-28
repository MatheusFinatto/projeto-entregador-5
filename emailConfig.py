from flask import Flask, render_template
from flask_mail import Mail, Message

def sendRecoverCode(code, email, mail):
    msg = Message('Steam Verde - Recover Password!', sender = 'peter@mailtrap.io', recipients = [email])
    # msg.body = "Hello! Here's your recover password code: "
    msg.html = render_template('recover-code-email.html', code=code)
    mail.send(msg)
    return True