from django.shortcuts import render
from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from donations.models import Member
from . import forms

# Create your views here.

class MemberDetailView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Member
    template_name = 'donations/member_detail.html'
    form_class = forms.MemberForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

class MemberListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Member
    paginate_by = 100
