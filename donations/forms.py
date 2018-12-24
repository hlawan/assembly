from django.forms import ModelForm

from . import models

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
