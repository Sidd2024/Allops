from datetime import datetime
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .filters import opportunityFilter
from .forms import *
from .models import *
from django.core.paginator import Paginator
import http.client,json
from django.shortcuts import render
import pyrebase

#TODO: Add SDKs for Firebase products that you want to use
# https://firebase.google.com/docs/web/setup#available-libraries

 #Your web app's Firebase configuration
#For Firebase JS SDK v7.20.0 and later, measurementId is optional
firebaseConfig = {
  'apiKey': "AIzaSyAgzpdxATSFW7mQPn1lUSIQAN7Sq3DWzP0",
  'authDomain': "allops-f9826.firebaseapp.com",
  'projectId': "allops-f9826",
  'databaseURL' : "https://allops-f9826-default-rtdb.asia-southeast1.firebasedatabase.app",
  'storageBucket': "allops-f9826.appspot.com",
  'messagingSenderId': "433849589058",
  'appId': "1:433849589058:web:b969e4f9eda03aae5c3cdb",
  'measurementId': "G-JJBB58ZX6E"
}
firebase=pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
database=firebase.database()


def index(request):
    
    #list and sort the tech domains according to the opportunities available on website
    user = database.child('User').child('name').get().val()
    age = database.child('User').child('age').get().val()
    web = opportunity.objects.filter(interest__icontains = 'Web').count()
    mobile = opportunity.objects.filter(interest__icontains = 'Mobile').count()
    game = opportunity.objects.filter(interest__icontains = 'Gaming').count()
    ml_ai = opportunity.objects.filter(interest__icontains = 'Machine Learning/AI').count()
    cloud = opportunity.objects.filter(interest__icontains = 'Cloud').count()
    devops = opportunity.objects.filter(interest__icontains = 'Devops').count()
    cyber = opportunity.objects.filter(interest__icontains = 'Cybersecurity').count()
    ar_vr = opportunity.objects.filter(interest__icontains = 'AR/VR').count()
    block = opportunity.objects.filter(interest__icontains = 'Blockchain').count()
    dict1 = {('Web',web),('Mobile',mobile),('blockchain',block),('Gaming',game),('Machine Learning/AI',ml_ai),('Cloud',cloud),('Devops',devops),('Cybersecurtiy',cyber),('AR/VR',ar_vr)}
    dict = sorted(dict1, reverse=True,key=lambda x:x[1])

    #get featured opportunities
    featured = opportunity.objects.filter(featured = True).order_by('-time')
    return render(request, "Allops/index.html",{
        "dict": dict,
        "items": featured,
        "user": user,
        "age": age
    })


def signin(request):
    
    #user submits the form to signin:
    if request.method == 'POST':
        form = signin_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            #if form is valid and user is authenticated then login user else throw the possible error.
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, "Allops/signin.html", {
                    "form": form,
                    "error": "Invalid username or password!"
                })
    #user requests the form to signin.
    else:
        form = signin_form()
        return render(request, "Allops/signin.html", {
            "form": form
        })


def signup(request):
    
    #user submits the form to signup:
    if request.method == 'POST':
        form = signup_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_pass = form.cleaned_data['confirm_pass']
            if password != confirm_pass:
                return render(request, "Allops/signup.html", {
                    "form": form,
                    "error": "Passwords didn't match!"
                })
            #if information is valid then create user else catch the error and send alert.
            try:
                user = User.objects.create_user(username, email, password)
                user.save
            except IntegrityError:
                return render(request, "Allops/signup.html", {
                    "form": form,
                    "error": "Username already taken!"
                })
            #If no error occured then login user.
            login(request, user)
            return redirect('index')
    #if user requests the signup form.
    else:
        form = signup_form()
        return render(request, "Allops/signup.html", {
            "form": form
        })


def signout(request):
    #signout current user:
    logout(request)
    return redirect('index')

#get opportunities according to the type requested by user.
def get_opportunities(request,type):
    items = opportunity.objects.filter(type=type).order_by('-time')

    #if filters applied then apply filters and update the opportunities accordingly:
    filter = opportunityFilter(request.GET, queryset=items)
    items = filter.qs
    total_items = items.count

    #Apply pagination to opportunities:
    item_paginator = Paginator(items, 9)
    page_num = request.GET.get('page')
    page = item_paginator.get_page(page_num)
    user = request.user

    #if user is logged in then get saved opportunities by that user.
    if user.is_authenticated:
        saves = save.objects.filter(user=request.user)
        return render(request, "Allops/opportunities.html", {
            "items": page,
            "saves": saves,
            "filter": filter,
            "type": type,
            "total_items": total_items
        })
    else:
        return render(request, "Allops/opportunities.html", {
            "items": page,
            "filter": filter,
            "type": type,
            "total_items": total_items

        })

#get a specific opportunity requested by user.
def activity(request, item_id):
    item = opportunity.objects.get(id = item_id)
    user = request.user
    
    #if user is logged in then check if this opportunity is saved by user:
    if user.is_authenticated:
        saved = save.objects.filter(user = user, activity = item).first()
        return render(request, "Allops/opportunity.html",{
            "item": item,
            "saved": saved
        })
    else:
        return render(request, "Allops/opportunity.html",{
            "item": item
        })

@login_required
@csrf_exempt
def save_it(request, item_id):
    #User toggles save button:
    try:
        user = request.user
        post = opportunity.objects.get(id = item_id)

        saved = save.objects.filter(user = user, activity = post).first()

        #if opportunity is not listed in saved then add it else remove it:
        if saved is None:
            saveit = save.objects.create(user = user, activity = post)
            saveit.save()
            css="fas fa-bookmark"
        else:
            saved.delete()
            css="far fa-bookmark fa-inverse"
    except:

        #throw error if something goes wrong.
        return HttpResponseBadRequest("somethins went wrong!")
    
    #change css of save button accordingly by passing it to the javascript.
    return JsonResponse({
        "css": css
    })

@login_required
def saved(request):
    user = request.user

    #get all opportunities saved by logged in user:
    saves = save.objects.filter(user = user)
    if saves is not None:
        return render(request, "Allops/saved.html",{
            "saves": saves,
        })
    #if saved list is empty then render this message.
    else:
        return render(request, "Allops/saved.html",{
            "msg": "Such empty! 0_0..."
        })

@login_required
def share(request):

    #if user submits the share form:
    if request.method == 'POST':
        form = share_form(request.POST)
        if form.is_valid():
            head = form.cleaned_data['head']
            desc = form.cleaned_data['desc']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            location = form.cleaned_data['location']
            details = form.cleaned_data['details']
            image = form.cleaned_data['image']
            link = form.cleaned_data['link']
            type = form.cleaned_data['type']
            interest = form.cleaned_data['interest']
            time = datetime.now
            user = request.user

            #if form is valid then create the corresponding opportunity for that.
            try:
                opportunity.objects.create(
                    head = head, desc = desc, start = start, end = end, location = location, details = details,
                    image = image, link = link, type = type, interest = interest, time = time, user = user
                )
            
            #throw error if something goes wrong.
            except:
                return render(request, "Allops/share.html",{
                    "error": "Something went wrong, we migth alredy have this listed!"
                })

            #get the users whose any single interest matches with the newly added opportunity's interest tags and add these users to the recepients list:
            users = mails()
            recep_list = []
            for tag in interest:
                users = mails.objects.filter(fields__icontains = tag)
            for user in users:
                recep_list.append(user.mail_id)

            #prepare the mail template:
            template = render_to_string('Allops/mail_template.html',{
                "head": head,
                "link": link,
                "interest": interest
            })


            #Send mail to all the recepients in the list:
            email = EmailMessage(
                'Opportunity for you on Allops',
                template,
                settings.EMAIL_HOST_USER,
                recep_list
            )
            email.fail_silently = False
            email.send()
            
            #render success message to the user.
            form = share_form()
            return render(request, "Allops/share.html",{
                "success": "Successfully added!, thank you for your time and effort.",
                "form": form
            })
    
    #if user requests the share form:
    else:
        form = share_form()
        return render(request, "Allops/share.html",{
            "form": form
        })

@login_required
def profile(request):

    #get the user and all the opportunitites shared by that user.
    user = request.user
    items = opportunity.objects.filter(user = user).order_by('-time')

    #apply filters if requested and update the opportunities list accordingly.
    filter = opportunityFilter(request.GET, queryset=items)
    items = filter.qs

    return render(request, "Allops/profile.html",{
        "items": items,
        "filter": filter
    })

@login_required
def activate_mails(request):

    #if user submits mails form:
    if request.method == 'POST':
        form = mails_form(request.POST)
        if form.is_valid():
            fields = form.cleaned_data['fields']
            mail_id = form.cleaned_data['mail_id']
            user = request.user
            unsubscribe = form.cleaned_data['unsubscribe']
            subscribed = mails.objects.filter(user = user,mail_id = mail_id).first()
            
            #Throws error if user mail id not match with given email id:
            if mail_id != user.email:
                return render(request, 'Allops/mails.html',{
                    "error": "Invalid email id!",
                    "form": form
                })

            #Delete mails model for user if he/she chooses to unsubscribe:
            if unsubscribe == True:
                try:
                    mails.objects.get(user = user, mail_id = mail_id).delete()
                    form = mails_form()
                    return render(request, "Allops/mails.html",{
                        "success": "Unsubscribed to mail notifications!",
                        "form": form
                    })
                except:
                    form = mails_form()
                    return render(request, "Allops/mails.html",{
                        "error": "Invalid email id, you must have subscribed with some other email id!",
                        "form": form
                    })

            #update mail interest fields of user if already subscribed to mail notfications:
            if subscribed is not None:
                mails.objects.update(user = user, mail_id = mail_id, fields = fields)

                form = mails_form()
                return render(request, "Allops/mails.html",{
                    "success": "Successfully updated the mail cofiguration!",
                    "form": form
                })
            
            #else activate mail notfications for the user according to the given information:
            else:
                try:
                    mail_user = mails.objects.create(user = user, mail_id = mail_id, fields = fields)
                    mail_user.save()
                    form = mails_form()
                    return render(request, "Allops/mails.html",{
                        "success": "Successfully subscribed to mails",
                        "form": form
                    })
                except:
                    return render(request, "Allops/mails.html",{
                        "error": "Something went wrong!, try later."
                    })
        #if form is not valid:
        else:
            form = mails_form()
            return render(request, "Allops/mails.html",{
                "error": "Entries are not valid",
                "form": form
            })
    #if user requests mail form:
    else:
        form = mails_form()
        user = request.user
        subscribed = mails.objects.filter(user = user)
        return render(request, "Allops/mails.html",{
            "form": form,
            "user": user,
            "subscribed": subscribed
        })
    
@login_required
def validate_mail(request):
    
    if request.method == 'POST':
        form = validate_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['mail_id']
            conn = http.client.HTTPSConnection("api.apyhub.com")
            payload = "{\"email\":\""+email+"\"}"
            headers = {
            'apy-token': "APY0UD0xUOw2Ke2oSetASpZ8UFU3b6AQsAFhJ6X5yk7RFaP4l16WcKRVc4TeMFT9MkkVRKHUJL1FUR",
            'Content-Type': "application/json"
            }

            conn.request("POST", "/validate/email/academic", payload, headers)

            res = conn.getresponse()
            data = res.read()

            flag = data.decode("utf-8")
            valid = json.loads(flag)
            

            if valid['data']:
                return render(request, "Allops/validate.html",{
                    "form": form,
                    "success": "Great!, Academic Email is Valid!"
                })
            else:
                return render(request, "Allops/validate.html",{
                    "form": form,
                    "error": "Invalid Academic Email!"
                })
        else:
            return render(request, "Allops/validate.html",{
                "form": form,
                "error": "Something went wrong!"
            })
    else:
        form = validate_form(request.GET)
        return render(request, "Allops/validate.html",{
            "form": form
        })
