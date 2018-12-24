from django.db import models
from django.urls import reverse

# Create your models here.

class Member(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    house_number = models.PositiveSmallIntegerField(null=True, blank=True)
    post_code = models.PositiveSmallIntegerField(null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    mail = models.EmailField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('member-detail', args=[str(self.id)])

    def __str__(self):
        return self.first_name + " " + \
               self.last_name

class FrequentContribution(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    period = models.DurationField()
    direct_debit = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('frequentcontribution-detail', args=[str(self.id)])

    def __str__(self):
        return self.member.first_name + " " + \
               self.member.last_name + " ( " + \
               str(self.amount) + "€ )"

class Donation(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    date = models.DateField()
    arrived = models.BooleanField(default=False)
    frequent_contribution = models.ForeignKey(FrequentContribution, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('donation-detail', args=[str(self.id)])

    def __str__(self):
        return self.member.first_name + " " + \
               self.member.last_name + " ( " + \
               str(self.amount) + "€ )"
