from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('user_profile/', views.user_profile_view, name='user_profile'),
    path('upload_item/', views.upload_item_view, name='upload_item'),
    path('view_items/', views.view_items, name='view_items'),
]