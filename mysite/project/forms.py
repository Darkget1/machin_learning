from django import forms
from project.models import Project, Project_setting

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project  # 사용할 모델
        fields = ['subject', 'content','target_product']
        labels = {
            'subject': '제목',
            'content': '내용',
            'target_product' : '제품'
        }
class Project_settingForm(forms.ModelForm):
    class Meta:
        model = Project_setting
        fields = {
            'date_1st':'시작날짜',
            'date_2nd':'종료날짜',
            'brand_add':'브랜드추가'
        }