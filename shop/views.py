from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from shop.models import *
from django.views import View

from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

import datetime

# Create your views here.
class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
  
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
  
        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('home:home')
  
    def get(self, request):
        # print()
        return HttpResponseRedirect(f'/{request.get_full_path()[1:]}')


def catalog(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()
  
    data = {}
    data['products'] = products
    data['categories'] = categories
  
    print('you are : ', request.session.get('email'))
    return render(request, 'shop.html', data)

  

class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request , 'cart.html' , {'products' : products} )

class CheckOut(View):
	def post(self, request):
		address = request.POST.get('address')
		phone = request.POST.get('phone')
		customer = request.session.get('customer')
		cart = request.session.get('cart')
		products = Product.get_products_by_id(list(cart.keys()))
		print(address, phone, customer, cart, products)

		for product in products:
			print(cart.get(str(product.id)))
			order = Order(customer=Customer(id=customer),
						product=product,
						price=product.price,
						address=address,
						phone=phone,
						quantity=cart.get(str(product.id)))
			order.save()
		request.session['cart'] = {}

		return redirect('shop:cart')


class OrderView(View):

	def get(self, request):
		customer = request.session.get('customer')
		orders = Order.get_orders_by_customer(customer)
		print(orders)
		return render(request, 'orders.html', {'orders': orders})
