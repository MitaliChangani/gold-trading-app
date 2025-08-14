from django.urls import path
from . import views
urlpatterns = [
    path('create_order', views.create_order, name='create_order'),
    path('payment_verify', views.payment_verify, name='payment_verify'),
    path('signup', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('withdraw', views.withdraw_request, name='withdraw'),
]