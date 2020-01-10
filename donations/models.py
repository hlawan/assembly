from django.db import models
from django.urls import reverse
from django.db.models import Sum

# Create your models here.

class FrequentContribution(models.Model):
    name = models.CharField(max_length=200)
    execution_date = models.DateField(null=True, blank=True)
    
    def get_absolute_url(self):
        return reverse('frequentcontribution-detail', args=[str(self.id)])

    def get_members(self):
        frequent = FrequentContribution.objects.get(pk=self.id)
        members = frequent.member_set.all() 
        return members

    def __str__(self):
        return self.name

class Member(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    house_number = models.CharField(max_length=5,null=True, blank=True)
    post_code = models.PositiveSmallIntegerField(null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    mail = models.EmailField(max_length=200, null=True, blank=True)
    membership = models.CharField(max_length=200, choices=[('voting','Voting Membership'),('supporting', 'Supporting Membership'), ('none','None')])
    entry_date = models.DateField(null=True, blank=True)
    frequent = models.ForeignKey(FrequentContribution, on_delete=models.SET_NULL, null=True, blank=True)
    membership_fee = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    pay_method = models.CharField(max_length=200, choices=[('cash','Cash'),('direct_debit', 'Direct Debit'), ('transfer','Transfer'), ('better_place', 'BetterPlace')], null=True, blank=True)

    def get_absolute_url(self):
        return reverse('member-detail', args=[str(self.id)])

    def get_donations(self):
        u = Member.objects.get(pk=self.id)
        donations = u.donation_set.all() 
        return donations
    
    def __str__(self):
        return self.first_name + " " + \
               self.last_name

# getter
def voting_members():
    return Member.objects.filter(membership='voting')

def supporting_members():
    return Member.objects.filter(membership='supporting')

def external_members():
    return Member.objects.filter(membership='none')

class Donation(models.Model):
    member = models.ForeignKey(Member, related_name="donation_set", on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    date = models.DateField()
    arrived = models.BooleanField(default=False)
    frequent_contribution = models.ForeignKey(FrequentContribution, on_delete=models.SET_NULL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('donation-detail', args=[str(self.id)])

    def __str__(self):
        return self.member.first_name + " " + \
               self.member.last_name + " ( " + \
               str(self.amount) + "€ )"

    def get_donation_sum():
        return Donation.objects.all(Sum('amount'))
