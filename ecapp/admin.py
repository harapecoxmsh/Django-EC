from django.contrib import admin
from .models import ItemModel, Genre
# Register your models here.
admin.site.register(ItemModel)
admin.site.register(Genre)