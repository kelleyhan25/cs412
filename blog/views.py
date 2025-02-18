from django.shortcuts import render
from django.views.generic import ListView, DetailView
# Create your views here.
from .models import Article 
import random

class ShowAllView(ListView):
    '''Define a view class to show all blog Articles.'''
    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

class ArticleView(DetailView):
    '''Display a single article'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"


class RandomArticleView(DetailView):
    '''display a single article selected at random.'''
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    #methods 
    def get_object(self):
        '''return one instance of the article object selected at random.'''
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article