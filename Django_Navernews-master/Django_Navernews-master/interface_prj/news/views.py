from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from news.models import Letter 

from django.utils import timezone
import time
from news._crawling import parsing, selenium_parsing, new100_parsing, selenium_parsing_new100

from news.forms import SearchForm, UDForm
from django.db.models import Q
from django.views.generic.edit import FormView

# Create your views here.

def news_list(request):
    contents = {}
    key = 0
    try:
        economy=  Letter.objects.filter(category__icontains='101' )#.order_by('-created_date')
        it_sc = Letter.objects.filter(category__icontains='105' )#.order_by('-created_date')
        sports= Letter.objects.filter(category__icontains='sports' )#.order_by('-created_date')
        contents = {'economy': economy , 'it_sc': it_sc, 'sports':sports}
    except:
        key=1
        
    return render(request, 'news/news_list.html',{'message':contents, 'key':key})


def news_category_sports(request):
    key = ['sports',]
    sports=['kbaseball','kfootball','wfootball']
    sportss=[]
    contents={}
    func = lambda __sid1__, __sid2__: Letter.objects.filter(category__icontains=__sid1__, topic__icontains=__sid2__)#.order_by('-created_date')
    for sid2 in sports:
        sportss.append(func('sports',sid2))
        contents = {'m': sportss}
    key.append(sports)
    return render(request, 'news/news_category.html', {'message': contents , 'key': key})


def news_category_list(request, sid1):
    key = [sid1,]
    economy = ['259','258','261']
    it_sc=['731','226','227']
    economys=[]
    it_scs=[]
    contents={}
    func = lambda __sid1__,__sid2__: Letter.objects.filter(category__icontains=__sid1__, topic__icontains=__sid2__)
    if key[0] =='101':
        print('101')
        for sid2 in economy:
            economy_topic= func(sid1,sid2)
            economys.append(economy_topic)
        contents={'m': economys}
        key.append(economy)

    elif key[0] == '105':
        print('105')
        for sid2 in it_sc:
            it_topic = func(sid1,sid2)
            it_scs.append(it_topic)
        contents={'m': it_scs}
        key.append(it_sc)


    return render(request, 'news/news_category.html', {'message': contents , 'key': key})


def news_detail(request, sid1, sid2):
    mylist = [sid1, sid2]
    if request.method == 'POST':
        UDform = UDForm(request.POST)
        if UDform.is_valid():
            # 최신 데이터 10개 가져오기
            if UDform.cleaned_data['UD'] == 'update':
                contents = parsing(sid1, sid2)
                for data in contents:
                    form = Letter(
                        category=sid1,
                        topic=sid2,
                        title= data[0],
                        letter_link=data[1],
                        published_date=data[2],
                        preview= data[3],
                        writer=data[4]
                        )
                    form.save()
            # 최신 데이터 100개 가져오기
            elif UDform.cleaned_data['UD'] == 'new100':
                contents = new100_parsing(sid1,sid2)
                for data in contents:
                    form = Letter(
                        category=sid1,
                        topic=sid2,
                        title= data[0],
                        letter_link=data[1],
                        published_date=data[2],
                        preview= data[3],
                        writer=data[4]
                        )
                    form.save()
            # 데이터 전부 삭제
            elif UDform.cleaned_data['UD'] =='delete':
                Letter.objects.filter(topic=sid2).delete()

    else:
        print('GET')
    News = Letter.objects.filter(topic= sid2)
    
    # pagination
    paginator = Paginator(News,3)
    page_no = request.GET.get('page')
    try:
        News_p = paginator.page(page_no)
    except PageNotAnInteger:
        News_p = paginator.page(1)
    except EmptyPage:
        News_p = paginator.page(paginator.num_pages)

    return render(request, 'news/news_detail.html' ,{'message': News_p, 'key':mylist})


def news_sports(request, sports):
    if request.method == 'POST':       
        
        UDform = UDForm(request.POST)
        if UDform.is_valid():
            if UDform.cleaned_data['UD'] == 'update':
                contents = selenium_parsing(sports)
                for data in contents:
                    form = Letter(
                        category = 'sports',
                        topic= sports,
                        title= data[0],
                        letter_link=data[1],
                        published_date=data[2],
                        preview= data[3],
                        writer=data[4]
                        )
                    form.save()
            elif UDform.cleaned_data['UD'] == 'new100':
                contents = selenium_parsing_new100(sports)
                for data in contents:
                    form = Letter(
                        category = 'sports',
                        topic= sports,
                        title= data[0],
                        letter_link=data[1],
                        published_date=data[2],
                        preview= data[3],
                        writer=data[4]
                        )
                    form.save()

            elif UDform.cleaned_data['UD'] =='delete':
                Letter.objects.filter(topic=sports).delete()
    else:
        print('GET')
    News = Letter.objects.filter(topic= sports ,created_date__lte = timezone.now())
    paginator = Paginator(News,3)
    page_no = request.GET.get('page')
    try:
        News_p = paginator.page(page_no)
    except PageNotAnInteger:
        News_p = paginator.page(1)
    except EmptyPage:
        News_p = paginator.page(paginator.num_pages)
    return render(request, 'news/news_sports.html',{'message':News_p, 'key':sports})


def news_search(request):
    context ={}
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['news_topic']
            _title = form.cleaned_data['news_title']
            news_list=[]
            if topic== 'default':
                news_list = Letter.objects.filter(title__icontains=_title)
            else:
                news_func = lambda __x__: Letter.objects.filter(Q(topic__icontains=__x__) & Q(title__icontains=_title)).distinct()
                news_list = news_func(topic)
           
            context['form'] = form
            context['search_keyword'] = _title 
            context['result_list']= news_list
            return render(request, 'news/news_search.html', {'search_list': context})

    else:
        form = SearchForm()

    return render(request, 'news/news_search.html', {'search_list': context})
