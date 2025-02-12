from django.shortcuts import render
import time 
import random 

FOOD = [
        "/static/1*E5htcQnqzILj8iu2gb3BkQ.jpg",
        "/static/shengjian-mantou-26.jpg",
    ]

SPECIAL_PIC = [
    "/static/image-resizing.jpeg",
    "/static/9169jed2x1e81.jpg",
    "/static/image-resizing-1.jpeg",
    "/static/Unknown.jpeg",
    "/static/Unknown-1.jpeg",
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
    '''Show the form to the user.'''
    template_name = 'restaurant/main.html'
    context = {
        'pic1':FOOD[0],
        'pic2':FOOD[1],
    }
    return render(request, template_name, context)

def order_page(request):
    '''Show the form to the user.'''
    template_name = 'restaurant/order.html'
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
    
    current_time = time.time()
    random_time = current_time + random.randint(30 * 60, 60 * 60)
    confirmation_time = time.ctime(random_time)
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