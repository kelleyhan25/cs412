from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView 
from django.urls import reverse
# Create your views here.
from .models import Article, Comment
import random
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

class ShowAllView(ListView):
    '''Define a view class to show all blog Articles.'''
    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

    def dispatch(self, request, *args, **kwargs):
        '''override the dispatch method to add debugging information'''
        if (request.user.is_authenticated):
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else: 
            print(f'ShowAllView.dispatch(): not logged in.')
        return super().dispatch(request, *args, **kwargs)

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
    
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Article.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        '''override the default method to add some debug info'''
        print(f'CreateArticleView.form_valid(): {form.cleaned_data}')

        user = self.request.user 
        print(f'CreateArticleView user={user} article.user={user}')
        form.instance.user = user
        return super().form_valid(form)
    
    def get_login_url(self):
        '''return the URL for this app's login page'''
        return reverse('login')

class CreateCommentView(CreateView):
    '''A view to create a new comment and save it to the database.'''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all')
        ## note: this is not ideal, because we are redirected to the main page.
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        return reverse('article', kwargs={'pk':pk})
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the article to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['article'] = article
        return context

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment
        object before saving it to the database.
        '''
        
		# instrument our code to display form fields: 
        print(f"CreateCommentView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        # attach this article to the comment
        form.instance.article = article # set the FK

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    

class UpdateArticleView(UpdateView):
    '''view class to handle update of an article based on its PK'''
    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"

class DeleteCommentView(DeleteView):
    '''view class to delete a comment on an article'''
    model = Comment
    template_name = "blog/delete_comment_form.html"
    context_object_name = 'comment'
    def get_success_url(self):
        '''return the URL to redirect after a success delete'''
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)
        article = comment.article
        return reverse('article', kwargs={'pk':article.pk})
    

class UserRegistrationView(CreateView):
    '''a view to show/process the registration form to create a new user'''

    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User 

    def get_success_url(self):
        '''the url to redirect to after creating a new user'''
        return reverse('login')