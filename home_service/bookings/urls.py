from django.urls import path
from .views import *

urlpatterns = [
    path('freelancers/<int:service_id>/', freelancer_list, name='freelancer_list'),
    path('review/<int:booking_id>/', add_review, name='add_review'),
    path('book/<int:service_id>/', create_booking, name='create_booking'),
]