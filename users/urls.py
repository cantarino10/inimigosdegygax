from . import views
from django.urls import path, include



urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register',views.register, name = 'register'),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('pasword_change',views.password_change, name='password_change'),
    path('reset/<uidb64>/<token>',views.password_reset_confirm,name='password_reset_confirm'),
    path('password_reset',views.password_reset, name='password_reset'),
    
  
]
