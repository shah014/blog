from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, UpdatePassword


# step3: setting url for our views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('register/', RegisterView.as_view(), name='request'),
    path('login/', obtain_auth_token, name='login'),
    path('change_pass/', views.UpdatePassword.as_view()),
    path('contact/', views.ContactCreate.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
