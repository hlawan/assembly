from django.forms import ModelForm

from . import models

class MemberForm(ModelForm):
    class Meta:
        model = models.Member
        exclude = []
