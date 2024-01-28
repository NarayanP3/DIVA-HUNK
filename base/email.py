from django.core.mail import send_mail
import random
from django.conf import settings
from .models import Voter


def sendEmailOTP(email):
    subject = 'Your email verification email'
    otp = random.randint(100000, 999999)
    message = 'Your otp is '+ str(otp)
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])
    user_obj = Voter.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()