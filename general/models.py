from django.db import models
from django.contrib.auth.models import User
from files.signals import file_load

class Objectbase(models.Model):
    
    createtime = models.DateTimeField(auto_now_add=True, editable=False, help_text="Create time")
    lastupdatetime = models.DateTimeField(auto_now=True, editable=False, help_text="Time of the last change.")
    createby = models.ForeignKey(User, editable=False, related_name="%(class)s_createby",
                                 null=True, blank=True, # <- If the model used outsite a real request (e.g. unittest, db shell)
                                 help_text="User that created this entry.")
    lastupdateby = models.ForeignKey(User, editable=False, related_name="%(class)s_lastupdateby",
                                     null=True, blank=True, # <- If the model used outsite a real request (e.g. unittest, db shell)
                                     help_text="User that last edit this entry.")
    active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True    
    
class Author(Objectbase):
    firstname = models.CharField(max_length = 100, null=False, blank=False)
    lastname = models.CharField(max_length = 100, null=False, blank=False)
    details = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return u'%d %s %s' % (self.id, self.firstname, self.lastname)
    
