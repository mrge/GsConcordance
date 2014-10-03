from django.db import models
from general.models import Objectbase
import re
from general.tools import print_error

# Create your models here.
class Word (Objectbase):
    value = models.CharField(max_length=256, null=False, blank=False, db_index=True)
    
    @staticmethod
    def is_end_of_sentence(word):
        sentenceEnders = re.compile(r"""
            # Split sentences on whitespace between them.
            (?:               # Group for two positive lookbehinds.
              (?<=[.!?])      # Either an end of sentence punct,
            | (?<=[.!?]['"])  # or end of sentence punct and quote.
            )                 # End group of two positive lookbehinds.
            (?<!  Mr\.   )    # Don't end sentence on "Mr."
            (?<!  Mrs\.  )    # Don't end sentence on "Mrs."
            (?<!  Jr\.   )    # Don't end sentence on "Jr."
            (?<!  Dr\.   )    # Don't end sentence on "Dr."
            (?<!  Prof\. )    # Don't end sentence on "Prof."
            (?<!  Sr\.   )    # Don't end sentence on "Sr."
            #\s+               # Split on whitespace between sentences.
            """, 
            re.IGNORECASE | re.VERBOSE)
        return sentenceEnders.search(word) is not None

    def __unicode__(self):
        return u'%d %s' % (self.id, self.value)

    def save(self, *args, **kwargs):
        try:
            self.value = self.value.upper()
        except Exception as e:
            print_error(e)
            
        super(Word, self).save(*args, **kwargs)
    
    @staticmethod
    def word_exists(word):
        return Word.objects.filter(value=word).exists()

    @staticmethod
    def get_word(word_value, stripchars = False):
        if stripchars: word_value = Word.fix_word_str(word_value)
        try:
            return Word.objects.filter(value=word_value)[0]
        except:
            return Word.objects.create(value=word_value)
        
    @staticmethod
    def fix_word_str(word_value):    
        return re.sub('[^A-Za-z0-9]+', '', word_value).upper()
    
class WordGroup (Objectbase):
    
    name = models.CharField(max_length=256, null=False, blank=False)
    words = models.ManyToManyField(Word, related_name = 'groups')

    def __unicode__(self):
        return u'%d %s' % (self.id, self.name)
