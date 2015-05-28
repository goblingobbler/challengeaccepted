from django.db import models

from django_extensions.db.fields import ModificationDateTimeField, CreationDateTimeField
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from jsonfield import JSONField

import secretballot

class Challenge(models.Model):
    title = models.CharField(_('Title'), max_length=300, help_text=_('Title'))
    desc = models.TextField(_('Description'), help_text=_('Description'))

    def __unicode__( self ):
        return self.title

class Comments(models.Model):
    challenge = models.ForeignKey(Challenge)
    
    parent = models.ForeignKey('self', blank = True, null = True)
    
    valid_video = models.BooleanField(default = False)
    
    link = models.CharField(_('Video Link'), max_length=300, help_text=_('Video link'))
    desc = models.TextField(_('Description'), help_text=_('Description'))

    def __unicode__( self ):
        return str(self.challenge) + ' ' + self.desc

secretballot.enable_voting_on(Challenge)
secretballot.enable_voting_on(Comments)


'''
class Address(models.Model):
    address = models.CharField(_('Address'), max_length=300, help_text=_('Address'))
    city = models.CharField(_('City'), max_length=100, help_text=_('City'))
    
    completed = models.BooleanField(default = False)
    
    lat = models.FloatField(_('Latitude'), help_text=_('Latitude'))
    lng = models.FloatField(_('Longitude'), help_text=_('Longitude'))
    
    score_title = models.CharField(_('Score Title'), max_length=300, help_text=_('Score Title'))
    score_desc = models.CharField(_('Score Description'), max_length=300, help_text=_('Score Description'))
    
    updated = ModificationDateTimeField()
    
    def scores(self):
        score = {}
        for row in self.addressscore_set.all():
            score[row.type.title] = row
        
        metrics = {
           'QUALITY': score['rating'],
           'PRICE VARIETY': score['price'],
           'CUISINE VARIETY': score['variety'],
           'PROXIMITY': score['distance']}
        
        return metrics
    
    def finalscore(self):
        return self.addressscore_set.filter(type__title = 'final').first().weighted()
    
    def __unicode__( self ):
        return self.address + ', ' + self.city

class ScoreType(models.Model):
    title = models.CharField(_('Title'), max_length=100, help_text=_('Title'))
    order = models.IntegerField(_('Order'), default = 0)
    
    image = models.CharField(_('Image'), max_length=100, help_text=_('Image'))
    
    color = models.CharField(_('Color'), max_length=100, help_text=_('Color'))
    
    class Meta:
        ordering = ['-order']
    def __unicode__( self ):
        return self.title


class AddressScore(models.Model):
    address = models.ForeignKey(Address)
    type = models.ForeignKey(ScoreType)
    
    weight = models.FloatField(_('Weight'), help_text=_('Weight'))
    score = models.FloatField(_('Score'), help_text=_('Score'))
    
    def weighted(self):
        return str(self.score * self.weight * 100).split('.')[0]
    
    def __unicode__( self ):
        return str(self.address) + ' ' + str(self.type) + ' ' + str(self.weight) + ' ' + str(self.score)
    

class ScoreGroup(models.Model):
    title = models.CharField(_('Title'), max_length=100, help_text=_('Title'))
    description = models.TextField('Description', blank = True)
    
    max_score = models.IntegerField(_('Max Score'), default = 0)
    
    class Meta:
        ordering = ['-max_score']
        
    def __unicode__( self ):
        return self.title + ' ' + str(self.max_score)



class Restaurant(models.Model):
    owner = models.ForeignKey(Address)
    google_id = models.CharField(_('google_id'), max_length=300, help_text=_('google_id'))
    
    data = JSONField(null=True, blank=True, default={})
    
    title = models.CharField(_('Title'), max_length=300, help_text=_('Title'))
    lat = models.FloatField(_('Latitude'), help_text=_('Latitude'))
    lng = models.FloatField(_('Longitude'), help_text=_('Longitude'))
    
    address = models.CharField(_('Address'), max_length=300, help_text=_('Address'))
    
    def weighted(self):
        return self.score * self.weight
    
    def __unicode__( self ):
        return str(self.title) + ' ' + str(self.address)
   


'''