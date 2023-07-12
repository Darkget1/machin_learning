from django import forms
from posting.models import Posting, Comment


class PostingForm(forms.ModelForm):
    class Meta:
        model = Posting  # 사용할 모델
        fields = ['subject', 'content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }

