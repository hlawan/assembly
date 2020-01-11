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
from django.http import FileResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Sum

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
from PyPDF2 import PdfFileMerger

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

@login_required
def DonationListView(request):
    donation_list = Donation.objects.all().order_by('-date')
    paginator = Paginator(donation_list, 100) # Show 100 donations per page

    page = request.GET.get('page')
    donations = paginator.get_page(page)
    return render(request, 'donations/donation_list.html', {'donations': donations})

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
def render_donation_certificate(request, year=None, pk=None):
    # TODO: later build a cache for the generated
    # spendenbescheinigungen
    with tempfile.TemporaryDirectory() as output_directory:
        last_year = datetime.datetime.now().year - 1
        donation_certificate = render_donation_certificate_for_person(pk,
                                                                      output_directory,
                                                                      last_year)
        if not donation_certificate:
            raise Http404("No donations for this person yet")
        else:
            return FileResponse(open(donation_certificate, 'rb'))

def render_donation_certificate_for_person(pk, tmp_directory, year):
    template_name = "donations/latex/spendenbescheinigung.tex"
    template = get_template(template_name)

    member = Member.objects.get(pk=pk)
    donations = member.donation_set.filter(date__year=year)

    if len(donations) == 0:
        return None

    total_amount = sum(d.amount for d in donations)

    multiple = len(donations) > 1

    if multiple:
        date = "01.01." + str(year) + "--31.12." + str(year)
    else:
        date = donations[0].date

    context = { "member": member,
                "donations": donations,
                "amount": total_amount,
                "amountwords": num2words(total_amount, lang='de', to='currency'),
                "date": date,
                "multiple": multiple}

    rendered = template.render(context)

    subprocess.run(["pdflatex",
                    "--jobname=donation" + str(pk),
                    "--output-directory=" + tmp_directory],
                   input=rendered.encode())

    return tmp_directory + os.sep + 'donation' + str(pk) + ".pdf"


@login_required
def render_letter(request, pk=None):
    with tempfile.TemporaryDirectory() as output_directory:
        last_year = datetime.datetime.now().year - 1
        letter = render_letter_for_person(pk, output_directory, last_year)
        return FileResponse(open(letter, 'rb'))

def render_letter_for_person(pk, tmp_directory, year):
    template_name = "donations/latex/anschreiben_" + str(year) + ".tex"
    template = get_template(template_name)

    member = Member.objects.get(pk=pk)

    abs_file = os.path.abspath('static/anschreiben_logo.pdf')

    context = { "member": member,
                "file": abs_file}
    rendered = template.render(context)

    subprocess.run(["pdflatex",
                    "--jobname=letter" + str(pk),
                    "--output-directory=" + tmp_directory],
                   input=rendered.encode())

    return tmp_directory + os.sep + 'letter' + str(pk) + ".pdf"

def render_donations_for_all(request, year):
    all_members = Member.objects.all()
    letters = []
    certificates = []
    with tempfile.TemporaryDirectory() as output_directory:
        for member in all_members:
            member_id = member.id
            donation_certificate = render_donation_certificate_for_person(member_id,
                                                                          output_directory,
                                                                          year)
            if not donation_certificate:
                continue
            letter = render_letter_for_person(member_id, output_directory, year)
            letters.append(letter)
            certificates.append(donation_certificate)

        merger = PdfFileMerger()
        for l, c in zip(letters, certificates):
            merger.append(l)
            merger.append(c)

        with open(output_directory + 'all_users.pdf', 'wb') as output_file:
            merger.write(output_file)

        return FileResponse(open(output_directory + 'all_users.pdf', 'rb'))

@login_required
def execute_frequent(request,pk=None):
    frequent = FrequentContribution.objects.get(id=pk)

    for member in frequent.member_set.all():
        donation = Donation(member = member,
                            amount = member.membership_fee,
                            date = frequent.execution_date,
                            arrived = True,
                            frequent_contribution = frequent)
        donation.save()

    return redirect('donation-list')

def start_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.YearForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            year = form.cleaned_data["year"]
            return render_donations_for_all(request, year)
            
    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.YearForm()
        return render(request, 'start.html', {'form': form})


        
def donation_statistic_view(request):
    donation_list = Donation.objects.all()
    start = donation_list.earliest('date').date.year
    end = donation_list.latest('date').date.year

    summary = []
    
    # accumulated over all years
    all_total = 0
    all_voting = 0
    all_supporting = 0
    all_extern = 0
    
    for year in range(start, end+1):
        # per year values
        donations = donation_list.filter(date__year=year)

        # sum donations of different membertypes
        total = donations.aggregate(Sum('amount'))['amount__sum']
        voting = donations.filter(member__membership='voting').aggregate(Sum('amount'))['amount__sum']
        supporting = donations.filter(member__membership='supporting').aggregate(Sum('amount'))['amount__sum']
        extern = donations.filter(member__membership='none').aggregate(Sum('amount'))['amount__sum']

        # hack if queryset was empty
        if not total: total = 0
        if not voting: voting = 0
        if not supporting: supporting = 0
        if not extern: extern = 0
    
        summary.append(
            {"time_range": year,
             "total": total,    
             "voting_amount": voting,
             "supporting_amount": supporting,
             "extern_amount": extern,
             "voting_percent": percent(total, voting),
             "supporting_percent": percent(total, supporting),
             "extern_percent": percent(total, extern)}
        )

        # accumulate
        all_total += total
        all_voting += voting
        all_supporting += supporting
        all_extern += extern

    # acuumulated values
    summary.append(
        {"time_range": "Gesamt",
         "total": all_total,
         "voting_amount": all_voting,
         "supporting_amount": all_supporting,
         "extern_amount": all_extern,
         "voting_percent": percent(all_total, all_voting),
         "supporting_percent": percent(all_total, all_supporting),
         "extern_percent": percent(all_total, all_extern)}
    )
    
    return render(request, 'donations/donation_statistics.html', {'summary': summary})

def percent(total, part):
    if total and part:
        return part/(total/100)
    else:
        return 0
