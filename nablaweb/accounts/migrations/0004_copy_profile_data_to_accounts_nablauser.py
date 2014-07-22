# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for u in orm['accounts.NablaUser'].objects.all():
            try:
                print("migrating {}".format(u))
                p = orm['accounts.UserProfile'].objects.get(user=u)
                u.telephone = p.telephone
                u.cell_phone = p.cell_phone
                u.birthday = p.birthday
                u.address = p.address
                u.mail_number = p.mail_number
                u.web_page = p.web_page
                u.wants_email = p.wants_email
                u.avatar = p.avatar
                u.ntnu_card_number = p.ntnu_card_number
                u.save()
            except:
                pass

    def backwards(self, orm):
        "Write your backwards methods here."
        for u in orm['accounts.NablaUser'].objects.all():
            p, created = orm['accounts.UserProfile'].objects.get_or_create(user=u)
            p.telephone = u.telephone
            p.cell_phone = u.cell_phone
            p.birthday = u.birthday
            p.address = u.address
            p.mail_number = u.mail_number
            p.web_page = u.web_page
            p.wants_email = u.wants_email
            p.avatar = u.avatar
            p.ntnu_card_number = u.ntnu_card_number
            p.save()

    models = {
        u'accounts.fysmatclass': {
            'Meta': {'object_name': 'FysmatClass', '_ormbases': [u'accounts.NablaGroup']},
            u'nablagroup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.NablaGroup']", 'unique': 'True', 'primary_key': 'True'}),
            'starting_year': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'})
        },
        u'accounts.groupleader': {
            'Meta': {'object_name': 'GroupLeader', '_ormbases': [u'accounts.NablaGroup']},
            'leads': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'leader'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['accounts.NablaGroup']"})
        },
        u'accounts.nablagroup': {
            'Meta': {'object_name': 'NablaGroup', '_ormbases': [u'auth.Group']},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'group_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.Group']", 'unique': 'True', 'primary_key': 'True'}),
            'group_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'mail_list': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'})
        },
        u'accounts.nablauser': {
            'Meta': {'object_name': 'NablaUser'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cell_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'mail_number': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'ntnu_card_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'wants_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web_page': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        },
        u'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cell_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_number': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'ntnu_card_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.NablaUser']", 'unique': 'True'}),
            'wants_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web_page': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']
    symmetrical = True
