from django.db import models
from django.contrib.auth.models import User

class Objectbase(models.Model):
    
    createtime = models.DateTimeField(auto_now_add=True, editable=False, help_text="Create time")
    lastupdatetime = models.DateTimeField(auto_now=True, editable=False, help_text="Time of the last change.")
    createby = models.ForeignKey(User, editable=False, related_name="%(class)s_createby",
                                 null=True, blank=True, # <- If the model used outsite a real request (e.g. unittest, db shell)
                                 help_text="User how create this entry.")
    lastupdateby = models.ForeignKey(User, editable=False, related_name="%(class)s_lastupdateby",
                                     null=True, blank=True, # <- If the model used outsite a real request (e.g. unittest, db shell)
                                     help_text="User as last edit this entry.")
    active = models.BooleanField(default=True, db_index=True)