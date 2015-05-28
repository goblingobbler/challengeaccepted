from django.conf.urls import patterns, url

from user import views

urlpatterns = patterns('',
    url(r'^register$', views.Register, name='register'),
    url(r'^login$', views.Login, name='login'),
    
    url(r'^profile/([0-9]+)$', views.Profile, name='profile'),
    
    url(r'^editaffiliate/([0-9]+)/$', views.EditAffiliate, name='editaffiliate'),
    
    url(r'^forgotpassword$', views.ForgotPassword, name='forgotpassword'),
    url(r'^passwordrecovery$', views.PasswordRecovery, name='passwordrecovery'),
    
    
    url(r'^adminapprove/([0-9]+)$', views.AdminApprove, name='adminapprove'),
    
    url(r'^unapproved$', views.unapproved, name='unapproved'),
    url(r'^logout$', views.Logout, name='logout'),
    
)

