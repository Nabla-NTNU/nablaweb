# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'YearChoices'
        db.create_table('jobs_yearchoices', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('jobs', ['YearChoices'])

        # Adding model 'RelevantForChoices'
        db.create_table('jobs_relevantforchoices', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('studieretning', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('jobs', ['RelevantForChoices'])

        # Adding model 'TagChoices'
        db.create_table('jobs_tagchoices', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('jobs', ['TagChoices'])

        # Adding model 'Company'
        db.create_table('jobs_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='company_created', null=True, to=orm['auth.User'])),
            ('last_changed_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('last_changed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='company_edited', null=True, to=orm['auth.User'])),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('cropping', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('jobs', ['Company'])

        # Adding model 'Advert'
        db.create_table('jobs_advert', (
            ('news_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['news.News'], unique=True, primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobs.Company'])),
            ('deadline_date', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('show_removal_date', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('removal_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('info_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('antall_stillinger', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('contact_info', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('jobs', ['Advert'])

        # Adding M2M table for field relevant_for_group on 'Advert'
        db.create_table('jobs_advert_relevant_for_group', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('advert', models.ForeignKey(orm['jobs.advert'], null=False)),
            ('relevantforchoices', models.ForeignKey(orm['jobs.relevantforchoices'], null=False))
        ))
        db.create_unique('jobs_advert_relevant_for_group', ['advert_id', 'relevantforchoices_id'])

        # Adding M2M table for field relevant_for_year on 'Advert'
        db.create_table('jobs_advert_relevant_for_year', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('advert', models.ForeignKey(orm['jobs.advert'], null=False)),
            ('yearchoices', models.ForeignKey(orm['jobs.yearchoices'], null=False))
        ))
        db.create_unique('jobs_advert_relevant_for_year', ['advert_id', 'yearchoices_id'])

        # Adding M2M table for field tags on 'Advert'
        db.create_table('jobs_advert_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('advert', models.ForeignKey(orm['jobs.advert'], null=False)),
            ('tagchoices', models.ForeignKey(orm['jobs.tagchoices'], null=False))
        ))
        db.create_unique('jobs_advert_tags', ['advert_id', 'tagchoices_id'])


    def backwards(self, orm):
        
        # Deleting model 'YearChoices'
        db.delete_table('jobs_yearchoices')

        # Deleting model 'RelevantForChoices'
        db.delete_table('jobs_relevantforchoices')

        # Deleting model 'TagChoices'
        db.delete_table('jobs_tagchoices')

        # Deleting model 'Company'
        db.delete_table('jobs_company')

        # Deleting model 'Advert'
        db.delete_table('jobs_advert')

        # Removing M2M table for field relevant_for_group on 'Advert'
        db.delete_table('jobs_advert_relevant_for_group')

        # Removing M2M table for field relevant_for_year on 'Advert'
        db.delete_table('jobs_advert_relevant_for_year')

        # Removing M2M table for field tags on 'Advert'
        db.delete_table('jobs_advert_tags')


    models = {
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
        },
        'jobs.advert': {
            'Meta': {'object_name': 'Advert', '_ormbases': ['news.News']},
            'antall_stillinger': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jobs.Company']"}),
            'contact_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'deadline_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'info_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'news_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['news.News']", 'unique': 'True', 'primary_key': 'True'}),
            'relevant_for_group': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['jobs.RelevantForChoices']", 'symmetrical': 'False'}),
            'relevant_for_year': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['jobs.YearChoices']", 'null': 'True', 'symmetrical': 'False'}),
            'removal_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'show_removal_date': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['jobs.TagChoices']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'jobs.company': {
            'Meta': {'object_name': 'Company'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'company_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'cropping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'company_edited'", 'null': 'True', 'to': "orm['auth.User']"}),
            'last_changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'jobs.relevantforchoices': {
            'Meta': {'object_name': 'RelevantForChoices'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'studieretning': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'jobs.tagchoices': {
            'Meta': {'object_name': 'TagChoices'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'jobs.yearchoices': {
            'Meta': {'object_name': 'YearChoices'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'news.news': {
            'Meta': {'object_name': 'News'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'news_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'cropping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'news_edited'", 'null': 'True', 'to': "orm['auth.User']"}),
            'last_changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'lead_paragraph': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['jobs']
