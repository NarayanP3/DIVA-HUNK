from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django import forms
from .email import sendEmailOTP
from .models import Voter
from .forms import VoterRegisterForm

def home(request) :
    return render(request, 'core/home.html')

def register(request):
    print("Inside register view");
    context = {
        # 'type': "Hunk",
        # 'candidate': candidate,
        'form': {},
        'message': "",
        'disabled':False,
        'name':'',
        'contactno':'',
        'email':'',
    }
    if (request.method == 'POST'):
        form = VoterRegisterForm(request.POST)
        if not form.is_valid():
            context.update(form=form, message='Form is invalid')
            return render(request, 'core/register.html', context)
        
        context.update(form=form)
        
        if 'sendOTP' in request.POST:
            email = request.POST.get('email_ID', '')
            if not email:
                context.update(message='Email is required')  # Add an error message to the context
                return render(request, 'core/register.html', context)

            voter = form.save(commit=False)
            find = Voter.objects.filter(email=voter.email)
            # if (find.count() >= 1):
            #     context.update(message='Only one vote from one email')
            
            #     return render(request, 'core/home.html', context)
            # else:
            #     print("Saving voter")
            #     voter.save()

            sendEmailOTP(email)  # Use the extracted 'email' variable here
            context.update(message='OTP sent successfully')
            context.update(disabled='True')
            context.update(name=request.POST.get('name', ''))
            context.update(contactno=request.POST.get('contactno', ''))
            context.update(email=email)  # Use the extracted 'email' variable here
            # print("Sending email:")
            # print("From: hrishikeshannamboodiri99@gmail.com")
            # print(f"To: {email}")  # Use the extracted 'email' variable here


            return render(request, 'core/register.html', context)

        if 'verify' in request.POST:
            email = request.POST[email]
            otp_1 = request.POST.get('otp_1', '')
            otp_2 = request.POST.get('otp_2', '')
            otp_3 = request.POST.get('otp_3', '')
            otp_4 = request.POST.get('otp_4', '')
            otp_5 = request.POST.get('otp_5', '')
            otp_6 = request.POST.get('otp_6', '')
            otp =  request.POST[otp_1]+request.POST[otp_2]+request.POST[otp_3]+request.POST[otp_4]+request.POST[otp_5]+request.POST[otp_6]
            
            find = Voter.objects.filter(email=email)
            if not find.exists():
                context.update(message='Email does not match')
                return render(request, 'core/home.html', context)

            if find[0].otp != otp:
                context.update(message='wrong otp')
                return render(request, 'core/home.html', context)
            
            # candidate.votes+=1
            # candidate.save()
            # find.update(hunk=candidate)
        return redirect('register')
    else:
        form = VoterRegisterForm()
    context.update(form=form)
    return render(request, 'core/register.html')

# Create your views here.
