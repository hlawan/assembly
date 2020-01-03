from django.forms import ModelForm

from . import models
from django import forms

class MemberForm(ModelForm):
    class Meta:
        model = models.Member
        exclude = []

class DonationForm(ModelForm):
    class Meta:
        model = models.Donation
        exclude = []

class FrequentContributionForm(ModelForm):
    class Meta:
        model = models.FrequentContribution
        exclude = []

class YearForm(forms.Form):
    year = forms.IntegerField(label='Year', min_value=2018)
