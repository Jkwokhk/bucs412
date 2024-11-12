# voter_analytics/views.py
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect

# define views for voter_analytics
# Create your views here.
from typing import Any
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django import forms
from .models import *
import random
import plotly
import plotly.express as px
from django.utils.html import format_html
from django.db.models import Count

import plotly.graph_objs as go
from collections import Counter
# Create your views here.

class VoterFilterForm(forms.Form):
    party_affiliation = forms.ChoiceField(choices=[('', 'Any')] + [(p, p) for p in Voter.objects.values_list('party_affiliation', flat=True).distinct()], required=False)
    min_birth_year = forms.ChoiceField(choices=[('', 'Any')] + [(y, y) for y in range(1920, 2025)], required=False)
    max_birth_year = forms.ChoiceField(choices=[('', 'Any')] + [(y, y) for y in range(1920, 2025)], required=False)
    voter_score = forms.ChoiceField(choices=[('', 'Any')] + [(str(i), str(i)) for i in range(6)], required=False)
    voted_20state = forms.BooleanField(required=False)
    voted_21town = forms.BooleanField(required=False)
    voted_21primary = forms.BooleanField(required=False)
    voted_22general = forms.BooleanField(required=False)
    voted_23town = forms.BooleanField(required=False)

class VoterListView(ListView):
    '''view for list of voters'''
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()
        # print(queryset)
        form = self.form = VoterFilterForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data['party_affiliation']:
                queryset = queryset.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data['min_birth_year']:
                queryset = queryset.filter(date_of_birth__year__gte=form.cleaned_data['min_birth_year'])
            if form.cleaned_data['max_birth_year']:
                queryset = queryset.filter(date_of_birth__year__lte=form.cleaned_data['max_birth_year'])
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            if form.cleaned_data['voted_20state']:
                queryset = queryset.filter(v20state=True)
            if form.cleaned_data['voted_21town']:
                queryset = queryset.filter(v21town=True)
            if form.cleaned_data['voted_21primary']:
                queryset = queryset.filter(v21primary=True)
            if form.cleaned_data['voted_22general']:
                queryset = queryset.filter(v22general=True)
            if form.cleaned_data['voted_23town']:
                queryset = queryset.filter(v23town=True)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context
    
class VoterDetailView(DetailView):
    '''detail view for a voter'''
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'

class VoterGraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = Voter.objects.all()
        form = self.form = VoterFilterForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data['party_affiliation']:
                queryset = queryset.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data['min_birth_year']:
                queryset = queryset.filter(date_of_birth__year__gte=form.cleaned_data['min_birth_year'])
            if form.cleaned_data['max_birth_year']:
                queryset = queryset.filter(date_of_birth__year__lte=form.cleaned_data['max_birth_year'])
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            if form.cleaned_data['voted_20state']:
                queryset = queryset.filter(v20state=True)
            if form.cleaned_data['voted_21town']:
                queryset = queryset.filter(v21town=True)
            if form.cleaned_data['voted_21primary']:
                queryset = queryset.filter(v21primary=True)
            if form.cleaned_data['voted_22general']:
                queryset = queryset.filter(v22general=True)
            if form.cleaned_data['voted_23town']:
                queryset = queryset.filter(v23town=True)
        return queryset

        
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve voter info
        # voters = Voter.objects.all()
        voters = self.get_queryset()
        # get yob
        year_of_birth = []
        for voter in voters:
            if voter.date_of_birth:
                year = voter.date_of_birth.year
                year_of_birth.append(year)
        year_counts = Counter(year_of_birth)
        year_data = sorted(year_counts.items())

        # Histogram
        x=[year for year, count in year_data]
        y=[count for year, count in year_data]
        # generate the histogram
        year_histogram = go.Bar(x= x, y = y)
        total_sample = sum(y)
        title=f"Voter Distribution by Year of Birth n = {total_sample}"
        # obtain the graph as HTML div
        graph_div_histogram = plotly.offline.plot({
            "data": [year_histogram],
            "layout_title_text": title,
            },
            auto_open=False,
            output_type='div')
        
        context['graph_div_histogram'] = graph_div_histogram

        # pie chart
        x = [voter.party_affiliation for voter in voters if voter.party_affiliation]
        y = Counter(x)
        # generate pie chart
        party_pie = go.Pie(labels=list(y.keys()), values=list(y.values()))
        total_sample = sum(y.values())
        title = f"Voter distribution by Party Affiliation n = {total_sample}"
        graph_div_party = plotly.offline.plot({
            "data": [party_pie],
            "layout_title_text": title,
        },
        auto_open=False,
        output_type='div')
        context['graph_div_party'] = graph_div_party

        # participation histogram
        election_field = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = {field: 0 for field in election_field}
        for voter in voters:
            for field in election_field:
                if getattr(voter, field, False):
                    election_counts[field] += 1

        x = election_field
        y = [election_counts[field] for field in election_field]
        total_sample = sum(y)
        title = f"Vote Count by Election n={total_sample}"
        vote_histogram = go.Bar(x=x, y=y)
        # obtain the graph as HTML div
        graph_div_count = plotly.offline.plot({
            "data": [vote_histogram],
            "layout_title_text": title,
            },
            auto_open=False,
            output_type='div')
        context['graph_div_count'] = graph_div_count

        context['form'] = self.form
        return context

    