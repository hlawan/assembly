from django.shortcuts import render
from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from django.http import FileResponse

from donations.models import Member
from donations.models import Donation
from donations.models import FrequentContribution

from . import forms

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime
import subprocess
import tempfile
import os
import re
from num2words import num2words

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
    success_url = reverse_lazy('member-create')

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
    success_url = reverse_lazy('donation-create')

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

# Spendenbescheinigung

@login_required
def render_donation_certificate(request, pk=None):
    template_name = "donations/latex/spendenbescheinigung.tex"
    template = get_template(template_name)

    member = Member.objects.get(pk=pk)

    # TODO: use last year instead of a fix year. later make it
    # variable.
    donations = member.donation_set.filter(date__year=2018)

    total_amount = sum(d.amount for d in donations)

    multiple = len(donations) > 1

    if multiple:
        date = "01.01.2018--31.12.2018"
    else:
        date = donations[0].date

    # TODO: what other information is needed for the template?
    context = { "member": member,
                "donations": donations,
                "amount": total_amount,
                "amountwords": num2words(total_amount, lang='de'),
                "date": date,
                "multiple": multiple}

    rendered = template.render(context)

    with tempfile.TemporaryDirectory() as output_directory:
        subprocess.run(["pdflatex",
                        "--jobname=foo",
                        "--output-directory=" + output_directory],
                       input=rendered.encode())

        # TODO: later build a cache for the generated
        # spendenbescheinigungen

        return FileResponse(open(output_directory + os.sep + "foo.pdf", 'rb'))

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
