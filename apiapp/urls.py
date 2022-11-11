from django.urls import path
from .views import ResourceAPI, home
urlpatterns = [
    path('s/<str:name>/', ResourceAPI.as_view()),
    path('s/', ResourceAPI.as_view()),
    path('c/', home),
]