from django.urls import path
from .views import login_view
from .views import dashboard_view
from .views import logout_view
from .views import register_view
from .views import landing_view

from . import views



urlpatterns = [
    path('', landing_view, name='landing'),  
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('toggle-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('toggle-status/user/<int:jadwal_id>/', views.toggle_status, name='toggle_status'),
    path('jadwal/tambah/', views.tambah_jadwal, name='tambah_jadwal'),
    path('jadwal/edit/<int:jadwal_id>/', views.edit_jadwal, name='edit_jadwal'),
    path('jadwal/hapus/<int:jadwal_id>/', views.hapus_jadwal, name='hapus_jadwal'),
    path('dashboard/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('dashboard/users/jadwal/<int:user_id>/', views.view_user_jadwal, name='view_user_jadwal'),

    

]