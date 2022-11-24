from django.views.generic import DetailView, View, ListView
from django.shortcuts import redirect, render
from .models import Item, Order, Discount, Tax, ItemOrder
import collections
import stripe

def create_discount_and_tax(order):
    # get random discount
    disc = Discount.objects.order_by('?')[0]
    order.discount = disc
    # get random tax
    tax = Tax.objects.order_by('?')[0]
    order.tax = tax
    return order

# Create your views here.

class ItemDetailView(DetailView):
    model = Item

class ItemListView(ListView):
    model = Item
    
    def add_to_order(request, id, *args, **kwargs):
        item = Item.objects.get(pk = id)
        order, created = Order.objects.get_or_create(session_key = request.session.session_key)
        if created:
            order = create_discount_and_tax(order)
        ItemOrder.objects.create(item = item, order = order).save()
        order.save()
        return render(
            request,
            'shop/item_list.html',
        )

class OrderView(View):
     
    def get(self, request, *args, **kwargs):
        order, created = Order.objects.get_or_create(session_key = request.session.session_key)
        if created:
            order = create_discount_and_tax(order) 
        order.save()
        counter = dict(collections.Counter(order.items.all()))
        context = {'counter': counter, 'order': order}
        return render(request, "shop/order_list.html", context)

class BuyView(View):
    stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

    def get(self, request, id = None, *args, **kwargs):
        
        if id:
            item = Item.objects.get(pk=id)
            coup_id = None
            tax_behavior = 'unspecified'
            tax_code = None
            counter = {item : 1}
        else:
            order  = Order.objects.get(session_key = request.session.session_key)
            coup_id = stripe.Coupon.create(
                percent_off = order.discount.percent_off, 
                duration = order.discount.duration).id
            tax_behavior = order.tax.tax_behavior if order.tax else 'unspecified'
            tax_code = order.tax.code if order.tax else None
            counter = dict(collections.Counter(order.items.all()))

        items = []
        
        for item, quantity in counter.items():
            items.append(
            {
                'price_data': {
                    'currency': 'usd',
                    'tax_behavior': tax_behavior,
                    'product_data': {
                        'name': f'{item.name}',
                        'tax_code': tax_code,
                    },
                    'unit_amount': f'{item.price*100}',
                },
                'quantity': f'{quantity}',
            },
            )
        
        session = stripe.checkout.Session.create(
            line_items = items,
            mode = 'payment',
            discounts=[{
                'coupon': coup_id,
            }],
            success_url='http://localhost:8000/items',
            cancel_url='http://localhost:8000/order',
        )

        return redirect(session.url)



