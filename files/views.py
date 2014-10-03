from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from files.models import File, FileWord
from general.tools import query_to_list, print_log, print_error,call_an_sp
from django.db.models import Count
#from django.db import connection,connections

from words.models import Word
# Create your views here.
@login_required
def index(request):
    return files_page(request)  

def files_page(request,context={}):
    files_list = File.objects.filter(active=True)
    #cursor = connection.cursor()
    #cursor.execute('CALL SP_GET_STATS_BY_FILE_ID(%s)',[1])
    stats_list = call_an_sp('SP_GET_STATS_BY_FILE_ID',None)
    #stats_list = query_to_list('CALL SP_GET_STATS_BY_FILE_ID(%s)',[1])         
    new_context = {'stats_list':stats_list,'files_list': files_list, 'title':'Files list'}
    #context = dict(context.items() + new_context.items())
    return render(request, 'files/index.html', new_context)

@login_required
def detail(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    total_filewords = FileWord.objects.filter(file_id__exact=file_id).count()
    words_list = FileWord.objects.select_related().filter(file_id__exact=file_id).values('word__id','word__value').annotate(total=Count('word__id')).order_by('word__value')
    stats_list = call_an_sp('SP_GET_STATS_BY_FILE_ID',file_id)
    #words_list = FileWord.objects.select_related().filter(file_id__exact=file_id).order_by('word__value')
    context = {'stats_list':stats_list,'file': file, 'words_list':words_list, 'total_filewords':total_filewords}
    return render(request, 'files/detail.html', context)


def fileword_detail(request,file_id,word_id):
    file = get_object_or_404(File, pk=file_id)
    word = get_object_or_404(Word, pk=word_id)
    filewords = FileWord.objects.raw('CALL SP_GET_WORD_BY_WORD_ID(%s,%s);',[word_id,file_id])
    filewords_total = len(list(filewords))
    context = {'filewords_total':filewords_total,'filewords_list': filewords, 'title':'Word in file','file':file,'word':word}
    return render(request, 'files/fileword_detail.html', context) 