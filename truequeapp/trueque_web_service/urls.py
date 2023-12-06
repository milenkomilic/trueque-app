from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('user_profile/', views.user_profile_view, name='user_profile'),
    path('upload_item/', views.upload_item_view, name='upload_item'),
    path('view_items/', views.view_items, name='view_items'),
    path('initiate_trade/<int:item_id>/', views.initiate_trade, name='initiate_trade'),
    path('respond_to_trade/', views.respond_to_trade, name='respond_to_trade'),
    path('my_items/', views.my_items, name='my_items'),
    path('update_item/', views.update_item, name='update_item'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('reset/<uidb64>/<token>/', views.activate_pwd, name='activate_pwd'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
]
