from django.core.files.storage import default_storage, FileSystemStorage
from django.core.files import File as pFile
from django.db import models
from words.models import Word
import logging
import MySQLdb

from general.models import Objectbase, Author
from general.tools import print_error,print_log, utfsafe_str
import threading
#from files.signals import file_load
import re

log = logging.getLogger(__name__)
fs = FileSystemStorage(location='/media')

class File (Objectbase):
    
    def _total_words(self):
        return self.words.count()

    def _distinct_words(self):
        return self.words.distinct('value').count()
    
    code = models.CharField(max_length=500, null=False, blank=False)
    title = models.CharField(max_length=500, null=False, blank=False)
    websource = models.URLField(null=True, blank=True)
    publishdate = models.DateField()
    #path = models.FilePathField(blank=True, null=True)
    words = models.ManyToManyField(Word, through='files.FileWord', related_name='files')
    author = models.ForeignKey(Author, null=True, related_name = 'files')
    total_words = property(_total_words)
    distinct_words = property(_distinct_words)
    original = models.FileField(upload_to='textfiles')
    fileloaded = models.BooleanField(default=False)
    
    #def save(self, *args, **kwargs):
        #super(File, self).save(*args, **kwargs)
        #f = open(self.original.path, 'r')
        #orgfile = pFile(f)
        #fulltext = orgfile.read()
        #file_load.send(sender=None, fileobj=self)
        #self.loadtext(fulltext)
    def loadtext(self, fulltext):
        try:
            print_log('Start load text for file: ' + str(self.id))
            lines = fulltext.splitlines()
            c_lines = 1
            c_words = 1
            c_sentence = 1
            filewords=[]
            add_string = ''
            words = Word.objects.all().values_list('value','id')
            dwords = dict(list(words))
            for line in lines:
                wordset = line.split()
                add_string += '\n'
                #filewords = []
                for word_value in wordset:
                    new_word = FileWord(file=self)
                    new_word.lineno = c_lines
                    new_word.wordno = c_words
                    new_word.sentenceno = c_sentence
                    new_word.word_original = add_string + word_value.decode("utf-8")
                    add_string = ''               
                    word_fixed = Word.fix_word_str(word_value)
                    # Check the dictionary of words before adding word to DB
                    if dwords.get(word_fixed):
                        #print 'exists - ' + str(word_fixed) 
                        word_id = dwords[word_fixed]
                    else:
                        #print 'CREATING - ' + str(word_fixed) 
                        word_id = Word.get_word(word_fixed).id
                        dwords[word_fixed]=word_id
                    new_word.word_id = word_id  #Word.get_word(word_fixed)   #Word.get_word(re.sub('[^A-Za-z0-9]+', '', word_value))
                    #new_word.save()
                    filewords.append(new_word)
                    c_words += 1
                    if Word.is_end_of_sentence(word_value): c_sentence += 1
                    if len(filewords)>998:
                        try:
                            FileWord.objects.bulk_create(filewords)
                        except MySQLdb.Warning, e:
                            print_error(e,level='DEBUG')
                            pass                        
                        filewords=[]
                c_lines += 1
            print_log('End load text for file: ' + str(self.id))
            self.fileloaded = True
            self.save()
        except Exception as e:
            print_error(e,withprint=True)
            #print filewords
    
class FileWord (models.Model):
    file = models.ForeignKey(File, related_name = 'filewords')
    word = models.ForeignKey(Word, related_name = 'filewords')
    word_original = models.CharField(max_length=256, null=False, blank=False, db_index=True)
    appears = models.IntegerField(default=0)
    wordno = models.IntegerField(default=0)
    lineno = models.IntegerField(default=0)
    pageno = models.IntegerField(default=0)
    sentenceno = models.IntegerField(default=0)
    paragraphno = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u'%d (File %d) %s' % (self.id, self.file.id, self.word.value)    
    
    def save(self, *args, **kwargs):
        try:
            if not self.pk:
                try:
                    word_value = kwargs.pop('word_value', None)
                    if word_value:
                        #print 'FileWord save - checking word'
                        self.word = Word.get_word(word_value)
                except:
                    pass
        except Exception as e:
            print_error(e)
            
        super(FileWord, self).save(*args, **kwargs)

def load_file_to_db(sender, **kwargs):
    if kwargs.get('created') is True:
        fileobj=kwargs.get('instance')    
        #fileobj = kwargs['fileobj']
        f = open(fileobj.original.path, 'r')
        orgfile = pFile(f)
        fulltext = orgfile.read()
        t = threading.Thread(target=fileobj.loadtext,
                             args=[fulltext])
        t.setDaemon(True)
        t.start()        
        #fileobj.loadtext(fulltext)
# Catches new file to load

models.signals.post_save.connect(load_file_to_db, sender=File)
#file_load.connect(load_file_to_db)