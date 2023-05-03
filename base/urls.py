from django.urls import path
from . import views


urlpatterns = [
    path('', views.landpage, name='landpage'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('home/', views.home, name='home'),
    path('post/<str:pk>', views.post, name='post'),
    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),
    path('profile/<str:pk>', views.userProfile, name='profile'),
    path('create-post/', views.createPost, name='create-post'),
    path('update-post/<str:pk>', views.updatePost, name='update-post'),
    path('delete-post/<str:pk>', views.deletePost, name='delete-post'),
    path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),
]