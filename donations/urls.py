"""assembly_stuff URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Member
    path('member/<int:pk>', views.MemberDetailView.as_view(), name='member-detail'),
    path('member/', views.MemberListView.as_view(), name='member-list'),
    path('member/create', views.MemberCreateView.as_view(), name='member-create' ),
    path('member/delete/<int:pk>', views.MemberDeleteView.as_view(), name='member-delete'),
    # Donation
    path('donation/<int:pk>', views.DonationDetailView.as_view(), name='donation-detail'),
    path('donation/', views.DonationListView.as_view(), name='donation-list'),
    path('donation/create', views.DonationCreateView.as_view(), name='donation-create' ),
    path('donation/delete/<int:pk>', views.DonationDeleteView.as_view(), name='donation-delete'),
    # FreqendContriubion
    path('frequentcontribution/<int:pk>', views.FrequentContributionDetailView.as_view(), name='frequentcontribution-detail'),
    path('frequentcontribution/', views.FrequentContributionListView.as_view(), name='frequentcontribution-list'),
    path('frequentcontribution/create', views.FrequentContributionCreateView.as_view(), name='frequentcontribution-create' ),
    path('frequentcontribution/delete/<int:pk>', views.FrequentContributionDeleteView.as_view(), name='frequentcontribution-delete'),
    path('frequentcontribution/execute/<int:pk>', views.execute_frequent , name='frequentcontribution-execute'),
    path('donationcertificate/<int:pk>', views.render_donation_certificate, name='donationcertificate-render'),
]
