from django import forms
from blog.models import Category, Article

s = []
cats = Category.objects.all()

for cat in cats:
    s.append((cat.id, cat.title))

class ContactForm(forms.Form):
    name = forms.CharField(min_length=5, widget=forms.TextInput(attrs={'name': 'name', 'placeholder': 'Ваше имя'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'name': 'email', 'placeholder': 'Email'}))
    message = forms.CharField(min_length=20, widget=forms.Textarea(attrs={'name': 'message', 'cols': 30, 'rows': 9, 'placeholder': 'Сообщение'}))


class AddArticle(forms.Form):
    title = forms.CharField(min_length=5, widget=forms.TextInput(attrs={'name': 'title', 'placeholder': 'Зоголовок статьи'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'name': 'description', 'placeholder': 'Описание статьи'}))
    fulltext = forms.CharField(min_length=20, widget=forms.Textarea(attrs={'name': 'fulltext', 'cols': 30, 'rows': 9, 'placeholder': 'Полный текст'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'name': 'image'}))
    cat = forms.ChoiceField(choices=s)

class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=100)

