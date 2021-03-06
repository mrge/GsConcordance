from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
from files.models import File, FileWord
from general.models import Author
from words.models import Word, WordGroup, WordPhrase


class GroupThroughInline(admin.TabularInline):
    model = WordGroup.words.through
    
    
class PhraseThroughInline(admin.TabularInline):
    model = WordPhrase.words.through
    ordering = ('sort',)
    extra = 0
    raw_id_fields = ('word',)

#    def formfield_for_foreignkey(self, db_field, request, **kwargs):
#        if db_field.name == "word":
#            kwargs["queryset"] = Word.objects.filter(active=True).values('value').order_by('value')
#        return super(PhraseThroughInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
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
#    inlines = [
#        WordsInline,
#    ]

    list_display = ('id', 'name')
    search_fields = ['=id', 'name']
    date_hierarchy = 'createtime'
    list_display_links = ('id', 'name')
    #list_filter = ('active')
    filter_horizontal = ('words',)    
    ordering = ('-id',)
    #raw_id_fields = ('image',)
    #readonly_fields = ['image_link']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'rows':4, 'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }      

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "words":
            kwargs["queryset"] = Word.objects.filter(active=True).order_by('value')
        return super(WordGroupAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change): 
        obj.createby = request.user
        obj.lastupdateby = request.user
        obj.save()

class WordPhraseAdmin(admin.ModelAdmin):
    inlines = [
        PhraseThroughInline,
    ]

    list_display = ('id', 'name')
    search_fields = ['=id', 'name']
    date_hierarchy = 'createtime'
    list_display_links = ('id', 'name')
    #list_filter = ('active')
    filter_horizontal = ('words',)    
    ordering = ('-id',)
    #raw_id_fields = ('image',)
    #readonly_fields = ['image_link']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'rows':4, 'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }      

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "words":
            kwargs["queryset"] = Word.objects.filter(active=True).order_by('value')
        return super(WordPhraseAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change): 
        obj.createby = request.user
        obj.lastupdateby = request.user
        obj.save()
        
class WordAdmin(admin.ModelAdmin):

    list_display = ('id', 'value')
    search_fields = ['=id', 'value']
    date_hierarchy = 'createtime'
    list_display_links = ('id', 'value')
    list_filter = ('active','filewords__file__title')
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
admin.site.register(WordPhrase,WordPhraseAdmin)