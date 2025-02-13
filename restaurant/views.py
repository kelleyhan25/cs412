# File: views.py 
# Author: Kelley Han (kelhan@bu.edu), 2/11/2025 
# Description: Functions that provide HTTP Response for pages in the restaurant app

from django.shortcuts import render
import time 
import random 
import socket 
CS_DEPLOYMENT_HOSTNAME = 'cs-webapps.bu.edu'

if socket.gethostname() == CS_DEPLOYMENT_HOSTNAME:
    FOOD = [
        "https://cs-webapps.bu.edu/kelhan/static/1*E5htcQnqzILj8iu2gb3BkQ.jpg",
        "https://cs-webapps.bu.edu/kelhan/static/shengjian-mantou-26.jpg",
    ]

    SPECIAL_PIC = [
    "https://cs-webapps.bu.edu/kelhan/static/image-resizing.jpeg",
    "https://cs-webapps.bu.edu/kelhan/static/9169jed2x1e81.jpg",
    "https://cs-webapps.bu.edu/kelhan/static/image-resizing-1.jpeg",
    "https://cs-webapps.bu.edu/kelhan/static/Unknown.jpeg",
    "https://cs-webapps.bu.edu/kelhan/static/Unknown-1.jpeg",
]
else:
    FOOD = [
        "https://cs-webapps.bu.edu/kelhan/static/1*E5htcQnqzILj8iu2gb3BkQ.jpg",
        "https://cs-webapps.bu.edu/kelhan/static/shengjian-mantou-26.jpg",
    ]

    SPECIAL_PIC = [
    "https://cs-webapps.bu.edu/kelhan/static/image-resizing.jpeg",
    "https://cs-webapps.bu.edu/kelhan/static/9169jed2x1e81.jpg",
    "https://cs-webapps.bu.edu/kelhanstatic/image-resizing-1.jpeg",
    "https://cs-webapps.bu.edu/kelhan/static/Unknown.jpeg",
    "https://cs-webapps.bu.edu/kelhan/static/Unknown-1.jpeg",
]


DAILY_SPECIAL = [
    "Shanghai-Style Chow Mein: comes with udon noodles with carrots, cabbage, onion, mushroom, and chicken, stir-fried in a delicious house sauce.",
    "Braised Pork Belly with Preserved Vegetables: comes with a side of rice and extra sauce.",
    "House Fried Rice: comes with egg, peas, carrots, shrimp, sliced ham and green onions.",
    "Five-spice Beef Stew Noodle Soup: comes with thin, hand-pulled noodles, stewed beef and vegetables, and broth.",
    "The-All-American: comes with a side of rice, orange chicken, egg rolls, sticky honey chicken wings, and a soda of choice."
]

# Create your views here.
def main_page(request):
    '''Show the main page to the user.'''
    template_name = 'restaurant/main.html'
    context = {
        'pic1':FOOD[0],
        'pic2':FOOD[1],
    }
    return render(request, template_name, context)

def order_page(request):
    '''Show the form to the user.'''
    template_name = 'restaurant/order.html'
    # For randomized daily special, reloads every time the user reloads the webpage
    picture_num = random.randint(0,4)
    context = {
        'daily_special':DAILY_SPECIAL[picture_num],
        'special_pic':SPECIAL_PIC[picture_num]
    }
    return render(request, template_name, context)

def confirmation(request):
    '''Process the form submission and generate a result'''
    template_name = 'restaurant/confirmation.html'
    print(request)
    # Collecting data that the user submitted in the form
    if request.POST: 
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        dumpling = request.POST.getlist('dumpling')
        filling = request.POST.getlist('filling')
        drink = request.POST.getlist('drink')
        special = request.POST['special']
        daily_special = request.POST.get('dailyspecial', None)

        if not dumpling: 
            dumpling = []
        if not filling: 
            filling = []
        if not drink: 
            drink = []
        
        dumpling_prices = {
            "Shanghai Pan Fried Dumpling $8.99": 8.99,
            "Shanghai Soup Dumpling $10.99": 10.99,
            "Shanghai Pan Fried Buns $7.99": 7.99,
            "Steamed Dumplings $6.99": 6.99,
        }
        drink_prices = {
            "Soy Milk": 4.99,
            "Apple Juice": 2.99,
            "Soda": 3.99,
            "Beer": 5.99,
        }
    
    # Calculating the time it takes for order to be ready at random 
    current_time = time.time()
    random_time = current_time + random.randint(30 * 60, 60 * 60)
    confirmation_time = time.ctime(random_time)

    # Calculates the subtotal, tax at 9% and final price
    sub_total = 0
    dumpling_price = 0
    drink_price = 0
    for dumpling_item in dumpling: 
        dumpling_price = dumpling_prices.get(dumpling_item, 0)
        sub_total += dumpling_price
    for drink_item in drink:
        drink_price = drink_prices.get(drink_item, 0)
        sub_total += drink_price
    if daily_special:
        sub_total += 15.99

    # Final prices 
    tax = sub_total * 0.09
    rounded_tax = round(tax, 2)
    total = sub_total + rounded_tax

    context = {
            'name':name,
            'phone':phone, 
            'email':email, 
            'dumpling':dumpling, 
            'filling':filling, 
            'drink':drink, 
            'special':special,
            'ready_time': confirmation_time, 
            'time_right_now': time.ctime(),
            'sub_total': round(sub_total, 2),
            'tax': rounded_tax,
            'total': round(total, 2),
            'dumpling_price':dumpling_price,
            'drink_price':drink_price,
            'daily_special':daily_special,
        }


    return render(request, template_name, context)