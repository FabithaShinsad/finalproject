from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/',views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('booking/<int:booking_id>/<str:action>/', views.update_booking_status, name='update_booking_status'),
    path('notifications/', views.notifications, name='notifications'),
    path('booking/update/<int:booking_id>/<str:action>/', views.update_booking, name='update_booking'),
    path('edit-profile/', views.edit_freelancer_profile, name='edit_profile'),
    path('edit-client-profile/', views.edit_client_profile, name='edit_client_profile'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('review/<int:booking_id>/', views.view_review, name='view_review'),
]