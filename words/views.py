from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from files.models import File, FileWord
from words.models import Word, WordGroup
from general.tools import query_to_list, print_log, print_error
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import HttpResponse

from words.models import Word
# Create your views here.
@login_required
def index(request):
    return words_page(request)  

def words_page(request,context={},wordgroup_id=None):
    wordgroup = None
    if wordgroup_id:
        wordgroup = get_object_or_404(WordGroup, pk=wordgroup_id)
        words_list = FileWord.objects.select_related().filter(word__active=True, word__groups__id = wordgroup_id).values('word__id','word__value').annotate(total=Count('word__id')).order_by('word__value')
    else:    
        words_list = FileWord.objects.select_related().filter(word__active=True).values('word__id','word__value').annotate(total=Count('word__id')).order_by('word__value')
    
    csv = request.GET.get('csv')
    if csv:
        return download_words_csv(request,words_list)

    paginator = Paginator(words_list, 100)
    page = request.GET.get('page')
    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        words = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        words = paginator.page(paginator.num_pages)             
    new_context = {'object_list': words, 'title':'Words list','wordgroup': wordgroup}
    context = dict(context.items() + new_context.items())
    return render(request, 'words/index.html', context)

def download_words_csv(request, queryset):
    import csv
    from django.http import HttpResponse
    import StringIO
 
    f = StringIO.StringIO()
    writer = csv.writer(f)
    writer.writerow(["word_id", "word_value", "total"])
 
    for s in queryset:
        print s
        writer.writerow([s['word__id'], s['word__value'], s['total']])
 
    f.seek(0)
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
    return response

@login_required
def detail(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    total_filewords = FileWord.objects.filter(word_id__exact=word_id).count()
    files_list = FileWord.objects.select_related().filter(word_id__exact=word_id).values('file__id','file__title').annotate(total=Count('file__id')).order_by('file__title')
    #words_list = FileWord.objects.select_related().filter(file_id__exact=file_id).order_by('word__value')
    context = {'word': word, 'files_list':files_list, 'total_filewords':total_filewords}
    return render(request, 'words/detail.html', context)


def wordgroup_detail(request,wordgroup_id):
    return words_page(request,wordgroup_id=wordgroup_id)
    #wordgroup = get_object_or_404(WordGroup, pk=wordgroup_id)
    #filewords = FileWord.objects.raw('CALL SP_GET_WORD_BY_WORD_ID(%s,%s);',[word_id,file_id])
    #context = {'wordgroup': wordgroup, 'title':'Word in file','file':file}
    #return render(request, 'words/fileword_detail.html', context) 

def wordgroup_words(request, wordgroup_id,word_id):
    return words_page(request,wordgroup_id=wordgroup_id)

def wordgroup_index(request):
    #wordgroups_list = WordGroup.objects.filter(active=True)
    wordgroups_list = Word.objects.select_related().filter(groups__active=True).values('groups__id','groups__name').annotate(total=Count('groups__id')).order_by('groups__id')
    context = {'wordgroups_list': wordgroups_list}
    return render(request, 'words/wg_index.html', context)    