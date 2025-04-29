from django import template
from persiantools.jdatetime import JalaliDate



register = template.Library()


@register.filter(name='three_digits_currency')
def three_digits_currency(value:int):
    return '{:,}'.format(value) + 'تومان'


# @register.filter(name='show_jalali_date')
# def show_jalali_date(value):
#     return date2jalali(value)

@register.filter
def to_jalali(value):
    if not value:
        return ""
    try:
        return JalaliDate(value).strftime('%Y/%m/%d')
    except Exception:
        return value


@register.simple_tag
def today_jalali():
    return JalaliDate.today().strftime('%Y/%m/%d')
