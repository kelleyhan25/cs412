from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
# Create your views here.
from .models import Article 
import random
from .forms import CreateArticleForm, CreateCommentForm

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
    
class CreateArticleView(CreateView):
    '''A view to handle creation of a new Article.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

class CreateCommentView(CreateView):
    '''A view to create a new comment and save it to the database.'''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('show_all')
        ## note: this is not ideal, because we are redirected to the main page.
