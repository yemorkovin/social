
from django.urls import path
from blog.views import *

main_patterns = [
    path('contacts/', contacts),
    path('articles/', articles),
    path('', index),
]