from .models import User
from .apis import passwordManager

def notify(name,email):
    users = User.objects.all()
    emails = []
    subject = f"Today's {name}'s birthday."
    message = subject + f" This email was sent on the behalf of {name} You can further visit our website to wish or you can email {name} on {email}.\n \n Regards Nested.com"
    for user in users:
        email_users = user.email
        emails.append(email_users)
    one_time_obj = passwordManager()
    if one_time_obj.mailer(1,emails,subject,message,not_bulk=False):
        return True
    raise ValueError("Email Not sent.")