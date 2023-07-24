from django import template

register = template.Library()

@register.filter()
def __zip(value,count):
    count2 = [1,2,3]
    return zip(value, count2)


@register.filter()
def __topic(value):
    if value =='259':
        return '금융'
    elif value == '258':
        return '증권'
    elif value == '261':
        return '산업/재계'
    elif value == '731':
        return '모바일'
    elif value == '226':
        return '인터넷/SNS'
    elif value == '227':
        return '통신/뉴미디어'
    elif value == 'kbaseball':
        return '야구'
    elif value == 'kfootball':
        return '축구'
    elif value == 'wfootball':
        return '해외축구'

@register.filter()
def __category(value):
    if value == '101':
       return '경제'
    elif value == '105':
        return 'IT/과학'
    elif value == 'sports':
        return '스포츠'
