from django.core.mail import send_mail, EmailMessage

def send_email():
    subject = 'タイトル'
    message = '本文'
    from_email = 'no-reply@shiftmanagementapp.com'
    to_emails = ['y.takumi4@gmail.com']
    email = EmailMessage(
        subject,
        message,
        from_email,
        to_emails
        )
    email.send()
