from django.core.mail import send_mail
import random
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Voter

def sendEmailOTP(email):
    subject = 'Your email verification email'
    otp = random.randint(100000, 999999)
    message = 'Your otp is ' + str(otp)
    from_email = settings.EMAIL_HOST_USER

    # Save the OTP along with the timestamp
    user_obj = Voter.objects.get(email=email)
    user_obj.otp = otp
    user_obj.otp_timestamp = timezone.now()
    user_obj.save()

    # Send the email
    send_mail(subject, message, from_email, [email])

def verifyEmailOTP(email, entered_otp):
    try:
        user_obj = Voter.objects.get(email=email)
        stored_otp = user_obj.otp
        otp_timestamp = user_obj.otp_timestamp

        # Check if OTP_timestamp is not None before performing timedelta
        if otp_timestamp:
            valid_timeframe = otp_timestamp + timedelta(minutes=5)
            current_time = timezone.now()

            if current_time <= valid_timeframe and entered_otp == stored_otp:
                # OTP is valid
                return True

        # OTP has expired or is incorrect
        return False

    except Voter.DoesNotExist:
        # Handle the case where the user with the given email does not exist
        return False
