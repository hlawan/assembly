from django.shortcuts import render
from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from donations.models import Member
from donations.models import Donation
from donations.models import FrequentContribution

from . import forms

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime

# Member

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

class MemberCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Member
    form_class = forms.MemberForm

class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Member
    success_url = reverse_lazy('member-list')

# Donations

class DonationDetailView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Donation
    template_name = 'donations/donation_detail.html'
    form_class = forms.DonationForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

class DonationListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Donation
    paginate_by = 100

class DonationCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Donation
    form_class = forms.DonationForm

class DonationDeleteView(LoginRequiredMixin, DeleteView):
    model = Donation
    success_url = reverse_lazy('donation-list')

# FrequentContribution

class FrequentContributionDetailView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = FrequentContribution
    template_name = 'donations/frequentcontribution_detail.html'
    form_class = forms.FrequentContributionForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

class FrequentContributionListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = FrequentContribution
    paginate_by = 100

class FrequentContributionCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = FrequentContribution
    form_class = forms.FrequentContributionForm

class FrequentContributionDeleteView(LoginRequiredMixin, DeleteView):
    model = FrequentContribution
    success_url = reverse_lazy('frequentcontribution-list')

@login_required
def execute_frequent(request,pk=None):
    now = datetime.datetime.now()
    frequent = FrequentContribution.objects.get(id=pk)

    for member in frequent.member_set.all():
        donation = Donation(member = member,
                            amount = member.membership_fee,
                            date = now,
                            arrived = True,
                            frequent_contribution = frequent)
        donation.save()

    return redirect('donation-list')
