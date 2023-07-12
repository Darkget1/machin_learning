from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import CommentForm
from ..models import Posting, Comment

@login_required(login_url='common:login')
def comment_create_posting(request, posting_id):
    # posting 질문 댓글 등록
    posting = get_object_or_404(Posting, pk=posting_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.posting = posting
            comment.save()
            return redirect('{}#comment_{}' .format(resolve_url('posting:detail',
                            posting_id=comment.posting.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'posting/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_posting(request, comment_id):
    # posting 질문 댓글 수정
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('posting:detail', posting_id=comment.posting.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()  # 수정일시 저장
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('posting:detail',
                            posting_id=comment.posting.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'posting/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_posting(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('posting:detail', posting_id=comment.posting.id)
    else:
        comment.delete()
    return redirect('posting:detail', posting_id=comment.posting.id)
# 답변의 댓글 등록, 수정, 삭제 함수
# @login_required(login_url='common:login')
# def comment_create_article(request, article_id):
#     # posting 질문 댓글 등록
#     article = get_object_or_404(Article, pk=article_id)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.create_date = timezone.now()
#             comment.article = article
#             comment.save()
#             return redirect('{}#comment_{}' .format(resolve_url('posting:detail',
#                             article_id=comment.article.id), comment.id))
#     else:
#         form = CommentForm()
#     context = {'form': form}
#     return render(request, 'posting/comment_form.html', context)
#
# @login_required(login_url='common:login')
# def comment_modify_article(request, comment_id):
#     # posting 질문 댓글 수정
#     comment = get_object_or_404(Comment, pk=comment_id)
#     if request.user != comment.author:
#         messages.error(request, '댓글수정권한이 없습니다')
#         return redirect('posting:detail', article_id=comment.article.id)
#
#     if request.method == "POST":
#         form = CommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.modify_date = timezone.now()  # 수정일시 저장
#             comment.save()
#             return redirect('{}#comment_{}'.format(resolve_url('posting:detail',
#                             article_id=comment.article.id), comment.id))
#     else:
#         form = CommentForm(instance=comment)
#     context = {'form': form}
#     return render(request, 'posting/comment_form.html', context)
#
# @login_required(login_url='common:login')
# def comment_delete_article(request, comment_id):
#     comment = get_object_or_404(Comment, pk=comment_id)
#     if request.user != comment.author:
#         messages.error(request, '댓글삭제권한이 없습니다')
#         return redirect('posting:detail', article_id=comment.article.id)
#     else:
#         comment.delete()
#     return redirect('posting:detail', article_id=comment.article.id)
# # 답변의 댓글 등록, 수정, 삭제 함수