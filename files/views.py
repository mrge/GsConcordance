from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from files.models import File, FileWord
from general.tools import query_to_list, print_log, print_error,call_an_sp
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#from django.db import connection,connections

from words.models import Word
# Create your views here.
@login_required
def index(request):
    return files_page(request)  

def files_page(request,context={}):
    files_list = File.objects.filter(active=True).select_related('words').annotate(word_count=Count('words'))
    stats_list = None #call_an_sp('SP_GET_STATS_BY_FILE_ID',None)
    new_context = {'stats_list':stats_list,'files_list': files_list, 'title':'Files list'}
    #context = dict(context.items() + new_context.items())
    return render(request, 'files/index.html', new_context)

@login_required
def detail(request, file_id):
    fileobj = get_object_or_404(File, pk=file_id)
    searchbox = request.GET.get('searchbox')
    linenumber = request.GET.get('linenumber')
    wordnumber = request.GET.get('wordnumber')    
    error_message=None
    words = None
    words_list = None
    total_filewords = None
    if searchbox:
        searchbox = searchbox.upper()
        total_filewords = FileWord.objects.filter(file_id__exact=file_id, word__value__contains=searchbox).count()
        words_list = FileWord.objects.select_related().filter(file_id__exact=file_id, word__value__contains=searchbox).values('word__id','word__value').annotate(total=Count('word__id')).order_by('word__value')
    elif linenumber:
        try:
            linenumber = int(linenumber)
            total_filewords = FileWord.objects.filter(file_id__exact=file_id, lineno=linenumber).count()
            words_list = FileWord.objects.select_related().filter(file_id__exact=file_id, lineno=linenumber).values('word__id','word__value').annotate(total=Count('word__id')).order_by('word__value')
        except:
            error_message = "Please enter a valid numeric line number"          
    elif wordnumber:
        try:
            wordnumber = int(wordnumber)
            total_filewords = FileWord.objects.filter(file_id__exact=file_id, wordno=wordnumber).count()
            words_list = FileWord.objects.select_related().filter(file_id__exact=file_id, wordno=wordnumber).values('word__id','word__value').annotate(total=Count('word__id')).order_by('word__value')
        except:
            error_message = "Please enter a valid numeric line number"          
    else:
        total_filewords = FileWord.objects.filter(file_id__exact=file_id).count()
        words_list = FileWord.objects.select_related().filter(file_id__exact=file_id).values('word__id','word__value').annotate(total=Count('word__id')).order_by('word__value')

    stats_list = None #call_an_sp('SP_GET_STATS_BY_FILE_ID',file_id)
    
    if words_list:
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
    #words_list = FileWord.objects.select_related().filter(file_id__exact=file_id).order_by('word__value')
    context = {'stats_list':stats_list,'file': fileobj, 'object_list':words, 'total_filewords':total_filewords, 
               'searchbox':searchbox, 'error_message':error_message, 'linenumber':linenumber, 'wordnumber':wordnumber}
    return render(request, 'files/detail.html', context)

def view(request, file_id):
    fileobj = get_object_or_404(File, pk=file_id)
    text = ' '.join(FileWord.objects.filter(file_id=file_id).values_list('word_original', flat=True).order_by('id'))
    context = {'file':fileobj,'text':text}
    return render(request, 'files/view.html', context)

def fileword_detailv(request,file_id,word_value):
    word = get_object_or_404(Word, value=word_value)
    return fileword_detail(request,file_id,word.id)
    
def fileword_detail(request,file_id,word_id):
    fileobj = get_object_or_404(File, pk=file_id)
    word = get_object_or_404(Word, pk=word_id)
    filewords = FileWord.objects.raw('CALL SP_GET_WORD_BY_WORD_ID(%s,%s);',[word_id,file_id])
    filewords_total = len(list(filewords))
    context = {'filewords_total':filewords_total,'filewords_list': filewords, 'title':'Word in file','file':fileobj,'searchtitle':word.value, 'objtype': 'Word'}
    return render(request, 'files/fileword_detail.html', context) 



def allstats(request):
    return filestats(request,None)

def filestats(request,file_id):
    if file_id:
        fileobj = get_object_or_404(File, pk=file_id)
        stats_list = call_an_sp('SP_GET_STATS_BY_FILE_ID',file_id)
    else:
        fileobj = None
        stats_list = call_an_sp('SP_GET_STATS_BY_FILE_ID',None)
    context = {'stats_list':stats_list, 'file': fileobj}
    return render(request, 'files/statsview.html', context) 