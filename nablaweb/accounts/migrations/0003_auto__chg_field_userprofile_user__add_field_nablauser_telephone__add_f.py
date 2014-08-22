# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'UserProfile.user'
        db.alter_column(u'accounts_userprofile', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.NablaUser'], unique=True))
        # Adding field 'NablaUser.telephone'
        db.add_column(u'accounts_nablauser', 'telephone',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True),
                      keep_default=False)

        # Adding field 'NablaUser.cell_phone'
        db.add_column(u'accounts_nablauser', 'cell_phone',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True),
                      keep_default=False)

        # Adding field 'NablaUser.birthday'
        db.add_column(u'accounts_nablauser', 'birthday',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'NablaUser.address'
        db.add_column(u'accounts_nablauser', 'address',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True),
                      keep_default=False)

        # Adding field 'NablaUser.mail_number'
        db.add_column(u'accounts_nablauser', 'mail_number',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=4, blank=True),
                      keep_default=False)

        # Adding field 'NablaUser.web_page'
        db.add_column(u'accounts_nablauser', 'web_page',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=80, blank=True),
                      keep_default=False)

        # Adding field 'NablaUser.wants_email'
        db.add_column(u'accounts_nablauser', 'wants_email',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'NablaUser.about'
        db.add_column(u'accounts_nablauser', 'about',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'NablaUser.avatar'
        db.add_column(u'accounts_nablauser', 'avatar',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'NablaUser.ntnu_card_number'
        db.add_column(u'accounts_nablauser', 'ntnu_card_number',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'UserProfile.user'
        db.alter_column(u'accounts_userprofile', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True))
        # Deleting field 'NablaUser.telephone'
        db.delete_column(u'accounts_nablauser', 'telephone')

        # Deleting field 'NablaUser.cell_phone'
        db.delete_column(u'accounts_nablauser', 'cell_phone')

        # Deleting field 'NablaUser.birthday'
        db.delete_column(u'accounts_nablauser', 'birthday')

        # Deleting field 'NablaUser.address'
        db.delete_column(u'accounts_nablauser', 'address')

        # Deleting field 'NablaUser.mail_number'
        db.delete_column(u'accounts_nablauser', 'mail_number')

        # Deleting field 'NablaUser.web_page'
        db.delete_column(u'accounts_nablauser', 'web_page')

        # Deleting field 'NablaUser.wants_email'
        db.delete_column(u'accounts_nablauser', 'wants_email')

        # Deleting field 'NablaUser.about'
        db.delete_column(u'accounts_nablauser', 'about')

        # Deleting field 'NablaUser.avatar'
        db.delete_column(u'accounts_nablauser', 'avatar')

        # Deleting field 'NablaUser.ntnu_card_number'
        db.delete_column(u'accounts_nablauser', 'ntnu_card_number')


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