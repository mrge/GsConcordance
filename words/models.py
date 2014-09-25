from django.db import models
from general.models import Objectbase

# Create your models here.
class Word (Objectbase):
    value = models.CharField(max_length=256, null=False, blank=False)
    
