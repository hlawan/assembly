from django import template
from django.db.models import Sum
from donations.models import Donation
from datetime import datetime

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.simple_tag
def get_donation_sum():
    donation_list = Donation.objects.all()
    sum = donation_list.aggregate(Sum('amount'))['amount__sum']
    return sum

@register.simple_tag
def last_year():
    last_year = datetime.now().year - 1
    return str(last_year)

def currency(euro):
    euro = round(float(euro), 2)
    return "%s%s" % (int(euro), ("%0.2f" % euro)[-3:])

register.filter('currency', currency)
