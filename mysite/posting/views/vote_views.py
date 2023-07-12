from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from ..models import Posting


@login_required(login_url='common:login')
def vote_posting(request, posting_id):
    """
    posting 질문추천등록
    """
    posting = get_object_or_404(Posting, pk=posting_id)
    if request.user == posting.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        posting.voter.add(request.user)
    return redirect('posting:detail', posting_id=posting.id)


# @login_required(login_url='common:login')
# def vote_posting(request, aritlce_id):
#     """
#     posting 모집추천등록
#     """
#     posting = get_object_or_404(Question, pk=article_id)
#     if request.user == article.author:
#         messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
#     else:
#         article.voter.add(request.user)
#     return redirect('posting:detail', article_id=posting.id)
