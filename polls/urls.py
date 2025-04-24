from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from .views import Login, Logout, NewUser, PollList, PollDetail, NewPoll, DeletePoll

app_name = 'polls'

urlpatterns = [
    path('', PollList.as_view(), name='index'),
    path('vote/<int:pk>/', PollDetail.as_view(), name='vote'),
    path('new/', NewPoll.as_view(), name='new_poll'),
    path('delete/<int:pk>/', DeletePoll.as_view(), name='delete_poll'),
    path('register/', NewUser.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]


urlpatterns += staticfiles_urlpatterns()