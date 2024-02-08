from django.shortcuts import render, redirect
from .models import Diva, Hunk, Voter
from .forms import VoterRegisterForm
from .email import sendEmailOTP, verifyEmailOTP
from itertools import chain
from django.http import HttpResponse
from datetime import datetime, timedelta
import os

# Create your views here.

# def testaccess(request):
#     # name = os.path.basename('base/test.txt')
#     # with open('base/test.txt') as f:
#     #     s = f.read()
#     f = open('base/test.txt', 'w')
#     f.write('This is a written file')
#     f.close()
#     f = open('base/test.txt', 'r')
#     name = f. read()
#     print(name)
#     f. close()

#     return render(request, 'base/testaccess.html', {'name':name})


def home(request):
    divas = Diva.objects.all()
    hunks = Hunk.objects.all()
    context = {
        'divas': divas,
        'hunks': hunks
    }
    
    return render(request, 'base/header.html', context)

# def register(request):
#     return render(request, 'base/register.html')

# def divaHunkList(request):
#     context = {
#         'diva': [],
#         'hunk': [],
#         'message': "",
#         'isdiva':False,
#     }
#     # We need need to get form data to render the context
#     searchquery = request.GET.get('search')
#     if searchquery!=None and searchquery!="":
#         searchDiva=Diva.objects.filter(name__icontains=searchquery)
#         searchHunk=Hunk.objects.filter(name__icontains=searchquery)
#         if searchDiva:
#             context.update(diva=searchDiva)
#         elif searchHunk:
#             context.update(hunk=searchHunk)
#         else:
#             context.update(message="No match found")
#             return render(request, 'base/list.html',context)
#     else:
        
#         if("Hunk" in request.GET):
#             results=Hunk.objects.all()
#             context.update(hunk=results)
#         else :
#             results=Diva.objects.all() 
#             context.update(diva=results)
#             context.update(isdiva=True)
    
#     return render(request, 'base/list.html',context)


def divaRegistration(request, pk):
    candidate = Diva.objects.get(pk=pk)
    context = {
        'type': "Diva",
        'candidate': candidate,
        'form': {},
        'message': "",
        'disabled':False,
        'name':'',
        'contact':'',
        'email':'',
    }
    if (request.method == 'POST'):
        form = VoterRegisterForm(request.POST)
        if not form.is_valid():
            context.update(form=form,message='form is invalid')
            return render(request, 'base/register.html', context)
        context.update(form=form)
        # voter = form.save(commit=False)
        
        if 'sendOTP' in request.POST:
            voter = form.save(commit=False)
            find = Voter.objects.filter(email=voter.email)
            if (find.count() >= 1):
                if (find[0].diva):
                    context.update(message='Only one vote from one email')
                    return render(request, 'base/register.html', context)
            else:
                voter.save()
            sendEmailOTP(voter.email)
            context.update(message='OTP sent successfully')
            context.update(disabled='True')
            context.update(name=request.POST['name'])
            context.update(contact=request.POST['contact'])
            context.update(email=request.POST['email'])
            Voter.objects.update(diva=candidate)
            return render(request, 'base/register.html', context)

        if 'verify' in request.POST:
            email = request.POST['email']
            otp =  request.POST['otp_1']+request.POST['otp_2']+request.POST['otp_3']+request.POST['otp_4']+request.POST['otp_5']+request.POST['otp_6']

            find = Voter.objects.filter(email=email)
            if not find.exists():
                context.update(message='Email does not match')
                return render(request, 'base/register.html', context)
            
            if not verifyEmailOTP(email, otp):
                context.update(message='otp expired')
                context.update(disabled='True')
                context.update(name='')
                context.update(contact='')
                context.update(email='')
                return render(request, 'base/register.html', context)

            if find[0].otp != otp:
                context.update(message='wrong otp')
                context.update(disabled='True')
                context.update(name=request.POST['name'])
                context.update(contact=request.POST['contact'])
                context.update(email=request.POST['email'])
                return render(request, 'base/register.html', context)
            
            candidate.votes=candidate.votes+1
            candidate.save()
            find.update(diva=candidate)
        return redirect('home')
    else:
        form = VoterRegisterForm()
    context.update(form=form)
    context.update(message = 'registered successfully')
    return render(request, 'base/register.html', context)


def hunkRegistration(request, pk):
    candidate = Hunk.objects.get(pk=pk)
    context = {
        'type': "Hunk",
        'candidate': candidate,
        'form': {},
        'message': "",
        'disabled':False,
        'name':'',
        'contact':'',
        'email':'',
    }
    if (request.method == 'POST'):
        form = VoterRegisterForm(request.POST)
        if not form.is_valid():
            context.update(form=form,message='form is invalid')
            return render(request, 'base/register.html', context)
        context.update(form=form)
        if 'sendOTP' in request.POST:
            voter = form.save(commit=False)
            find = Voter.objects.filter(email=voter.email)
            if (find.count() >= 1):
                if (find[0].hunk):
                    context.update(message='Only one vote from one email')
                    return render(request, 'base/register.html', context)
            else:
                voter.save()
            sendEmailOTP(voter.email)
            context.update(message='OTP sent successfully')
            context.update(disabled='True')
            context.update(name=request.POST['name'])
            context.update(contact=request.POST['contact'])
            context.update(email=request.POST['email'])
            Voter.objects.update(hunk=candidate)
            return render(request, 'base/register.html', context)

        if 'verify' in request.POST:
            email = request.POST['email']
            otp =  request.POST['otp_1']+request.POST['otp_2']+request.POST['otp_3']+request.POST['otp_4']+request.POST['otp_5']+request.POST['otp_6']
            
            find = Voter.objects.filter(email=email)
            if not find.exists():
                context.update(message='Email dose not match')
                return render(request, 'base/register.html', context)
            
            if not verifyEmailOTP(email, otp):
                context.update(message='otp expired')
                context.update(disabled='True')
                context.update(name='')
                context.update(contact='')
                context.update(email='')
                return render(request, 'base/register.html', context)

            if find[0].otp != otp:
                context.update(message='wrong otp')
                # context.update(message='OTP sent successfully')
                context.update(disabled='True')
                context.update(name=request.POST['name'])
                context.update(contact=request.POST['contact'])
                context.update(email=request.POST['email'])
                return render(request, 'base/register.html', context)
            
            candidate.votes+=1
            candidate.save()
            find.update(hunk=candidate)
        return redirect('home')
    else:
        form = VoterRegisterForm()
    context.update(form=form)
    return render(request, 'base/register.html', context)

def voting_list(request):
    diva_participants = Diva.objects.order_by('-votes')  # Assuming Diva model has a 'votes' field
    hunk_participants = Hunk.objects.order_by('-votes')  # Assuming Hunk model has a 'votes' field
    
    return render(request, 'base/votinglist.html', {'diva_participants': diva_participants, 'hunk_participants': hunk_participants})

# def thanksdiva(request):
#     return render(request, 'base/thanks_diva.html')

# def thankshunk(request):
#     return render(request, 'base/thanks_hunk.html')
