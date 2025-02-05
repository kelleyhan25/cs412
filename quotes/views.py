from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time

# Create your views here.

QUOTES = [
    "You once told me that the human eye is god's loneliest creation. How so much of the world passes through the pupil and still it holds nothing. The eye, alone in its socket, doesn't even know there's another one, just like it, an inch away, just as hungry, as empty.",
    "Because the sunset, like survival, exists only on the verge of its own disappearing. To be gorgeous, you must first be seen, but to be seen allows you to be hunted.",
    "I am thinking of beauty again, how some things are hunted because we have deemed them beautiful. If, relative to the history of our planet, an individual life is so short, a blink, as they say, then to be gorgeous, even from the day you're born to the day you die, is to be gorgeous only briefly."
]

IMAGES = [
    "static/Interview_2019_Web_Summer_OceanVuong.jpg",
    "static/ov-1712956131052.jpg",
    "static/ocean-vuong-the-advocate.jpg"
]

def main_page(request):
    template = 'quotes/quote.html'
    context = {
        'quote': QUOTES[random.randint(0,2)],
        'image': IMAGES[random.randint(0,2)],
        'current_time': time.ctime(), 
    }
    return render(request, template, context)
    
def show_all(request):
    template = 'quotes/show_all.html'
    context = {
        'quote1': QUOTES[0],
        'quote2': QUOTES[1],
        'quote3': QUOTES[2],
        'pic1': IMAGES[0],
        'pic2': IMAGES[1],
        'pic3': IMAGES[2],
        'current_time': time.ctime(),
    }
    return render(request, template, context)

def about_page(request):
    template = 'quotes/about.html'
    context = {
        'current_time': time.ctime(),
    }
    return render(request, template, context)
    


