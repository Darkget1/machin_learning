from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import PostingForm
from ..models import Posting


@login_required(login_url='common:login')
def posting_create(request):
    if request.method == 'POST':
        form = PostingForm(request.POST)
        if form.is_valid():
            posting = form.save(commit=False)
            posting.author = request.user
            posting.create_date = timezone.now()
            posting.save()
            return redirect('posting:index')
    else:
        form = PostingForm()
    context = {'form': form}
    return render(request, 'posting/posting_form.html', context)

@login_required(login_url='common:login')
def posting_modify(request, posting_id):
    posting = get_object_or_404(Posting, pk=posting_id)
    if request.user != posting.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('posting:detail', posting_id=posting.id)
    if request.method == "POST":
        form = PostingForm(request.POST, instance=posting)
        if form.is_valid():
            posting = form.save(commit=False)
            posting.modify_date = timezone.now()  # 수정일시 저장
            posting.save()
            return redirect('posting:detail', posting_id=posting.id)
    else:
        form = PostingForm(instance=posting)
    context = {'form': form}
    return render(request, 'posting/posting_form.html', context)

@login_required(login_url='common:login')
def posting_delete(request, posting_id):
    posting = get_object_or_404(Posting, pk=posting_id)
    if request.user != posting.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('posting:detail', posting_id=posting.id)
    posting.delete()
    return redirect('posting:index')

