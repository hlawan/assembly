from django.db import models

# Create your models here.

class Member(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    house_number = models.PositiveSmallIntegerField(null=True, blank=True)
    post_code = models.PositiveSmallIntegerField(null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    mail = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)

class MonthlyContribution(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    direct_debit = models.BooleanField(default=True)

class Donation(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    date = models.DateField()
    arrived = models.BooleanField(default=False)
    monthly_contribution = models.ForeignKey(MonthlyContribution, on_delete=models.CASCADE, blank=True, null=True)
