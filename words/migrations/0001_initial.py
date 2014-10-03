# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Word'
        db.create_table(u'words_word', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createtime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastupdatetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('createby', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='word_createby', null=True, to=orm['auth.User'])),
            ('lastupdateby', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='word_lastupdateby', null=True, to=orm['auth.User'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
        ))
        db.send_create_signal(u'words', ['Word'])

        # Adding model 'WordGroup'
        db.create_table(u'words_wordgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createtime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastupdatetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('createby', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='wordgroup_createby', null=True, to=orm['auth.User'])),
            ('lastupdateby', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='wordgroup_lastupdateby', null=True, to=orm['auth.User'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'words', ['WordGroup'])

        # Adding M2M table for field words on 'WordGroup'
        m2m_table_name = db.shorten_name(u'words_wordgroup_words')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wordgroup', models.ForeignKey(orm[u'words.wordgroup'], null=False)),
            ('word', models.ForeignKey(orm[u'words.word'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wordgroup_id', 'word_id'])


    def backwards(self, orm):
        # Deleting model 'Word'
        db.delete_table(u'words_word')

        # Deleting model 'WordGroup'
        db.delete_table(u'words_wordgroup')

        # Removing M2M table for field words on 'WordGroup'
        db.delete_table(db.shorten_name(u'words_wordgroup_words'))


    models = {
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
        },
        u'words.word': {
            'Meta': {'object_name': 'Word'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'createby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'word_createby'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'createtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastupdateby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'word_lastupdateby'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'lastupdatetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'})
        },
        u'words.wordgroup': {
            'Meta': {'object_name': 'WordGroup'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'createby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'wordgroup_createby'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'createtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastupdateby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'wordgroup_lastupdateby'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'lastupdatetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'words': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'to': u"orm['words.Word']"})
        }
    }

    complete_apps = ['words']