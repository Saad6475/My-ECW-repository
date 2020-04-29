from math import ceil

from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orderproduct, OrderUpdate
import json
# Create your views here.
def index(request):
    #products = Product.objects.all()
    #print(products)
    #n= len(products)
    #nslides = n//4 + ceil((n/4)-(n//4))
    #perms = {'no_of_slides' : nslides , 'range' : range(1,nslides) , 'Product': products}
    #allprods = [[products,range(1,nslides), nslides] ,[products,range(1,nslides), nslides]]
    allprods= []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n//4 + ceil((n/4)-(n//4))
        allprods.append([prod,range(1,nslides), nslides ])
    perms = {'allprods' : allprods}
    return render(request,'shop/index.html', perms)


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query= request.GET.get('search')

    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)

        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))

        if len(prod) != 0 :
            allprods.append([prod, range(1, nslides), nslides])

    perms = {'allprods': allprods}
    return render(request, 'shop/search.html', perms)

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    thank = False
    if request.method=="POST":
        print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        print(name, email, phone, desc)
        cont = Contact(name=name, email=email, phone=phone, desc=desc)
        cont.save()
        thank= True
    return render(request,'shop/contact.html',{'thank': thank})


def checkout(request):
    if request.method=="POST":
        print(request)
        items_json = request.POST.get('itemsJson', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orderproduct(items_json=items_json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone, amount= amount)
        order.save()
        # when someone place order then we receive an update
        update = OrderUpdate(order_id=order.id, update_desc="The order has been placed")
        update.save()
        thank = True
        id =order.id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request,'shop/checkout.html')


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        #return HttpResponse(f"{orderId} and {email}")
        try:
            order = Orderproduct.objects.filter(id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc, 'time':item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')



def products(request, myid):
    # Fetch the product using id
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, 'shop/prodview.html', {'product':product[0]})
