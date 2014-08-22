# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('auth_user', 'accounts_nablauser')
        db.rename_table('auth_user_groups', 'accounts_nablauser_groups')
        db.rename_table('auth_user_user_permissions','accounts_nablauser_user_permissions')
        db.rename_column('accounts_nablauser_groups', 'user_id', 'nablauser_id')
        db.rename_column('accounts_nablauser_user_permissions', 'user_id', 'nablauser_id')
        if not db.dry_run:
         # For permissions to work properly after migrating
            orm['contenttypes.contenttype'].objects.filter(app_label='auth',
            model='user').update(app_label='accounts', model='nablauser')

    def backwards(self, orm):
        db.rename_column('accounts_nablauser_groups', 'nablauser_id', 'user_id')
        db.rename_column('accounts_nablauser_user_permissions', 'nablauser_id', 'user_id')
        db.rename_table('accounts_nablauser', 'auth_user')
        db.rename_table('accounts_nablauser_groups', 'auth_user_groups')
        db.rename_table('accounts_nablauser_user_permissions', 'auth_user_user_permissions')
        if not db.dry_run:
         # For permissions to work properly after migrating
            orm['contenttypes.contenttype'].objects.filter(app_label='accounts',
            model='nablauser').update(app_label='auth', model='user')

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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
