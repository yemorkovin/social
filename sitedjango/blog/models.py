from django.db import models

# Create your models here.
class Contact(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    link = models.CharField(max_length=100, verbose_name='Ссылка')

    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название категории')
    def __str__(self):
        return self.title


class User(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    login = models.CharField(max_length=200, verbose_name='Login')
    email = models.CharField(max_length=200, verbose_name='Email')
    password = models.CharField(max_length=200, verbose_name='Password')

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок стать')
    description = models.TextField(verbose_name='Описание статьи')
    img = models.ImageField(upload_to='blog/static/images', verbose_name='Картинка статьи')
    fulltext = models.TextField(verbose_name='Полный текст статьи')
    cat = models.ForeignKey(Category, models.CASCADE, default=1)
    user = models.ForeignKey(User, models.CASCADE,  default=1)
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Comment(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание статьи')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, default=1)


class Fried(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name} - {self.friend.name}'

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userchat')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendchat')
    message = models.TextField(verbose_name='Сообщение')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.name} - {self.friend.name}'