from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from ..models import Posting


def main(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    #정렬

    if so == 'recommend':
        posting_list = Posting.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        posting_list = Posting.objects.annotate(
            num_comment=Count('comment')).order_by('-num_comment', '-create_date')
    else:
        posting_list = Posting.objects.order_by('-create_date')

    if kw:
        posting_list = posting_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(comment__author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(posting_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'posting_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'posting/posting_list.html', context)


def detail(request, posting_id):
    posting = get_object_or_404(Posting, pk=posting_id)
    context = {'posting': posting}
    return render(request, 'posting/posting_detail.html', context)