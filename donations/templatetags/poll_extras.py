from django import template
from django.db.models import Sum
from donations.models import Donation

register = template.Library()

@register.simple_tag
def get_donation_sum():
    donation_list = Donation.objects.all()
    sum = donation_list.aggregate(Sum('amount'))['amount__sum']
    return sum
