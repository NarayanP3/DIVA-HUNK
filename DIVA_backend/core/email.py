from django.core.mail import send_mail
import random
from django.conf import settings
from .models import Voter


def sendEmailOTP(email):
    user_obj = None;
    subject = 'Your email verification email'
    otp = random.randint(100000, 999999)
    message = 'Your otp is '+ str(otp)
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])
    try:
        user_obj = Voter.objects.get(email=email)
    except Voter.MultipleObjectsReturned:
        user_obj = Voter.objects.filter(email=email).first()
    except Voter.DoesNotExist:
        print(f"No voter found with that email");
    finally:
        if user_obj:
            user_obj.otp = otp
            user_obj.save()
