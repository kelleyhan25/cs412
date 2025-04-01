# voter_analytics/views.py 
# Kelley Han kelhan@bu.edu 
# This file contains all the renderings and views of the voters information display and graphs 
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
        '''returns the context variables'''
        context =  super().get_context_data(**kwargs)
        context['birth_year_range'] = range(1910, 2026)
       
        return context

    def get_queryset(self):
        '''returns the query set based on the form submissions and filters accordingly'''
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

class GraphDataListView(ListView):
    '''view to show graphs of aggregate data about Voter records'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'g'


    def get_queryset(self):
        '''returns the query set based on the form submissions and filters accordingly'''
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


        return voters 
    def get_context_data(self, **kwargs):
        '''provide context variables for use in the template'''
        context = super().get_context_data(**kwargs)
        g = context['g']
        context['birth_year_range'] = range(1910, 2026)
        
        # code to create and display a histogram (bar chart), illustrating distribution of Voters by birth year 
        birth_years_count = {}
        for person in g:
            year = person.dob[:4]
            if (year in birth_years_count.keys()):
                # if the year already exists as a key 
                birth_years_count[year] = birth_years_count[year] + 1
            else:
                # year does not exist as a key, add 1 
                birth_years_count[year] = 1
            
        labels = sorted(birth_years_count.keys())
        counts = []
        for y in labels: 
            count = birth_years_count.get(y)
            counts.append(count)
        
        fig = go.Bar(x=labels, y=counts)
        title_text = f"Voter distribution by Year of Birth"
        graph_div_year = plotly.offline.plot({"data":[fig],
                                              "layout_title_text": title_text},
                                              auto_open=False,
                                              output_type="div")
        
        context['graph_div_year'] =  graph_div_year

        # code to create and display a pie chart illustrating the distribution of Voters by party affiliation (similar logic as above)
        party_count = {}
        for person in g: 
            party = person.party 
            if (party in party_count.keys()):
                party_count[party] += 1
            else:
                party_count[party] = 1
        
        labelparty = list(party_count.keys())
        partycounts = []
        for y in labelparty: 
            c = party_count.get(y)
            partycounts.append(c)
        
        pie = go.Pie(labels=labelparty, values=partycounts)
        title_text_pie = f"Voter distribution by Party Affiliation"
        graph_div_party = plotly.offline.plot({"data":[pie],
                                               "layout_title_text": title_text_pie},
                                               auto_open=False,
                                               output_type="div")
        
        context['graph_div_party'] = graph_div_party

        # code to create and display a histogram (bar chart) illustrating the distribution of Voters by participation in elections 
        election_count = {
            'v20state': 0,
            'v21town': 0,
            'v21primary': 0,
            'v22general': 0,
            'v23town': 0
        }

        for person in g: 
            if person.v20state == True: 
                election_count['v20state'] += 1
            if person.v21town == True: 
                election_count['v21town'] += 1
            if person.v21primary == True: 
                election_count['v21primary'] += 1
            if person.v22general == True:
                election_count['v22general'] += 1
            if person.v23town == True:
                election_count['v23town'] += 1
           
             
            
        election_labels = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        electioncounts = []
        for y in election_labels: 
            c = election_count[y]
            electioncounts.append(c)

        electionbar = go.Bar(x=election_labels, y=electioncounts)
        title_text_elect = f"Vote Count by Election"
        graph_div_elect = plotly.offline.plot({"data":[electionbar],
                                                "layout_title_text": title_text_elect},
                                                auto_open=False, 
                                                output_type="div")
        context['graph_div_elect'] = graph_div_elect
        return context 
    
   