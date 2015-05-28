from django.db import models
import datetime
from django.utils import timezone
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from sorl.thumbnail import ImageField

from django_extensions.db.fields import ModificationDateTimeField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.core.mail import EmailMessage

from fractions import Fraction

from django.utils.timesince import timesince
from ckeditor.fields import RichTextField

import random
import string

# Create your models here.

class UserManager(BaseUserManager):
    
    def create_user(self, email, password, type, title, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email address must be set')
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, type=type, name = title, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        if user.type > 1:
            for admin in User.objects.filter(is_superuser = True):
                admin.email_user('Nutritional Factors: New Chef Registration', 'A new user has registered as a chef.  <a href="http://nutritionalfactors.com/admin/user/user/'+str(user.id)+'/" >Review and approve</a>')
            
            if user.type == 2:
                a = Artist(owner = user, title = title)
                a.save()
            elif user.type == 3:
                a = Affiliate(owner = user, title = email)
                a.save()
            
            rand_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
            user.code = rand_string
            
        else:
            user.approved = True
        
        user.save()
        
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

class User(AbstractBaseUser):
    email = models.EmailField(_('email address'), max_length=254, unique=True, db_index=True)
    name = models.CharField(_('Name'), max_length=100, help_text=_('Name'), default = '', blank=True)
    
    is_superuser = models.BooleanField(
        _('admin status'), default=False, help_text=_('Designates whether the user can access the admin panel.'))
    
    is_active = models.BooleanField(
        _('active'), default=False,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting '
                    'accounts.'))
    
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    updated = ModificationDateTimeField()
    @property
    def last_time_logged_in(self):
        return timesince(self.updated)
    
    deleted = models.DateTimeField(_('deleted'), null=True, blank=True)
    
    facebook_id = models.CharField(_('Facebook Id'), max_length=100, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, default='')
    last_name = models.CharField(_('last name'), max_length=30, blank=True, default='')
    
    verified_string = models.CharField(_('Verification String'), max_length=30, blank=True)
    picture = ImageField(_('picture'), upload_to='images/', default='images/default-user.png', max_length=400)
    
    type = models.IntegerField(choices = ((0,'Visitor'),(1,'Member'),
            (2,'Chef'),(3,'Partner'),(4,'Business'),(5,'Dietitian'),), default=0)
    
    approved = models.BooleanField(_('admin approved'), default=False, help_text=_('Admin has verified user'))
    
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, blank = True, null = True)
    code = models.CharField(_('Code to share with customers when signing up'), max_length=40, blank=True)
    
    admin_comments = RichTextField(_('Admin Comments'), help_text=_('Leave any important details here'), default='', blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    # Only email and password is required to create a user account but this is how you'd require other fields.
    REQUIRED_FIELDS = ['password']
    
    @property
    def is_staff(self):
        return self.is_superuser
    
    def get_full_name(self):
        if self.first_name != '':
            return self.first_name + ' ' + self.last_name
        else:
            return self.email

    def get_short_name(self):
        if self.first_name != '':
            return self.first_name
        else:
            return self.email
    
    def __unicode__( self ):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User with content type HTML.
        """
        # It's possible to send multi-part text / HTML email by following these instructions:
        # https://docs.djangoproject.com/en/1.5/topics/email/#sending-alternative-content-types
        msg = EmailMessage(subject, message, from_email, [self.email])
        msg.content_subtype = 'html'  # Main content is now text/html
        msg.send()
        
    def menu_items(self, front = False):
        if front:
            d =  ['Monday']
            m = ['Breakfast']
            t = ['Entree','Side']
        else:
            d =  ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            m = ['Breakfast','Lunch','Dinner','Snack']
            t = ['Entree','Side']
            
        return [d,m,t]
    
    def menu_planner(self, front = False):
        [d,m,t] = self.menu_items(front)
        menu = {}
        for day in d:
            menu[day] = {}
            for meal in m:
                if meal == 'Snack':
                    menu[day][meal] = []
                else:
                    menu[day][meal] = {}
                    
                    for type in t:
                        menu[day][meal][type] = []
        
        if front:
            for item in MenuItem.objects.filter(frontpage = True).all():
                print item.id
                if item.meal == 'Snack':
                    menu[item.day_name()][item.meal].append(item)
                else:
                    menu[item.day_name()][item.meal][item.type].append(item)
        else:
            for item in self.menuitem_set.all():
                print item.id
                if item.meal == 'Snack':
                    menu[item.day_name()][item.meal].append(item)
                else:
                    menu[item.day_name()][item.meal][item.type].append(item)
        
        print menu
        return menu
        
    def daily_values(self):
        menu = self.menu_planner()
        daily_values = {}
        for day in menu:
            daily_values[day] = {}
            daily_values[day]['Total'] = {'kCals':0,'Fat(g)':0,'Pro(g)':0,'CHO(g)':0, 'Fiber':0}
            
            for meal in menu[day]:
                daily_values[day][meal] = {'kCals':0,'Fat(g)':0,'Pro(g)':0,'CHO(g)':0, 'Fiber':0}
                
                for type in menu[day][meal]:
                    for item in menu[day][meal][type]:
                        nutrition = item.recipe.nutrition()
                        
                        if item.recipe.servings != 0 and item.servings != 0:
                            convert = item.servings / item.recipe.servings
                        else:
                            convert = 1
                            
                        daily_values[day][meal]['kCals'] += (float(nutrition.Energ_Kcal) * convert)
                        daily_values[day][meal]['Fat(g)'] += (float(nutrition.Lipid_Tot_g) * convert)
                        daily_values[day][meal]['Pro(g)'] += (float(nutrition.Protein_g) * convert)
                        daily_values[day][meal]['CHO(g)'] += (float(nutrition.Carbohydrt_g) * convert)
                        daily_values[day][meal]['Fiber'] += (float(nutrition.Fiber_TD_g) * convert)
                        
            
                daily_values[day]['Total']['kCals'] += daily_values[day][meal]['kCals']
                daily_values[day]['Total']['Fat(g)'] += daily_values[day][meal]['Fat(g)']
                daily_values[day]['Total']['Pro(g)'] += daily_values[day][meal]['Pro(g)']
                daily_values[day]['Total']['CHO(g)'] += daily_values[day][meal]['CHO(g)']
                daily_values[day]['Total']['Fiber'] += daily_values[day][meal]['Fiber']
        
        return daily_values
    
    def menu_counts(self):
        return ['','Breakfast','Lunch','Dinner','Snack','Total']

    def linkedinfo(self):
        a = self.artist_set.first()
        if not a:
            a = self.affiliate_set.first()
        return a

class Affiliate(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    
    title = models.CharField(_('Title'), max_length=100, help_text=_('Title'))
    class Meta:
        ordering = ['title']
    def __unicode__( self ):
        return self.title
    
    def safe_name(self):
        return self.title.replace(' ','_').lower()
    
    description = models.TextField(_('Description'), help_text=_('Description'), default='')
    def description_safe(self):
        return self.description.replace('<br>','').replace('<br />','')
    
    link = models.TextField(default = '',blank=True)
    
    image = ImageField(
        _('image'), max_length=255, blank=True, upload_to='private-images/', default='private-images/default.jpg',
        help_text=_('Artist Picture'))
    
    saved = models.BooleanField(default=False, help_text=_('This will submit the details to a site admin.'))
    approved = models.BooleanField(default=False, help_text=_('This will show that a site admin had reviewed and published the ad.'))
    
    ad = models.ManyToManyField('factors.FactorAd', blank = True, null = True, 
                                help_text=_('Be sure to approve the affiliate or they will not appear on the page'))
    
    
    
    

