from django.db.models.query import QuerySet
from .models import ItemModel, Genre
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
    username = request.user.username
    return render(request, 'list.html',{'object_list':object_list, 'username':username})



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

def goodfunc(request, pk):
    object = get_object_or_404(ItemModel, pk=pk)
    object.good = object.good + 1
    object.save()
    return redirect("list")