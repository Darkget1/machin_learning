from django import forms
from project.models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project  # 사용할 모델
        fields = ['subject', 'content','target_product']
        labels = {
            'subject': '제목',
            'content': '내용',
            'target_product' : '제품'
        }