from django.urls import path
from . import views
from .views import RemainderCreate

urlpatterns = [
    path('signup', views.signup_user, name='signup'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('remainderCreate', RemainderCreate.as_view(), name='remaindersCreate'),
    path('remainderList', views.remainderList, name='remaindersList'),

]
