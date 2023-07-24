from django import forms

class SearchForm(forms.Form):
    news_topic = forms.CharField(label='Topic keyword',max_length=10)
    news_title = forms.CharField(label='Search keyword', max_length=20)

#update, delete form
class UDForm(forms.Form):
    UD = forms.CharField(label='UD',max_length=10)