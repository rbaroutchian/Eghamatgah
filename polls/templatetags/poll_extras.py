from django import template


register = template.Library()


@register.filter(name='three_digits_currency')
def three_digits_currency(value:int):
    return '{:,}'.format(value) + 'تومان'


# @register.filter(name='show_jalali_date')
# def show_jalali_date(value):
#     return date2jalali(value)
