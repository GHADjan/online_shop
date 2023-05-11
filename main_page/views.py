from django.shortcuts import render, redirect
from .models import Category, Product, Cart
from . import models
from .forms import SearchForm
from telebot import TeleBot

bot = TeleBot('6197130919:AAEfcY3pQtaEgbKdYaY7GVISZZIivFBnvtM', parse_mode='HTML')


def index(request):
    # # Получим значение введенное в поисковой строке сайта
    # from_frontend = request.GET.get('exact_product')
    # # было ли введено что-то в поиске
    # if from_frontend is not None:
    #
    #     # Фильтруем продукты по введенному значению
    #     all_products = models.Product.objects.filter(product_name__contains=from_frontend)


    search_bar = SearchForm()
    all_categories = models.Category.objects.all()
    all_products = models.Product.objects.all()


    context = {'products': all_products,
               'all_categories': all_categories,
               'form': search_bar}

    if request.method == "POST":
        product_find = request.POST.get('search_product')
        try:

            search_result = Product.objects.get(product_name=product_find)
            return redirect(f'/item/{search_result.id}')
        except:
            return redirect('/')

    return render(request, 'index.html', context)

def current_category(request, pk):
    category = models.Product.objects.get(id=pk)
    context = {'products', category}
    return render(request, 'current_categories.html', context)


def get_exact_category(request, pk):
    exact_category = models.Category.objects.get(id=pk)
    categories = models.Category.objects.all()
    category_products = models.Product.objects.filter(product_category=exact_category)

    return render(request, 'categrory_products.html', {'category_products': category_products,
                                                       'categories': categories})


#
def exact_product(request, pk):
    product = models.Product.objects.get(id=pk)
    context = {'product': product}
    if request.method == 'POST':
        product_quantity = request.POST.get('user_product_quantity')
        total_for_product = product.product_price * int(product_quantity)
        models.Cart.objects.create(user_id=request.user.id,
                                   user_product=product,
                                   user_product_quantity=product_quantity,
                                   total_for_product=total_for_product)
        return redirect('/cart')

    return render(request, 'about_product.html', context)



def get_user_cart(request, ):
    user_cart = models.Cart.objects.filter(user_id=request.user.id)
    total = sum([i.total_for_product for i in user_cart])
    context = {'cart': user_cart,
               'total': total}
    return render(request, 'user_cart.html',  context)


# Оформление заказа
def complete_order(request, ):
    # Получаем корзину пользователя
    user_card = models.Cart.objects.filter(user_id=request.user.id)
    # Формирование сообщения для тг админа
    result_message = 'Новый заказ(Сайт)\n\n'
    total_for_all_cart = 0
    for cart in user_card:
        result_message += f'<b>{cart.user_product}</b> x {cart.user_product_quantity} = {cart.total_for_product} сум\n'
        total_for_all_cart += cart.total_for_product
    result_message += f'\n-------\n<b>Итого:{total_for_all_cart}сум</b>'
    # Отправляем админу сообщения в тг
    bot.send_message(1088568707, result_message)
    return redirect('/')









