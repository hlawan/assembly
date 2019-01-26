from django import template
from django.db.models import Sum

register = template.Library()

@register.simple_tag
def get_donation_sum(donationList):
    
    sum = donationList.aggregate(Sum('amount'))['amount__sum']
    return sum
