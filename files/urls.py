from django.urls import path
from .views import *

urlpatterns = [
    path('<path:directory_path>/', view, name='view'),
    path('', home, name='files'),
]