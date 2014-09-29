from django.core.files.storage import default_storage, FileSystemStorage
from django.core.files import File as pFile
from django.db import models
from words.models import Word
import logging
from general.models import Objectbase, Author
from general.tools import *
from files.signals import file_load
import re

log = logging.getLogger(__name__)
fs = FileSystemStorage(location='/media')

class File (Objectbase):
    
    def _total_words(self):
        return self.words.count()

    def _distinct_words(self):
        return self.words.distinct('value').count()
    
    filename = models.CharField(max_length=500, null=False, blank=False)
    title = models.CharField(max_length=500, null=False, blank=False)
    websource = models.URLField(null=True, blank=True)
    publishdate = models.DateField(auto_now=True)
    path = models.FilePathField(blank=True, null=True)
    words = models.ManyToManyField(Word, through='files.FileWord', related_name='files')
    author = models.ForeignKey(Author, null=True, related_name = 'files')
    total_words = property(_total_words)
    distinct_words = property(_distinct_words)
    original = models.FileField(upload_to='textfiles')
    
    def save(self, *args, **kwargs):
        super(File, self).save(*args, **kwargs)
        #f = open(self.original.path, 'r')
        #orgfile = pFile(f)
        #fulltext = orgfile.read()
        file_load.send(sender=None, fileobj=self)
        #self.loadtext(fulltext)
    
    def loadtext(self, fulltext):
        try:
            print_log('Start load text for file: ' + str(self.id))
            lines = fulltext.splitlines()
            c_lines = 1
            c_words = 1
            c_sentence = 1
            for line in lines:
                wordset = line.split()
                filewords = []
                for word_value in wordset:
                    new_word = FileWord()
                    new_word.lineno = c_lines
                    new_word.file = self
                    new_word.wordno = c_words
                    new_word.sentenceno = c_sentence
                    new_word.word = Word.get_word(re.sub('[^A-Za-z0-9]+', '', word_value))
                    #new_word.save()
                    filewords.append(new_word)
                    #new_word.save(word_value=re.sub('[^A-Za-z0-9]+', '', word_value))
                    if Word.is_end_of_sentence(word_value): c_sentence += 1
                    c_words += 1
                FileWord.objects.bulk_create(filewords)
                c_lines += 1
            print_log('End load text for file: ' + str(self.id))
                
        except Exception as e:
            print e
    
class FileWord (models.Model):
    file = models.ForeignKey(File)
    word = models.ForeignKey(Word)
    appears = models.IntegerField(default=0)
    wordno = models.IntegerField(default=0)
    lineno = models.IntegerField(default=0)
    pageno = models.IntegerField(default=0)
    sentenceno = models.IntegerField(default=0)
    paragraphno = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        try:
            if not self.pk:
                try:
                    word_value = kwargs.pop('word_value', None)
                    if word_value:
                        self.word = Word.get_word(word_value)
                except:
                    pass
        except Exception as e:
            log.error(e.message)
            
        super(FileWord, self).save(*args, **kwargs)
        
def load_file_to_db(sender, **kwargs):
    fileobj = kwargs['fileobj']
    f = open(fileobj.original.path, 'r')
    orgfile = pFile(f)
    fulltext = orgfile.read()
    fileobj.loadtext(fulltext)
# Catches new file to load
file_load.connect(load_file_to_db)