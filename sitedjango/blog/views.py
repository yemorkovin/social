from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from blog.models import *
from blog.forms import ContactForm, AddArticle, SearchForm
from django.core.mail import send_mail

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def contact(request):
    if request.method == 'POST':
        pass #если форма отправлена, то есть пользователь нажал на кнопку Отправить
        request.session['a'] = 'Форма успешно отправлена'
        return redirect('/contact')
    else:
        suc = ''
        if 'a' in request.session:
            suc = request.session['a']
        form = ContactForm() #если форма не отправлена, то есть пользователь просто зашел на страницу
    return render(request, 'contact.html', context={'form': form, 'suc': suc})



def index(request):

    return render(request, 'index.html')

def contacts(request):
    contacts = Contact.objects.all()

    context = {
        'contacts': contacts,
    }


    return render(request, 'contacts.html', context=context)

def articles(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            articles = Article.objects.filter(title=query)
        else:
            articles = Article.objects.all()
    else:
        form = SearchForm()
        articles = Article.objects.all()
    art_new = []
    for article in articles:
        art_new.append({
            'title': article.title,
            'description': article.description,
            'img': str(article.img)[5:],
            'id': article.id,
            'category': article.cat.title,
            'user': article.user,
            'date': article.date
        })

    context = {
        'articles': art_new,
        'form': form
    }
    return render(request, 'articles.html', context=context)

def articlesid(request, id):

    if request.method == 'POST':
        name = request.POST['name']
        comment = request.POST['comment']
        ids = Article.objects.filter(id=request.POST['id']).first()
        images = ids.img[5:]
        com = Comment()
        com.title = name
        com.description = comment
        com.article = ids
        com.save()

    article = Article.objects.filter(id=id).first()
    images = str(article.img)[5:]
    a = {
        'article': article,
        'images':images
    }
    return render(request, 'articledetail.html', context=a)

def reg(request):
    errors = ''
    suc = ''
    if request.method == 'POST':
        name = request.POST['name']
        login = request.POST['login']
        email = request.POST['email']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']
        if (password_repeat == password) and (not User.objects.filter(login=login).exists()):
            user = User()
            user.name = name
            user.login = login
            user.email = email
            user.password = password
            user.save()
            suc = 'Вы успешно зарегистрированы!'
        else:
            errors += 'Пароли не совпадают или такой пользователь под логинов '+login+' уже зарегистрирован'
    context = {
        'errors': errors,
        'suc': suc
    }
    return render(request, 'reg.html', context=context)

def auth(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        if User.objects.filter(login=login).exists() and User.objects.filter(password=password).exists():
            request.session['login'] = login
            return redirect('/panel')
    return render(request, 'auth.html')


def panel(request):
    if 'login' in request.session:
        #если прошел авторизацию
        loginsession = request.session['login']
        print(loginsession)
        data = User.objects.filter(login=loginsession).first()
        print(data)
        if request.method == 'POST':
            name = request.POST['name']
            login = request.POST['login']
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.filter(id=data.id).first()
            user.name = name
            user.login = login
            user.email = email
            user.password = password
            user.save()
            return redirect('/panel')
        a = {
            'data': data
        }
        return render(request, 'panel.html', context=a)
    else:
        #не авторизирован
        return redirect('/reg')

def logout(request):
    if 'login' in request.session:
        del request.session['login']
    return redirect('/reg')
def handle_uploaded_file(f):
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def addarticle(request):
    if 'login' in request.session:
        suc = ''
        if request.method == "POST" and request.FILES:

            title = request.POST['title']
            description = request.POST['description']
            fulltext = request.POST['fulltext']
            cat = request.POST['cat']

            image = request.FILES['image']

            f = FileSystemStorage()
            f_name = f.save(image.name, image)

            art = Article()
            art.title = title
            art.description = description
            art.fulltext = fulltext
            art.cat = Category.objects.filter(id=cat).first()
            art.user = User.objects.filter(login=request.session['login']).first()
            art.img = 'blog/static/images/'+f_name
            art.save()

            article = Article.objects.order_by('-id').first()
            send_notification(request.session['login'], 'http://127.0.0.1:8000/article/'+str(article.id))


            suc = 'Вы усппешно добавили новую статью!'
            #return redirect('/addarticle')
        form = AddArticle
        return render(request, 'addarticle.html', context={'form': form, 'suc':suc})
    else:
        return render(request, '404.html')

def listarticles(request):
    if 'login' in request.session:
        user = User.objects.get(login=request.session['login'])

        articles = Article.objects.filter(user=user)
        return render(request, 'listarticles.html', context={'articles': articles})
    else:
        return render(request, '404.html')


def send_notification(user, link_article):
    subject = 'Оповещение добавления новой статьи от пользователя ' + user
    message = 'Добавлена новая статья, которая доступна по ссылке ' + link_article
    from_email = 'tmp@yandex.ru'
    users = User.objects.all()
    email_list = []
    for user in users:
        email_list.append(user.email)
    send_mail(subject, message, from_email, email_list)

#ajax
def users(request):
    users = User.objects.all()
    return render(request, 'user/users.html', context={'users': users})

def userdetail(request, login):

    user = User.objects.filter(login=login).first()
    user_f = get_object_or_404(User, id=user.id)
    current_user = get_object_or_404(User, login=request.session['login'])
    s = False
    if Fried.objects.filter(user=current_user, friend=user_f).exists():
        s = True
    return render(request, 'user/userdetail.html', context={'user': user, 's': s})




def send(request):
    subject = 'Тема письма'
    message = 'Текст письма.'
    from_email = 'nf.morkovin@gmail.com'
    recipient_list = ['nf.morkovin@gmail.com']

    send_mail(subject, message, from_email, recipient_list)

    return HttpResponse('Письмо успешно отправлено.')



def addfriend(request):
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.POST['id_friend'])
        current_user = get_object_or_404(User, login=request.session['login'])
        if user==current_user:
            return redirect('/user/'+user.login)

        if not Fried.objects.filter(user=current_user, friend=user).exists():
            Fried.objects.create(user=current_user, friend=user)
        return redirect('/user/'+user.login)

def chatid(request, id):
    user = get_object_or_404(User, login=request.session['login'])
    frienduser = get_object_or_404(User, id=id)
    if request.method == 'POST':
        message = request.POST['message']
        Chat.objects.create(user=user, friend=frienduser, message=message)
    #chats = Chat.objects.filter(user=user, friend=frienduser)

    #(user=user and frienduser=frienduser) or (user=frienduser and friend=user)
    chats_1 = Chat.objects.filter(Q(user=user, friend=frienduser) | Q(user=frienduser, friend=user)).order_by('date')


    return render(request, 'chat/chatid.html', context={'chats': chats_1, 'friend':id, 'user': request.session['login']})


def ajaxchat(request):
    if request.method == 'POST':
        # Получение данных из POST-запроса
        data = json.loads(request.body)
        user = get_object_or_404(User, login=request.session['login'])
        frienduser = get_object_or_404(User, id=data['friend'])

        chats_1 = Chat.objects.filter(Q(user=user, friend=frienduser) | Q(user=frienduser, friend=user)).order_by(
            'date')

        r = ''
        for i in chats_1:
            r += '<div class ="chat_mesaage_item" >'
            r += '<p>' + i.user.login + ' ' + str(i.date) + '</p>'
            r += '<p>' + i.message + '</p>'
            if user == i.user:
                r += '<p> <a href="" onclick="deleteitemmessage('+str(i.id)+')"> Удалить </a></p>'
            r += '</div>'
        response_data = {'data': r}
        return JsonResponse(response_data)

def ajaxdelete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data['id']
        Chat.objects.filter(id=id).delete()
        response_data = {'data': 1}
        return JsonResponse(response_data)

