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
    sold = models.BooleanField(default=False)
    price_id = models.CharField(max_length=255, unique=True, null=True, blank=True)


    def __str__(self):
        return self.name

    def count_likes(self):
        return self.like_set.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')


