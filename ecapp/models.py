from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ItemModel(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='')
    price = models.IntegerField()
    explanation = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    good = models.IntegerField(null=True, blank=True, default=0)


    def __str__(self):
        return self.name