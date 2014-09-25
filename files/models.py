from django.db import models
from words.models import Word
from general.models import Objectbase

class File (Objectbase):
    filename = models.CharField(max_length=500, null=False, blank=False)
    words = models.ManyToManyField(Word, through='files.FileWord', related_name='files')

class FileWord (models.Model):
    file = models.ForeignKey(File)
    word = models.ForeignKey(Word)
    appears = models.IntegerField(default=0)
    lineno = models.IntegerField(default=0)
    pageno = models.IntegerField(default=0)
    sentenceno = models.IntegerField(default=0)
    paragraphno = models.IntegerField(default=0)
    