from django.shortcuts import render

# Create your views here.
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter

import plotly
import plotly.graph_objs as go 


class VotersListView(ListView):
    '''view to display voters'''
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['birth_year_range'] = range(1910, 2026)
        
        return context

    def get_queryset(self):
        voters = super().get_queryset()

        if 'party' in self.request.GET: 
            party  = self.request.GET['party']
            if party:
                voters = voters.filter(party=party)
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                voters = voters.filter(voter_score=voter_score)
        
       
        if 'v20state' in self.request.GET:
            v20state = self.request.GET['v20state']
            if v20state:
                voters = voters.filter(v20state=True)
        
        if 'v21town' in self.request.GET:
            v21town = self.request.GET['v21town']
            if v21town:
                voters = voters.filter(v21town=True)
        
        if 'v21primary' in self.request.GET:
            v21primary = self.request.GET['v21primary']
            if v21primary:
                voters = voters.filter(v21primary=True)

        if 'v22general' in self.request.GET:
            v22general = self.request.GET['v22general']
            if v22general:
                voters = voters.filter(v22general=True)

        if 'v23town' in self.request.GET:
            v23town = self.request.GET['v23town']
            if v23town:
                voters = voters.filter(v23town=True)
        
        if 'min_birth_year' in self.request.GET: 
            min_birth_year = self.request.GET['min_birth_year']
            if min_birth_year:
                voters = voters.filter(dob__gte=min_birth_year)
        
        if 'max_birth_year' in self.request.GET: 
            max_birth_year = self.request.GET['max_birth_year']
            if max_birth_year: 
                voters = voters.filter(dob__lte=max_birth_year)
           
               
                
        return voters.order_by('dob')    

class VoterDetailView(DetailView):
    '''view to show detail page of one voter'''
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter 
    context_object_name = 'd'
