from django.db.models.query import QuerySet
import stripe.error
from .models import ItemModel, Genre, Like
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from .forms import ItemForm
from django.shortcuts import get_object_or_404
from django.conf import settings

import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY




# Create your views here.
def signupfunc(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, " ", password)
            return redirect('signin')
        except IntegrityError:
            return render(request, 'signup.html', {'error':'このユーザーはすでに登録されています'})

    return render(request, 'signup.html', {})

def signinfunc(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return render(request, 'signin.html', {'context':'not logged in'})

    return render(request, 'signin.html', {'context':'get method'})

def logoutfunc(request):
    logout(request)
    return redirect('signin')


def listfunc(request):
    object_list = ItemModel.objects.all()
    genre_list = Genre.objects.all()
    username = request.user.username
    return render(request, 'list.html',{'object_list':object_list, 'genre_list':genre_list, 'username':username})

def create_stripe_price(product_name, unit_amount):

    product_data = {
        'name': product_name
    }

    product = stripe.Product.create(**product_data)

    price = stripe.Price.create(
        product=product.id,
        unit_amount=unit_amount,
        currency='jpy'
    )

    return price.id

class ItemCreate(CreateView):
    model = ItemModel
    template_name = 'create.html'
    form_class = ItemForm
    success_url = reverse_lazy('list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre_list'] = Genre.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        product_name = form.cleaned_data['name']
        unit_amount = form.cleaned_data['price']
        form.instance.price_id = create_stripe_price(product_name, unit_amount)
        return super().form_valid(form)



class ItemSearch(ListView):
    model = ItemModel
    template_name = 'search_item.html'

    def get_queryset(self):
        query = super().get_queryset()
        name = self.request.GET.get('name', None)
        if name:
            query = query.filter(name__icontains=name)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = self.request.GET.get('name', '')
        return context

@login_required
def detailfunc(request, pk):
    object = get_object_or_404(ItemModel, pk=pk)
    username = request.user.username
    return render(request, 'detail.html', {'object':object, 'username':username})

def like_item(request, pk):
    item = get_object_or_404(ItemModel, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, item=item)
    if not created:
        like.delete()
    return redirect('list')

def liked_items_list(request):
    likes = Like.objects.filter(user=request.user)
    items = [like.item for like in likes]
    username = request.user.username
    return render(request, 'liked_items_list.html', {'items': items, 'username':username})

def item_filter(request):
    username = request.user.username
    genre_name = request.GET.get('genre')
    if genre_name:
        filtered_items = ItemModel.objects.filter(genre__name=genre_name).order_by('name')
    else:
        filtered_items = ItemModel.objects.all().order_by('genre__name')
    return render(request, 'genrefilter.html', {'filtered_items': filtered_items, 'username':username})

# def mark_item_as_sold(request, pk):
#     item = get_object_or_404(ItemModel, pk=pk)
#     item.sold = True
#     item.save()
#     return redirect('list')

DOMAIN = settings.SITE_DOMAIN

def checkout(request, pk):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    order_item = get_object_or_404(ItemModel, pk=pk)
    price_id = order_item.price_id

    if request.method == "POST":

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=DOMAIN+"success",
            cancel_url=DOMAIN+"cancel"
        )
        return redirect(checkout_session.url, code=303)
    return render(request, "checkout.html", {'order_item': order_item})


def success(request):
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")