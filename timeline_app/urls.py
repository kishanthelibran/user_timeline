from django.urls import path
from .get_user_timeline import get_request

urlpatterns = [
    path('', get_request, name='home')

]
