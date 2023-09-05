from django.urls import path
from . import views
from .views import RemainderCreate, RemainderListView

urlpatterns = [
    path('signup', views.signup_user, name='signup'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('login-otp', views.login_with_otp, name="login-otp"),
    path('remainderCreate', RemainderCreate.as_view(), name='remaindersCreate'),
    path('remainderList', RemainderListView.as_view(), name='remaindersList'),
    path('search', views.searchUser, name='search-for-user'),

]
