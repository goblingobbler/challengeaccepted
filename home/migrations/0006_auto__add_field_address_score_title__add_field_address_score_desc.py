# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Address.score_title'
        db.add_column(u'search_address', 'score_title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=300),
                      keep_default=False)

        # Adding field 'Address.score_desc'
        db.add_column(u'search_address', 'score_desc',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=300),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Address.score_title'
        db.delete_column(u'search_address', 'score_title')

        # Deleting field 'Address.score_desc'
        db.delete_column(u'search_address', 'score_desc')


    models = {
        u'search.address': {
            'Meta': {'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'score_desc': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'score_title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'search.addressscore': {
            'Meta': {'object_name': 'AddressScore'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Address']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.ScoreType']"}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        u'search.restaurant': {
            'Meta': {'object_name': 'Restaurant'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'data': ('jsonfield.fields.JSONField', [], {'default': '{}', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Address']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'search.scoregroup': {
            'Meta': {'ordering': "['-max_score']", 'object_name': 'ScoreGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'search.scoretype': {
            'Meta': {'ordering': "['-order']", 'object_name': 'ScoreType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['search']