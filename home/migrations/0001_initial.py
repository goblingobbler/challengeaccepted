# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Address'
        db.create_table(u'search_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'search', ['Address'])

        # Adding model 'ScoreType'
        db.create_table(u'search_scoretype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'search', ['ScoreType'])

        # Adding model 'AddressScore'
        db.create_table(u'search_addressscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Address'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.ScoreType'])),
            ('score', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'search', ['AddressScore'])


    def backwards(self, orm):
        # Deleting model 'Address'
        db.delete_table(u'search_address')

        # Deleting model 'ScoreType'
        db.delete_table(u'search_scoretype')

        # Deleting model 'AddressScore'
        db.delete_table(u'search_addressscore')


    models = {
        u'search.address': {
            'Meta': {'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'search.addressscore': {
            'Meta': {'object_name': 'AddressScore'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Address']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.ScoreType']"})
        },
        u'search.scoretype': {
            'Meta': {'ordering': "['-order']", 'object_name': 'ScoreType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['search']