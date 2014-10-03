from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
from files.models import File, FileWord
from words.models import Word
from general.tools import random_slug

class FileWordInline(admin.TabularInline):
    model = FileWord
    fk_name = "file"
    #ordering = ("-active","param__code","id")
    extra=0
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows':3, 'cols':40})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }    
    
#    readonly_fields = ('scope_link', )
#    def scope_link(self, obj):
#        try:
#            change_url = urlresolvers.reverse('admin:apps_appscopeparam_change', args=(obj.paramscope.id,))
#            return mark_safe("<a href='%s'>scope (%s) %d for param %d</a>" % (change_url,obj.paramscope.name,obj.paramscope.id, obj.id))
#        except:
#            return "-----"
#    #accappparam_link.allow_tags = True
#        
#    def formfield_for_foreignkey(self, db_field, request, **kwargs):
#        if db_field.name == "param1":
#            kwargs["queryset"] = AppParam.filters
#        return super(AppParamInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
#
#    def save_model(self, request, obj, form, change):
#        instance = form.save(commit=False)
#        #if not hasattr(instance,'createby'):
#        instance.createby = request.user.id
#        instance.lastupdateby = request.user.id
#        instance.save()
#        form.save_m2m()
#        return instance
#    def queryset(self, request):
#        return super(FileWordInline, self).queryset(request).prefetch_related('word') 

class FileAdmin(admin.ModelAdmin):
    #inlines = [
    #    FileWordInline,
    #]

    list_display = ('id', 'code', 'active', 'original','author','fileloaded')
    search_fields = ['=id', 'code']
    date_hierarchy = 'createtime'
    list_display_links = ('id', 'code')
    #list_filter = ('active')
    #filter_horizontal = ('author',)    
    ordering = ('fileloaded','-id',)
    #raw_id_fields = ('image',)
    #readonly_fields = ['fileloaded','code']

    def get_readonly_fields(self, request, obj=None):
        if obj: # obj is not None, so this is an edit
            return ['fileloaded','code','original'] # Return a list or tuple of readonly fields' names
        else: # This is an addition
            return ['fileloaded','code']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'rows':4, 'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }      
    
    def save_model(self, request, obj, form, change): 
        obj.createby = request.user
        obj.lastupdateby = request.user
        obj.code = random_slug()
        obj.save()

    def queryset(self, request):
        return super(FileAdmin, self).queryset(request).prefetch_related('filewords','filewords__word')        

admin.site.register(File,FileAdmin)