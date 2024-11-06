from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from .models import Result

# Create your views here.
class ResultsListView(ListView):
    template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = 'results'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        return qs[:25]