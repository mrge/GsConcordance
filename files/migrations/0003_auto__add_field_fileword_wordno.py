# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FileWord.wordno'
        db.add_column(u'files_fileword', 'wordno',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FileWord.wordno'
        db.delete_column(u'files_fileword', 'wordno')


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
        u'files.file': {
            'Meta': {'object_name': 'File', '_ormbases': [u'general.Objectbase']},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'null': 'True', 'to': u"orm['general.Author']"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'objectbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['general.Objectbase']", 'unique': 'True', 'primary_key': 'True'}),
            'original': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'path': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'words': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'files'", 'symmetrical': 'False', 'through': u"orm['files.FileWord']", 'to': u"orm['words.Word']"})
        },
        u'files.fileword': {
            'Meta': {'object_name': 'FileWord'},
            'appears': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['files.File']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lineno': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pageno': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'paragraphno': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sentenceno': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['words.Word']"}),
            'wordno': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'general.author': {
            'Meta': {'object_name': 'Author', '_ormbases': [u'general.Objectbase']},
            'details': ('django.db.models.fields.TextField', [], {}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'objectbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['general.Objectbase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'general.objectbase': {
            'Meta': {'object_name': 'Objectbase'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'createby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'objectbase_createby'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'createtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastupdateby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'objectbase_lastupdateby'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'lastupdatetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'words.word': {
            'Meta': {'object_name': 'Word', '_ormbases': [u'general.Objectbase']},
            u'objectbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['general.Objectbase']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['files']