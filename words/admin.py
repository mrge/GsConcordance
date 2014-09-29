from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
from files.models import File, FileWord
from general.models import Author


class WordsInline(admin.TabularInline):
    model = Word
    #fk_name = "author"
    #ordering = ("-active","param__code","id")
    extra=0
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows':3, 'cols':40})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }    
#    
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

#    def save_model(self, request, obj, form, change):
#        instance = form.save(commit=False)
#        #if not hasattr(instance,'createby'):
#        instance.createby = request.user.id
#        instance.lastupdateby = request.user.id
#        instance.save()
#        form.save_m2m()
#        return instance

class WordGroupAdmin(admin.ModelAdmin):
    inlines = [
        FilesInline,
    ]

    list_display = ('id', 'name')
    search_fields = ['=id', 'name']
    date_hierarchy = 'createtime'
    list_display_links = ('id', 'name')
    #list_filter = ('active')
    #filter_horizontal = ('author',)    
    ordering = ('-id',)
    #raw_id_fields = ('image',)
    #readonly_fields = ['image_link']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'rows':4, 'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }      
    
    def save_model(self, request, obj, form, change): 
        obj.createby = request.user
        obj.lastupdateby = request.user
        obj.save()
        
class WordAdmin(admin.ModelAdmin):

    list_display = ('id', 'value')
    search_fields = ['=id', 'value']
    date_hierarchy = 'createtime'
    list_display_links = ('id', 'value')
    #list_filter = ('active')
    #filter_horizontal = ('author',)    
    ordering = ('-id',)
    #raw_id_fields = ('image',)
    #readonly_fields = ['image_link']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'rows':4, 'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }      
    
    def save_model(self, request, obj, form, change): 
        obj.createby = request.user
        obj.lastupdateby = request.user
        obj.save()


admin.site.register(WordGroup,WordGroupAdmin)
admin.site.register(Word,WordAdmin)