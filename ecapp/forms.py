from django import forms
from .models import ItemModel, Genre

class ItemForm(forms.ModelForm):

    class Meta:
        model = ItemModel
        fields = ['name', 'image', 'price', 'explanation', 'genre']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].queryset = Genre.objects.all()

        self.fields['name'].widget.attrs.update({
            'class': 'appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
        self.fields['name'].label = '商品名'

        self.fields['image'].widget.attrs.update({
            'class': 'appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
        self.fields['image'].label = '商品画像'

        self.fields['price'].widget.attrs.update({
            'class': 'appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
        self.fields['price'].label = '価格'

        self.fields['explanation'].widget.attrs.update({
            'class': 'appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
        self.fields['explanation'].label = '説明'

        self.fields['genre'].widget.attrs.update({
            'class': 'appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
        self.fields['genre'].label = 'ジャンル'

    def save(self, commit=True):
        instance = super(ItemForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance

