from django.db import models
from general.models import Objectbase
import re

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
    
    @staticmethod
    def word_exists(word):
        return Word.objects.filter(value=word).exists()

    @staticmethod
    def get_word(word):
        try:
            return Word.objects.filter(value=word)[0]
        except:
            return Word.objects.create(value=word)

    
class WordGroup (Objectbase):
    name = models.CharField(max_length=256, null=False, blank=False)
    words = models.ManyToManyField(Word, related_name = 'groups')
    
