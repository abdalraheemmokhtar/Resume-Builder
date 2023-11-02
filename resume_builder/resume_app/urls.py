from django.urls import path
from .views import  download_cv, other_view, generate_text, home

urlpatterns = [
    # path('', home, name='home'),
    path('', other_view, name='other_view'),
    path('home/', home, name='home'),
    path('download_cv/', download_cv, name='download_cv'),
    path('hug/',generate_text, name='generate_text'),
    # Add more views as needed
]
