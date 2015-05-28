from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.template.loader import get_template

from django.core.mail import EmailMessage
from urlparse import urlparse 
import urllib2 
import requests
import facebook

import json
import re
import random
import string

from models import *
from home.models import StaticPlaceholder

from django.core.mail import EmailMessage

def my_login_required(function):
    def wrapper(request, *args, **kw):
        user=request.user
        if not (request.user and request.user.is_authenticated()):
            return HttpResponseRedirect(settings.LOGIN_URL + '?redirect=' + request.get_full_path())
        else:
            if not request.user.approved:
                return HttpResponseRedirect(reverse('user:unapproved'))
            
            return function(request, *args, **kw)
    return wrapper

def Register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        type = int(request.POST['type'])
        title = request.POST['title']
        
        if not User.objects.filter(email = email):
            user = User.objects.create_user(email, password, type, title)
            if request.POST['code'] != '':
                parent = User.objects.filter(code = request.POST['code']).first()
                user.parent = parent
                user.save()
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if request.COOKIES.get('redirect') != '':
                    return HttpResponseRedirect(request.COOKIES.get('redirect'))
                else:
                    if user.type > 1:
                        return HttpResponseRedirect(reverse('artistpage', args=(user.linkedinfo().safe_name(),)))
                    else:
                        return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect(reverse('user:register'))
            
        else:
            return HttpResponseRedirect(reverse('user:login') + '?error=This email is in use. Please log in.')
        
    else:
        if 'code' in request.GET:
            code = request.GET['code']
            url = 'https://graph.facebook.com/oauth/access_token?client_id=1562656020613677&redirect_uri='
            url += 'http://nutritionalfactors.com/user/register&client_secret=93c559b962b96215688e9efafd186a4a&code=' + code
            response = requests.request("GET",url)
            
            if 'error' not in response.text:
                token = response.text.split('&')[0].split('=')[1]
                graph = facebook.GraphAPI(token)
                me = graph.get_object('me')
                print me
                print ''
                data = json.loads(requests.request("GET",'https://graph.facebook.com/v2.2/'+ me['id'] + '/picture?redirect=0').text)
                print data
                
                user = User.objects.filter(facebook_id = me['id']).first()
                if not user:
                    email = me['email']
                    facebook_id = me['id']
                    password = me['id']
                    first_name = me.get('first_name','')
                    last_name = me.get('last_name','')
                    picture = data['data']['url']
                    
                    user = User.objects.filter(email = email).first()
                    if user:
                        User.objects.filter(email = email).update(first_name = first_name, last_name = last_name, facebook_id = facebook_id, picture = picture)
                    else:
                        user = User.objects.create_user(email, password, first_name = first_name, last_name = last_name, 
                                facebook_id = facebook_id, picture = picture)
                        user.save()
                
                user.backend='django.contrib.auth.backends.ModelBackend'
                login(request, user)
                if request.COOKIES.get('redirect') != '':
                    return HttpResponseRedirect(request.COOKIES.get('redirect'))
                else:
                    
                    if user.type > 1:
                        return HttpResponseRedirect(reverse('artistpage', args=(user.linkedinfo().safe_name(),)))
                    else:
                        return HttpResponseRedirect(reverse('index'))
        
        else:
            path = request.META['HTTP_HOST']
            
            redirect = ''
            if 'redirect' in request.GET:
                redirect = request.GET['redirect']
            
            message = ''
            if 'success' in request.GET:
                if request.GET['success'] == 'password':
                    message = 'Password reset successfully'
                elif request.GET['success'] == 'email':
                    message = 'Email was sent! Please check your inbox and spam folder'
                    
            error = request.GET.get('error','')
            c = request.GET.get('c','')
            if c != '':
                start = 1
            else:
                start = 0
            
            emails = [x.email for x in User.objects.only('email').all()]
            
            
            response = render(request, 'user/register.html', {'path': path, 'emails': emails, 'code': c,
                                                              'message': message, 'error':error, 'start': start})
            response.set_cookie('redirect',redirect)
            return response


def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        if not User.objects.filter(email = email).first():
            return HttpResponseRedirect(reverse('user:register') + '?error=This email address does not match any in our records, please sign up first')
        
        user = authenticate(email=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.COOKIES.get('redirect') != '':
                    return HttpResponseRedirect(request.COOKIES.get('redirect'))
                else:
                    if user.type > 1:
                        return HttpResponseRedirect(reverse('artistpage', args=(user.linkedinfo().safe_name(),)))
                    else:
                        return HttpResponseRedirect(reverse('index'))
                    # Redirect to a success page.
            else:
                return HttpResponseRedirect(reverse('user:register') + '?error=This account is inactive#login')
                # Return a 'disabled account' error message
        else:
            return HttpResponseRedirect(reverse('user:register') + '?error=Invalid email or password#login')
            # Return an 'invalid login' error message.
        
    else:     
        path = request.META['HTTP_HOST']
        
        redirect = ''
        if 'redirect' in request.GET:
            redirect = request.GET['redirect']
        
        message = ''
        if 'success' in request.GET:
            if request.GET['success'] == 'password':
                message = 'Password reset successfully'
            elif request.GET['success'] == 'email':
                message = 'Email was sent! Please check your inbox and spam folder'
                
        error = request.GET.get('error','')
        
        emails = [x.email for x in User.objects.only('email').all()]
        
        response = render(request, 'user/login.html', {'path': path, 'emails': emails, 
                                                          'message': message, 'error':error,})
        response.set_cookie('redirect',redirect)
        return response

@my_login_required
def AdminApprove(request, id):
    if request.user.is_superuser:
        user = get_object_or_404(User, pk = id)
        user.approved = True
        
        user.save()
        
        email = StaticPlaceholder.objects.filter(name = 'chef_approval_email').first()
        if email:
            user.email_user(email.title, email.desc + '<a href="http://nutritionalfactors.com/recipe/artist/'+str(user.linkedinfo().id)+'">Click here</a>')
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    
def unapproved(request):
    
    return render(request, 'user/unapproved.html', {})
    
    
def Logout(request):
    logout(request)
    
    return HttpResponseRedirect(reverse('index'))


def ForgotPassword(request):
    email = request.POST['email']
    user = get_object_or_404(User, email = email)
    rand_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
    user.verified_string = rand_string
    user.save()

    message = 'You have requested a password reset on Nutritional Factors<br><br>'
    message += '<a href="' + settings.HOST_DOMAIN + '/user/passwordrecovery?verified=' + str(rand_string) + '">Reset Password</a><br><br><br>'
    message += 'The Nutritional Factors Team'
    
    msg = EmailMessage('Password Reset', message, None, [email])
    msg.content_subtype = 'html'  # Main content is now text/html
    msg.send()
    
    return HttpResponseRedirect("%s?success=email" % reverse('user:register'))


def PasswordRecovery(request):
    if request.method == 'POST':
        user = User.objects.filter(id = request.POST['id']).first()
            
        if user:
            password = request.POST['password']
            re = request.POST['repassword']
            
            user.set_password(password)
            user.save()
            
            return HttpResponseRedirect("%s?success=password#login" % reverse('user:register'))
        else:
            return HttpResponseRedirect("%s?invalid=1" % reverse('user:register'))
    else:
        user = get_object_or_404(User, verified_string = request.GET['verified'])
        verified = True
        
        return render(request, 'user/passwordrecovery.html', {'tempuser':user, 'verified':verified})

@my_login_required
def Profile(request,id):
    menu = request.user.menu_planner()
    [days,meals,types] = request.user.menu_items()
    daynums = {'Monday':1,'Tuesday':2,'Wednesday':3,'Thursday':4,'Friday':5,'Saturday':6,'Sunday':7}
    menucounts = request.user.menu_counts()
    
    nutritions = ['kCals','Fat(g)','Pro(g)','CHO(g)']
    nutritioncolors = {'kCals':'purple','Fat(g)':'blue','Pro(g)':'green','CHO(g)':'yellow'}
    return render(request, 'user/profile.html', {'menu':menu,'days':days,'meals':meals,'types':types,'nutritions':nutritions,
                                            'nutritioncolors':nutritioncolors,'menucounts':menucounts, 'daynums':daynums})


def EditAffiliate(request, id):
    if request.method == 'POST':
        a = get_object_or_404(Affiliate, pk = id)
        if request.POST['title'] != '':
            a.title = request.POST['title']
        a.description = request.POST['description']
        a.link = request.POST['link']
            
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            a.image = form.cleaned_data['image']
        
        if 'approval' in request.POST:
            a.saved = True
            for admin in User.objects.filter(is_superuser = True):
                admin.email_user('Nutritional Factors: New Ad Request', 'A partner affiliate has requested an ad.  <a href="http://nutritionalfactors.com/admin/user/affiliate/'+str(request.user.linkedinfo().id)+'/" >Review and approve</a>')
            
        
        a.approved = False
        
        a.save()
        
    a = get_object_or_404(Affiliate, pk = id)
    
    return render(request, 'user/editaffiliate.html', {'artist':a,})


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
    
def uploadPic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.picture = form.cleaned_data['image']
            request.user.save()
    
        return HttpResponseRedirect(reverse('user:profilesettings'))
        
    else:    
        return HttpResponseForbidden('allowed only via POST')
