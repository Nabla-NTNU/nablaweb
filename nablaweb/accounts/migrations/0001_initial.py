# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('accounts_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('signature', self.gf('django.db.models.fields.TextField')(max_length=0, blank=True)),
            ('signature_html', self.gf('django.db.models.fields.TextField')(max_length=30, blank=True)),
            ('time_zone', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('language', self.gf('django.db.models.fields.CharField')(default='Norwegian Bokmal', max_length=10, blank=True)),
            ('show_signatures', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('post_count', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('avatar', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('autosubscribe', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('cell_phone', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('mail_number', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('web_page', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('wants_email', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('about', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ntnu_card_number', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal('accounts', ['UserProfile'])

        # Adding model 'NablaGroup'
        db.create_table('accounts_nablagroup', (
            ('group_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.Group'], unique=True, primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('mail_list', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('group_type', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal('accounts', ['NablaGroup'])

        # Adding model 'GroupLeader'
        db.create_table('accounts_groupleader', (
            ('leads', self.gf('django.db.models.fields.related.OneToOneField')(related_name='leader', unique=True, primary_key=True, to=orm['accounts.NablaGroup'])),
        ))
        db.send_create_signal('accounts', ['GroupLeader'])

        # Adding model 'FysmatClass'
        db.create_table('accounts_fysmatclass', (
            ('nablagroup_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.NablaGroup'], unique=True, primary_key=True)),
            ('starting_year', self.gf('django.db.models.fields.CharField')(unique=True, max_length='4')),
        ))
        db.send_create_signal('accounts', ['FysmatClass'])

    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('accounts_userprofile')

        # Deleting model 'NablaGroup'
        db.delete_table('accounts_nablagroup')

        # Deleting model 'GroupLeader'
        db.delete_table('accounts_groupleader')

        # Deleting model 'FysmatClass'
        db.delete_table('accounts_fysmatclass')

    models = {
        'accounts.fysmatclass': {
            'Meta': {'object_name': 'FysmatClass', '_ormbases': ['accounts.NablaGroup']},
            'nablagroup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.NablaGroup']", 'unique': 'True', 'primary_key': 'True'}),
            'starting_year': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'4'"})
        },
        'accounts.groupleader': {
            'Meta': {'object_name': 'GroupLeader', '_ormbases': ['accounts.NablaGroup']},
            'leads': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'leader'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['accounts.NablaGroup']"})
        },
        'accounts.nablagroup': {
            'Meta': {'object_name': 'NablaGroup', '_ormbases': ['auth.Group']},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.Group']", 'unique': 'True', 'primary_key': 'True'}),
            'group_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'mail_list': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'})
        },
        'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'autosubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'avatar': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cell_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'Norwegian Bokmal'", 'max_length': '10', 'blank': 'True'}),
            'mail_number': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'ntnu_card_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'show_signatures': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {'max_length': '0', 'blank': 'True'}),
            'signature_html': ('django.db.models.fields.TextField', [], {'max_length': '30', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'time_zone': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'wants_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web_page': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']